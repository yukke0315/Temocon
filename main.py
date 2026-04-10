from fastapi import FastAPI, WebSocket, Form, Request, status
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pyautogui as pag   # os操作をするため(ツールチャンネル参照)
import json
import os
import uuid   # トークン用
import time
import webbrowser   # ブラウザ起動用
import subprocess   # アプリ起動用

# インスタンス作成
app = FastAPI()

# 安全装置オフ
pag.FAILSAFE = False
pag.PAUSE = 0   # デフォの0.1s待機を無効に(カクカク解消)

# 認証用パスワードとCookie設定
PASSWORD = os.getenv("TEMOCON_PASSWORD", "devpass")
COOKIE_NAME = "temocon_session"
COOKIE_VALUE = str(uuid.uuid4())

# セッション管理用
SESSION_TIMEOUT = 60   # 試験用60秒

# -ログイン画面-
@app.get("/login")
async def get_login():
    return FileResponse("static/login.html")

# -ログイン処理-
@app.post("/login")
async def post_login(password: str = Form(...)):
    if password == PASSWORD:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key=COOKIE_NAME, value=COOKIE_VALUE, httponly=True)
        return response
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

# -トップ-
@app.get("/")
async def get_index(request: Request):
    cookie = request.cookies.get(COOKIE_NAME)
    if cookie != COOKIE_VALUE:
        return RedirectResponse(url="/login")
    return FileResponse("static/index.html")

# -WS処理-
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Cのpthreと違って１スレッドでやるぽい？

    # このタイミングでもチェック
    cookie = websocket.cookies.get(COOKIE_NAME)
    if cookie != COOKIE_VALUE:
        await websocket.close()
        return
    
    await websocket.accept()
    print("接続完了")

    # 最初の基準
    last_active_time = time.time()

    try:
        while True:
            # スマホからのデータ待ちすいせい
            # awaitだと、待ちの間は他の処理もできる
            data = await websocket.receive_text()

            try:
                msg = json.loads(data)   # JSON文字列を辞書型に変換
            except:
                continue

            # セッションタイムアウトチェック
            if time.time() - last_active_time > SESSION_TIMEOUT:
                print("session timeout")
                await websocket.close()
                break

            last_active_time = time.time()   # アクティブ時間更新

            # マウス処理
            if msg.get("type") == "move":
                try:
                    x = msg.get("x", 0)
                    y = msg.get("y", 0)
                    # 感度
                    sensitivity = 5.0

                    # マウス移動（相対座標）
                    pag.moveRel(x * sensitivity, y * sensitivity)

                except Exception as e:
                    print(f"Move Error: {e}")

            elif msg.get("type") == "scroll":
                try:
                    dy = msg.get("dy", 0)
                    scroll_sensitivity = 4.0

                    # 指を下（dy負）で下スクロール
                    pag.scroll(int(dy * scroll_sensitivity))
                except Exception as e:
                    print(f"Scroll Error: {e}")

            elif msg.get("type") == "command":
                # コマンド処理
                cmd = msg.get("command")
                print(f"cmd: {cmd}")

                if cmd == "volume_up":
                    pag.press("volumeup")
                    print("Volume UP")

                elif cmd == "volume_down":
                    pag.press("volumedown")
                    print("Volume DOWN")

                elif cmd == "play_pause":
                    pag.press("playpause")
                    print("play/pause")

                elif cmd == "mute":
                    pag.press("volumemute")
                    print("Mute")

                elif cmd == "left_click":
                    pag.click()
                    print("Click")

                elif cmd == "open_youtube":
                    webbrowser.open("https://www.youtube.com/")
                    print("Open YouTube")

                elif cmd == "open_notepad":
                    subprocess.Popen("notepad.exe")
                    print("Open Notepad")

                elif cmd == "open_terminal":
                    subprocess.Popen(["cmd.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    print("Open Terminal")

                elif cmd == "open_browser":
                    webbrowser.open("https://www.google.com/")
                    print("Open Browser")
            
    except Exception as e:
        # エラー処理(切断)
        print("切断")

# 指定フォルダの中身をWeb配信してくれる
app.mount("/", StaticFiles(directory="static"), name="static")
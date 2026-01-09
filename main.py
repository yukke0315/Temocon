from fastapi import FastAPI, WebSocket
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

# 認証用パスワード
PASSWORD = os.getenv("TEMOCON_PASSWORD", "devpass")

# セッション管理用
SESSION_TIMEOUT = 60   # 試験用60秒

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Cのpthreと違って１スレッドでやるぽい？
    await websocket.accept()
    print("接続完了")

    # 認証用
    authenticated = False
    session_token = None
    last_active_time = None

    try:
        while True:
            # スマホからのデータ待ちすいせい
            # awaitだと、待ちの間は他の処理もできる
            data = await websocket.receive_text()

            if not authenticated:
                try:
                    msg = json.loads(data)
                    if msg.get("type") == "auth" and msg.get("password") == PASSWORD:
                        session_token = str(uuid.uuid4())
                        authenticated = True
                        last_active_time = time.time()
                        await websocket.send_text(
                            json.dumps({"type": "auth_ok", "session_token": session_token})
                        )
                    else:
                        await websocket.send_text(json.dumps({"type": "auth_ng"}))
                except:
                    await websocket.send_text(json.dumps({"type": "auth_ng"}))
                continue

            # 認証後の処理
            try:
                msg = json.loads(data)   # JSON文字列を辞書型に変換
            except:
                continue

            # tokenチェック
            if msg.get("session_token") != session_token:
                print("invalid token")
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
                    print(f"Error: {e}")

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
app.mount("/", StaticFiles(directory="static", html=True), name="static")
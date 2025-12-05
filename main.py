from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import pyautogui as pag   # os操作をするため(ツールチャンネル参照)
import json

# インスタンス作成
app = FastAPI()

# 安全装置オフ
pag.FAILSAFE = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Cのpthreと違って１スレッドでやるぽい？
    await websocket.accept()
    print("接続完了")

    try:
        while True:
            # スマホからのデータ待ちすいせい
            # awaitだと、待ちの間は他の処理もできる
            data = await websocket.receive_text()

            # 受信データが座標（JSON）かコマンドか判定
            if data.startswith("{"):
                # マウス処理
                try:
                    move_data = json.loads(data)   # JSON文字列を辞書型に変換
                    x = move_data.get("x", 0)
                    y = move_data.get("y", 0)
                    # 感度
                    sensitivity = 5.0

                    # マウス移動（相対座標）
                    pag.moveRel(x * sensitivity, y * sensitivity)

                except Exception as e:
                    print(f"Error: {e}")

            else:
                # コマンド処理
                print(f"受信: {data}")

                if data == "volume_up":
                    pag.press("volumeup")
                    print("Volume UP")

                elif data == "volume_down":
                    pag.press("volumedown")
                    print("Volume DOWN")

                elif data == "play_pause":
                    pag.press("playpause")
                    print("play/pause")

                elif data == "left_click":
                    pag.click()
                    print("Click")
            
    except Exception as e:
        # エラー処理(切断)
        print("切断")

# 指定フォルダの中身をWeb配信してくれる
app.mount("/", StaticFiles(directory="static", html=True), name="static")
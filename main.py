from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import pyautogui as pag   # os操作をするため(ツールチャンネル参照)

# インスタンス作成
app = FastAPI()

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
            print(f"受信: {data}")

            # コマンド処理
            if data == "volume_up":
                pag.press("volumeup")
                print("Volume UP")

            elif data == "volume_down":
                pag.press("volumedown")
                print("Volume DOWN")

            elif data == "play_pause":
                pag.press("playpause")
                print("play/pause")
            
    except Exception as e:
        # エラー処理(切断)
        print("切断")

# 指定フォルダの中身をWeb配信してくれる
app.mount("/", StaticFiles(directory="static", html=True), name="static")
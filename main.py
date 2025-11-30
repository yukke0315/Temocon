from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

# インスタンス作成
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Cのpthreと違って１スレッドでやるぽい？
    await websocket.accept()
    print("スマホと接続完了")

    try:
        while True:
            # スマホからのデータ待ちすいせい
            # awaitだと、待ちの間は他の処理もできる
            data = await websocket.receive_text()
            print(f"受信: {data}")

            # strcmp
            if data == "click":
                print("クリックされました")
            
    except Exception as e:
        # エラー処理(切断)
        print("接続終了")

# 指定フォルダの中身をWeb配信してくれる
app.mount("/", StaticFiles(directory="static", html=True), name="static")
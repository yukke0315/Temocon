from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import socket
import qrcode

# 分割したルーターを読み込む
from routers import auth, ws

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
    ip = get_ip()
    url = f"http://{ip}:8000"
    
    print(f"\n Scan QRcode")
    print(f" URL: {url}\n")
    
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    
    yield   # ここ以前までが起動時、以降が終了時
    
    # 終了時
    print("\n shutdown")

# インスタンス作成
app = FastAPI(lifespan=lifespan)

# 分割したルーターを登録
app.include_router(auth.router)
app.include_router(ws.router)

# 指定フォルダの中身をWeb配信してくれる
app.mount("/", StaticFiles(directory="static"), name="static")
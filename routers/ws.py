# WebSocketの処理をまとめ

from fastapi import APIRouter, WebSocket
import json
import time
from core.config import COOKIE_NAME, COOKIE_VALUE, SESSION_TIMEOUT
from core.controller import move_mouse, scroll_mouse, execute_command

router = APIRouter()

# -WS処理-
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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

            # typeによって処理分岐
            msg_type = msg.get("type")
            if msg_type == "move":
                move_mouse(msg.get("x", 0), msg.get("y", 0))
            elif msg_type == "scroll":
                scroll_mouse(msg.get("dy", 0))
            elif msg_type == "command":
                execute_command(msg.get("command"))

    except Exception as e:
        print("切断")
# 認証関連ルーター

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse, FileResponse
from core.config import PASSWORD, COOKIE_NAME, COOKIE_VALUE

router = APIRouter()

# -ログイン画面-
@router.get("/login")
async def get_login():
    return FileResponse("static/login.html")

# -ログイン処理-
@router.post("/login")
async def post_login(password: str = Form(...)):
    if password == PASSWORD:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key=COOKIE_NAME, value=COOKIE_VALUE, httponly=True)
        return response
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

# -トップ-
@router.get("/")
async def get_index(request: Request):
    cookie = request.cookies.get(COOKIE_NAME)
    if cookie != COOKIE_VALUE:
        return RedirectResponse(url="/login")
    return FileResponse("static/index.html")
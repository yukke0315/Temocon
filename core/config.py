# 環境変数やセッションの設定管理モジュール

import os
import uuid   # トークン用

# 認証用パスワードとCookie設定
PASSWORD = os.getenv("TEMOCON_PASSWORD", "devpass")
COOKIE_NAME = "temocon_session"
COOKIE_VALUE = str(uuid.uuid4())

# セッション管理用
SESSION_TIMEOUT = 60   # 試験用60秒
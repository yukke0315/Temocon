# Temocon (テモコン)

## 1. Overview
「手元」+「リモコン」が由来。
Temoconは、スマートフォンをPCの簡易コントローラーとして利用するWebアプリです。
FastAPIとWebSocketを用いて、スマホからの操作をリアルタイムにPCに反映します。

## 2. Motivation
PC操作時に物理的な距離がある場面（ベッド・プレゼン等）で、スマホをリモコンのように使えたら便利だと考え制作しました。

## 3. How to Use
1. FastAPIサーバーを起動

2. 同一ネットワーク上のスマートフォンからアクセス
起動すると、PCへの接続が始まります。  
パスワード入力が求められます。（今は仮の固定パスワード）
<img src="https://github.com/user-attachments/assets/8a589fc6-9908-4c90-8488-bf7696061246" width="30%">

3. 表示されたUIで操作
接続が完了すると、以下のようなリモート操作画面が表示されます。
- マウス操作（~~Drag~~ / Scroll / ~~Right Click~~）
- 音量操作（Vol ± / Mute）
- メディア操作（Play / Pause）
- アプリ起動（YouTube / Notepad / Terminal / Browser）
<img src="https://github.com/user-attachments/assets/59df9aa1-6e2a-4235-a6e8-50061097ddbf" width="30%">

## 4. Architecture
- フロントエンド: HTML / JavaScript（スマートフォン）
- バックエンド: Python / FastAPI
- 通信方式: WebSocket（双方向・リアルタイム）
- 認証方式: UUIDとHTTPOnly Cookieを用いたセッション管理
- OS操作: pyautogui

WebSocket経由でJSON形式のデータをやり取りする。

## 5. WebSocket Communication
- 通信の形式はJSONに統一
- 操作の種類は'type'により判別
  - `auth`: 認証
  - `move`: マウス移動
  - `scroll`: スクロール操作（縦移動量 `dy`）
  - `command`: 操作コマンド系
- タッチ（マウス）操作は相対座標として送信
- POSTリクエストでパスワードを送信し、成功時に`HttpOnly`属性のCookie（UUIDセッショントークン）を発行する
- WebSocket接続時にもCookieを検証

## 6. Implemented Features
- マウス移動（相対座標）
- スクロール
- 左クリック
- 音量操作
- 再生/停止
- ランチャー機能（ブラウザ、ターミナル、メモ帳などの起動）
- パスワード認証
- CookieとUUIDを利用したセッション認証

## 7. Limitations & Future Work
- 認証機能はシンプルなパスワード方式（要強化）->ハッシュ化
- セキュリティ対策は今後の課題
- 通信がHTTPSに未対応
- テキスト入力機能の追加
- UI / UX 改善
- 別ページ作って現在のPCの設定状態を常時可視化とか

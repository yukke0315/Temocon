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
- OS操作: pyautogui

WebSocket経由でJSON形式のデータをやり取りする。

## 5. WebSocket Communication
- 通信の形式はJSONに統一
- 操作の種類は'type'により判別
  - 'auth': 認証
  - 'move': マウス移動
  - 'command': 操作コマンド系
- タッチ（マウス）操作は相対座標として送信
- 認証後はセッショントークンを付与し、以降の操作で検証

## 6. Implemented Features
- マウス移動（相対座標）
- 左クリック
- 音量操作
- 再生/停止
- パスワード認証
- セッショントークンによる操作認証

## 7. Limitations & Future Work
- 認証機能はシンプルなパスワード方式（要強化）
- セキュリティ対策は今後の課題
- コードの責務分離改善予定
- 通信がHTTPSに未対応
- UI / UX 改善

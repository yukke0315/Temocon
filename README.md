# Temocon (テモコン)

## 1. Overview
「手元」+「リモコン」が由来。
Temoconは、スマートフォンをPCの簡易コントローラーとして利用するWebアプリです。
FastAPIとWebSocketを用いて、スマホからの操作をリアルタイムにPCに反映します。

## 2. Motivation
PC操作時に物理的な距離がある場面（ベッド・プレゼン等）で、スマホをリモコンのように使えたら便利だと考え制作しました。

## 3. Architecture
- フロントエンド: HTML / JavaScript（スマートフォン）
- バックエンド: Python / FastAPI
- 通信方式: WebSocket（双方向・リアルタイム）
- OS操作: pyautogui

WebSocket経由でJSON形式のデータをやり取りする。

## 4. WebSocket Communication
- 通信の形式はJSONに統一
- 操作の種類は'type'参照
  - 'auth': 認証
  - 'move': マウス移動
  - 'command': 操作コマンド系
- タッチ（マウス）操作は相対座標として送信
- 認証後はセッショントークンを付与し、以降の操作で検証

## 5. Implemented Features
- マウス移動（相対座標）
- 左クリック
- 音量操作
- 再生/停止
- パスワード認証
- セッショントークンによる操作認証

## 6. Limitations & Future Work
- 認証機能はシンプルなパスワード方式（要強化）
- セキュリティ対策は今後の課題
- コードの責務分離改善予定
- 通信がHTTPSに未対応
- UI / UX 改善

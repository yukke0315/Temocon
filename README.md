# Temocon (テモコン)

## 1. Overview
「手元」+「リモコン」が由来。
Temoconは、スマートフォンをPCの簡易コントローラーとして利用するWebアプリです。
FastAPIとWebSocketを用いて、スマホからの操作をリアルタイムにPCに反映します。

## 2. Motivation
PC操作時に物理的な距離がある場面（ベッド・プレゼン等）で、スマホをリモコンのように使えたら便利だと考え制作しました。

## 3. Architecture
- フロントエンド: HTML / JavaScript（スマートフォン）
- バックエンド: FastAPI（WebSocket）
- 通信方式: WebSocket（双方向・リアルタイム）

## 4. WebSocket Communication
- タッチ操作は相対座標として送信
- JSONデータとコマンド文字列を分けて処理

## 5. Implemented Features
- マウス移動（相対座標）
- 左クリック
- 音量操作
- 再生/停止

## 6. Limitations & Future Work
- 認証機能は未実装（ローカル利用前提）
- セキュリティ対策は今後の課題
- コードの責務分離改善予定

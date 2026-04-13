# OS操作のまとめ

import pyautogui as pag   # os操作をするため(ツールチャンネル参照)
import webbrowser   # ブラウザ起動用
import subprocess   # アプリ起動用

# 安全装置オフ
pag.FAILSAFE = False
pag.PAUSE = 0   # デフォの0.1s待機を無効に(カクカク解消)

def move_mouse(x: float, y: float, sensitivity: float = 5.0):
    try:
        # マウス移動（相対座標）
        pag.moveRel(x * sensitivity, y * sensitivity)
    except Exception as e:
        print(f"Move Error: {e}")

def scroll_mouse(dy: float, scroll_sensitivity: float = 4.0):
    try:
        # 指を下（dy負）で下スクロール
        pag.scroll(int(dy * scroll_sensitivity))
    except Exception as e:
        print(f"Scroll Error: {e}")

def execute_command(cmd: str):
    print(f"cmd: {cmd}")
    try:
        # コマンド処理
        if cmd == "volume_up":
            pag.press("volumeup")
            print("Volume UP")
        elif cmd == "volume_down":
            pag.press("volumedown")
            print("Volume DOWN")
        elif cmd == "play_pause":
            pag.press("playpause")
            print("play/pause")
        elif cmd == "mute":
            pag.press("volumemute")
            print("Mute")
        elif cmd == "left_click":
            pag.click()
            print("Click")
        elif cmd == "open_youtube":
            webbrowser.open("https://www.youtube.com/")
            print("Open YouTube")
        elif cmd == "open_notepad":
            subprocess.Popen("notepad.exe")
            print("Open Notepad")
        elif cmd == "open_terminal":
            subprocess.Popen(["cmd.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print("Open Terminal")
        elif cmd == "open_browser":
            webbrowser.open("https://www.google.com/")
            print("Open Browser")
    except Exception as e:
        print(f"Command Error: {e}")

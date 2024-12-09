import tkinter as tk
import pyautogui
import threading
import time
import keyboard

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("매크로 애플리케이션")
        self.is_running = False

        # 시작 버튼
        self.start_button = tk.Button(root, text="시작", command=self.start_macro)
        self.start_button.pack(pady=20)

        # 중지 버튼
        self.stop_button = tk.Button(root, text="중지", command=self.stop_macro)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=20)

    def start_macro(self):
        self.is_running = True
        self.status_label.config(text="매크로가 실행 중입니다...")
        threading.Thread(target=self.run_macro).start()  # 매크로를 별도의 스레드에서 실행

    def stop_macro(self):
        self.is_running = False
        self.status_label.config(text="매크로가 중지되었습니다.")

    def run_macro(self):
        # 대기 시간
        time.sleep(1)  # 3초 후 시작

        while self.is_running:
            # (941, 80) 위치로 마우스 이동 및 클릭
            pyautogui.moveTo(757, 219, duration=0.1)
            pyautogui.click()
            time.sleep(1)

            # 텍스트 입력
            pyautogui.typewrite("www.naver.com", interval=0.1)
            pyautogui.press('enter')  # 엔터키 입력
            time.sleep(1)

            pyautogui.moveTo(1406, 915, duration=0.1)
            pyautogui.click()   
            time.sleep(1)
            
            pyautogui.moveTo(779, 604, duration=0.1)
            pyautogui.click()
            time.sleep(1)
            
            pyautogui.typewrite("ckswls", interval=0.1)
            pyautogui.press('enter')  # 엔터키 입력
            # break  # 한 번만 실행하도록 break

        self.status_label.config(text="매크로가 완료되었습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)

    # 'q' 키를 눌러 중지할 수 있도록 설정
    keyboard.add_hotkey('q', app.stop_macro)

    root.mainloop()

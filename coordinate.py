import tkinter as tk
import pyautogui
import threading
import time

class HelloWorldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("안녕하세요 애플리케이션")

        # 텍스트 라벨
        self.text_label = tk.Label(root, text="안녕하세요", font=("Helvetica", 24))
        self.text_label.pack(pady=20)

        # 마우스 좌표 라벨
        self.position_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.position_label.pack(pady=20)

        # 시작 버튼
        self.start_button = tk.Button(root, text="좌표 보기 시작", command=self.start_tracking)
        self.start_button.pack(pady=20)

        # 중지 버튼
        self.stop_button = tk.Button(root, text="좌표 보기 중지", command=self.stop_tracking)
        self.stop_button.pack(pady=20)

        self.is_running = False

    def start_tracking(self):
        self.is_running = True
        self.update_position()  # 좌표 업데이트 시작

    def stop_tracking(self):
        self.is_running = False
        self.position_label.config(text="좌표 보기 중지됨")

    def update_position(self):
        if self.is_running:
            x, y = pyautogui.position()  # 현재 마우스 좌표 가져오기
            self.position_label.config(text=f"현재 마우스 좌표: ({x}, {y})")
            self.root.after(100, self.update_position)  # 100ms 후에 다시 호출

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()

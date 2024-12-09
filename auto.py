# import tkinter as tk
# import pyautogui
# import threading
# import time
# import sqlite3
# import keyboard

# class MacroApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("매크로 애플리케이션")
#         self.is_running = False
#         self.data = []  # 데이터 저장

#         # 시작 버튼
#         self.start_button = tk.Button(root, text="시작", command=self.start_macro)
#         self.start_button.pack(pady=20)

#         # 중지 버튼
#         self.stop_button = tk.Button(root, text="중지", command=self.stop_macro)
#         self.stop_button.pack(pady=20)

#         self.status_label = tk.Label(root, text="")
#         self.status_label.pack(pady=20)

#         self.load_data()  # 데이터 로드

#     def load_data(self):
#         # 데이터베이스에서 데이터 로드
#         conn = sqlite3.connect('business_data.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, region, store_name FROM business_data ORDER BY id")
#         self.data = cursor.fetchall()  # ID, region, store_name을 가져옴
#         conn.close()

#     def start_macro(self):
#         self.is_running = True
#         self.status_label.config(text="매크로가 실행 중입니다...")
#         threading.Thread(target=self.run_macro).start()  # 매크로를 별도의 스레드에서 실행

#     def stop_macro(self):
#         self.is_running = False
#         self.status_label.config(text="매크로가 중지되었습니다.")

#     def run_macro(self):
#         time.sleep(1)  # 1초 후 시작

#         for item in self.data:
#             if not self.is_running:  # 매크로 중지 확인
#                 break

#             id, region, store_name = item

#             # region 클릭
#             pyautogui.moveTo(757, 219, duration=0.1)  # region 클릭 위치
#             pyautogui.click()
#             time.sleep(1)

#             # region 입력
#             pyautogui.typewrite(region, interval=0.1)  # region 입력
#             pyautogui.press('enter')  # 엔터키 입력
#             time.sleep(1)

#             # store_name 클릭
#             pyautogui.moveTo(1406, 915, duration=0.1)  # store_name 클릭 위치
#             pyautogui.click()
#             time.sleep(1)

#             # store_name 입력
#             pyautogui.typewrite(store_name, interval=0.1)  # store_name 입력
#             pyautogui.press('enter')  # 엔터키 입력
#             time.sleep(1)

#             # 이미지 인식
#             image_path = 'path_to_your_image.png'  # 확인할 이미지 경로
#             location = pyautogui.locateOnScreen(image_path, confidence=0.8)  # 이미지 찾기

#             # 이미지 발견 여부에 따라 T 또는 F 저장
#             conn = sqlite3.connect('business_data.db')
#             cursor = conn.cursor()
#             if location:
#                 cursor.execute("UPDATE business_data SET open = 'T' WHERE id = ?", (id,))
#                 self.status_label.config(text="이미지 발견! 다음 작업으로 진행합니다.")
#             else:
#                 cursor.execute("UPDATE business_data SET open = 'F' WHERE id = ?", (id,))
#                 self.status_label.config(text="이미지 없음. 다음 작업으로 진행합니다.")
#             conn.commit()
#             conn.close()

#             time.sleep(1)  # 다음 작업 전 대기

#         self.status_label.config(text="매크로가 완료되었습니다.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MacroApp(root)

#     # 'q' 키를 눌러 중지할 수 있도록 설정
#     keyboard.add_hotkey('q', app.stop_macro)

#     root.mainloop()

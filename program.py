import pandas as pd
import sqlite3
import tkinter as tk
import pyautogui
import threading
import time
import keyboard
import os

# 1단계: 엑셀 파일을 데이터베이스에 저장
def save_to_db(excel_file):
    # 데이터베이스 연결
    conn = sqlite3.connect('business_data.db')
    cursor = conn.cursor()

    # 데이터베이스 테이블 생성 (이미 존재하는 경우에는 건너뜁니다)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT,
        registration_number TEXT,
        store_name TEXT,
        detailed_area TEXT,
        open TEXT  -- open 필드 추가
    )
    ''')

    # 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # 데이터프레임을 SQLite 데이터베이스에 저장 (덮어쓰지 않고 추가)
    df.to_sql('business_data', conn, if_exists='append', index=False)

    # 연결 종료
    conn.commit()
    conn.close()

    print("엑셀 파일이 데이터베이스에 저장되었습니다.")

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("매크로 애플리케이션")
        self.is_running = False
        self.data = []  # 데이터 저장
        self.current_index = 0  # 현재 진행 중인 인덱스
        self.excel_file_name = None  # 진행 상태를 저장할 엑셀 파일 이름

        # 시작 버튼
        self.start_button = tk.Button(root, text="시작", command=self.start_macro)
        self.start_button.pack(pady=20)

        # 중지 버튼
        self.stop_button = tk.Button(root, text="중지", command=self.stop_macro)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=20)

        self.load_data()  # 데이터 로드

    def load_data(self):
        # 데이터베이스에서 데이터 로드
        conn = sqlite3.connect('business_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, region, store_name FROM business_data ORDER BY id")
        self.data = cursor.fetchall()  # ID, region, store_name을 가져옴
        conn.close()

    def start_macro(self):
        self.is_running = True
        self.status_label.config(text="매크로가 실행 중입니다...")
        threading.Thread(target=self.run_macro).start()  # 매크로를 별도의 스레드에서 실행

    def stop_macro(self):
        self.is_running = False
        self.status_label.config(text="매크로가 중지되었습니다.")
        self.save_progress_to_excel()  # 현재 진행 상태를 엑셀로 저장

    def save_progress_to_excel(self):
        conn = sqlite3.connect('business_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM business_data WHERE id <= ?", (self.current_index,))
        data = cursor.fetchall()  # 현재까지 처리한 데이터 가져오기
        conn.close()

        # 데이터프레임으로 변환
        df = pd.DataFrame(data, columns=['id', 'region', 'registration_number', 'store_name', 'detailed_area', 'open'])

        # 진행 상태를 저장할 엑셀 파일 이름 설정
        if self.excel_file_name is None:
            self.excel_file_name = f"progress_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(self.excel_file_name, index=False)  # 처음 저장할 때 새로 생성
            print(f"현재 진행 상태가 {self.excel_file_name}로 저장되었습니다.")
        else:
            # 기존 파일에 이어서 작성
            with pd.ExcelWriter(self.excel_file_name, mode='a', engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False, sheet_name='Progress')  # 헤더 제외하고 추가
            print(f"현재 진행 상태가 {self.excel_file_name}로 이어서 저장되었습니다.")

    def run_macro(self):
        time.sleep(1)  # 1초 후 시작

        # 현재 인덱스에서 시작
        for index in range(self.current_index, len(self.data)):
            if not self.is_running:  # 매크로 중지 확인
                self.current_index = index  # 현재 인덱스 저장
                break

            id, region, store_name = self.data[index]

            # region 클릭
            pyautogui.moveTo(757, 219, duration=0.1)  # region 클릭 위치
            pyautogui.click()
            time.sleep(1)

            # region 입력
            pyautogui.typewrite(region, interval=0.1)  # region 입력
            pyautogui.press('enter')  # 엔터키 입력
            time.sleep(1)

            # store_name 클릭
            pyautogui.moveTo(1406, 915, duration=0.1)  # store_name 클릭 위치
            pyautogui.click()
            time.sleep(1)

            # store_name 입력
            pyautogui.typewrite(store_name, interval=0.1)  # store_name 입력
            pyautogui.press('enter')  # 엔터키 입력
            time.sleep(1)

            # 이미지 인식
            image_path_1 = 'path_to_your_first_image.png'  # 첫 번째 이미지 경로
            image_path_2 = 'path_to_your_second_image.png'  # 두 번째 이미지 경로
            location_1 = pyautogui.locateOnScreen(image_path_1, confidence=0.8)  # 첫 번째 이미지 찾기
            location_2 = pyautogui.locateOnScreen(image_path_2, confidence=0.8)  # 두 번째 이미지 찾기

            # 이미지 발견 여부에 따라 T 또는 F 저장
            conn = sqlite3.connect('business_data.db')
            cursor = conn.cursor()
            if location_1 or location_2:  # 두 이미지 중 하나라도 발견되면 'T'
                cursor.execute("UPDATE business_data SET open = 'T' WHERE id = ?", (id,))
                self.status_label.config(text="이미지 발견! 다음 작업으로 진행합니다.")
            else:
                cursor.execute("UPDATE business_data SET open = 'F' WHERE id = ?", (id,))
                self.status_label.config(text="이미지 없음. 다음 작업으로 진행합니다.")
            conn.commit()
            conn.close()

            time.sleep(1)  # 다음 작업 전 대기

        # 모든 작업을 마친 후 인덱스를 초기화
        if self.is_running:
            self.current_index = 0  # 모든 작업이 완료되면 인덱스를 초기화
            self.status_label.config(text="매크로가 완료되었습니다.")

if __name__ == "__main__":
    # 엑셀 파일 경로 설정
    excel_file = 'excel/test.xlsx'
    save_to_db(excel_file)  # 데이터베이스에 엑셀 데이터 저장

    root = tk.Tk()
    app = MacroApp(root)

    # 'q' 키를 눌러 중지할 수 있도록 설정
    keyboard.add_hotkey('q', app.stop_macro)

    root.mainloop()

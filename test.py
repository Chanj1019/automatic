import pandas as pd

# 데이터만 포함된 리스트 생성
data = [
    ['서울', '123456','가게1',  '강남구',''],
    ['부산', '654321','가게2',  '해운대구',''],
    ['인천', '414344','가게3',  '인천시','']
]

# 데이터프레임 생성 (열 이름 없음)
df = pd.DataFrame(data)

# Excel 파일로 저장 (열 이름 없이)
df.to_excel("test.xlsx", index=False, header=False)
print("test.xlsx 파일이 생성되었습니다.")

#pyinstaller --onefile --noconsole --icon=your_icon.ico your_script.py

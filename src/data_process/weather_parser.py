import pandas as pd
import re
from src.config import DATA_RAW, DATA_INTERIM

folder_path = DATA_RAW / 'weather'
all_files = list(folder_path.glob('*.csv'))  # 取得資料夾下所有CSV檔

dfs = []  # 最後的大 df

for file_path in all_files:
    df = pd.read_csv(file_path, na_values=['/', '--'])
    
    filename = file_path.name
    stn_id = re.search(r'^([A-Z0-9]+)', filename).group(1)
    year_date = re.search(r'(\d{4}-\d{2})', filename).group(1)

    df['觀測日期'] = year_date + '-' + df['觀測時間(day)']
    df['氣象站ID'] = stn_id
    
    # 先轉觀測日期型別，才能計算季節
    df['觀測日期'] = pd.to_datetime(df['觀測日期'], errors='coerce')

    # 新增季節欄位
    def month_to_season(month):
        if pd.isna(month):
            return None
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        elif month in [12, 1, 2]:
            return 'winter'
        else:
            return None
    df['季節'] = df['觀測日期'].dt.month.apply(month_to_season)

    df = df[['觀測日期', '氣象站ID', '季節', "氣溫(℃)", "相對溼度(%)", "風速(m/s)", "風向(360degree)", "降水量(mm)"]]

    df = df.drop(index=0).reset_index(drop=True)  # drop第一筆英文標頭

    # 轉型別
    float_cols = ['氣溫(℃)', '風速(m/s)', '降水量(mm)']
    int_cols = ['相對溼度(%)', '風向(360degree)']
    df[float_cols] = df[float_cols].astype(float)
    df[int_cols] = df[int_cols].astype('Int64')

    dfs.append(df)  # 加進大 df

if dfs:
    all_data = pd.concat(dfs, ignore_index=True)

    # 將欄位名稱改成英文 不然怕哪裡又報錯
    all_data = all_data.rename(columns={
        '觀測日期': 'date',
        '氣象站ID': 'station_id',
        '季節': 'season',
        '氣溫(℃)': 'temperature',
        '相對溼度(%)': 'humidity',
        '風速(m/s)': 'wind_speed',
        '風向(360degree)': 'wind_direction',
        '降水量(mm)': 'rainfall'
    })

    # interim 路徑 (使用 config.py 的 DATA_INTERIM)
    interim_path = DATA_INTERIM / 'weather' / 'weather.csv'
    all_data.to_csv(interim_path, index=False, encoding='utf-8-sig')

    print(f"合併後資料存到：{interim_path.resolve()}")
else:
    print("錯誤!!!!!!!!!!!!!!!!!!!")

import pandas as pd
from src.config import DATA_INTERIM, SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine

def weather_to_sql():
    df = pd.read_csv(DATA_INTERIM / 'weather' / 'weather.csv')
    df = df.astype(object).where(pd.notnull(df), None) # NaN轉None mysql才看得懂

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.raw_connection()

    columns = df.columns.to_list() # 你要寫進 DB 的欄位

    # 動態產生sql query的值 不寫死 改欄位就不用回來改
    placeholders = ", ".join(["%s"] * len(columns))
    columns_sql = ", ".join([f"`{col}`" for col in columns])    
    exclude_cols = ['date', 'station_id', 'id'] # 不該更新的欄位    
    update_columns = [col for col in columns if col not in exclude_cols] # 自動產生要更新的欄位

    update_sql = ", ".join([f"`{col}`=VALUES(`{col}`)" for col in update_columns])

    insert_sql = f"""
    INSERT INTO weather ({columns_sql})
    VALUES ({placeholders})
    ON DUPLICATE KEY UPDATE {update_sql}
    """

    data = [tuple(row[col] for col in columns) for _, row in df.iterrows()]

    with connection.cursor() as cursor:
        cursor.executemany(insert_sql, data)

    connection.commit()
    connection.close()
    print(f"成功 upsert {len(data)} 筆天氣資料！")


def gpx_to_sql():
    df = pd.read_csv(DATA_INTERIM / 'gpx' / '桃山gpx.csv')
    df = df.rename(columns={
    "日期": "date",
    "上傳此GPX用戶": "uploader",
    "總距離水平(km)": "total_distance_km",
    "總爬升高度(m)": "total_ascent_m",
    "總下降高度(m)": "total_descent_m",
    "總花費時間(HH:MM:SS)": "total_duration",
    "起始到折返點時間(HH:MM:SS)": "ascent_time",
    "折返到結束時間(HH:MM:SS)": "descent_time",
    "上山水平速度(km/h)": "ascent_speed_kmh",
    "上山垂直速度(m/h)": "ascent_speed_vmph",
    "下山水平速度(km/h)": "descent_speed_kmh",
    "下山垂直速度(m/h)": "descent_speed_vmph",
    "全程平均水平速度(km/h)": "avg_speed_kmh",
    "全程平均垂直速度(m/h)": "avg_speed_vmph",
    "最高海拔(m)": "max_elevation_m",
    "最低海拔(m)": "min_elevation_m",
    })
    df = df.astype(object).where(pd.notnull(df), None)

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.raw_connection()

    columns = df.columns.to_list() # 欄位

    # 動態產生sql query的值 不寫死 改欄位就不用回來改
    placeholders = ", ".join(["%s"] * len(columns))
    columns_sql = ", ".join([f"`{col}`" for col in columns])    
    exclude_cols = [] # 不該更新的欄位, 唯一鍵    
    update_columns = [col for col in columns if col not in exclude_cols] # 自動產生要更新的欄位

    update_sql = ", ".join([f"`{col}`=VALUES(`{col}`)" for col in update_columns])

    insert_sql = f"""
    INSERT INTO gpx ({columns_sql})
    VALUES ({placeholders})
    ON DUPLICATE KEY UPDATE {update_sql}
    """

    data = [tuple(row[col] for col in columns) for _, row in df.iterrows()]

    with connection.cursor() as cursor:
        cursor.executemany(insert_sql, data)

    connection.commit()
    connection.close()

    print(f"成功 upsert {len(df)}筆登山資料進資料庫！")

weather_to_sql()
gpx_to_sql()
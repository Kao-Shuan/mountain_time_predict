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
    df = pd.read_csv(DATA_INTERIM / 'gpx' / 'merged_taoshan_data.csv')

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

if __name__ == "__main__":
    weather_to_sql()
    gpx_to_sql()
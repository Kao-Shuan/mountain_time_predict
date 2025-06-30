import pandas as pd
from src.config import DATA_INTERIM, SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine

df = pd.read_csv(DATA_INTERIM / 'weather' / 'weather.csv')

engine = create_engine(SQLALCHEMY_DATABASE_URI)

df.to_sql(
    name='weather',        # 對應 SQL 中的table名
    con=engine,
    if_exists='append',    # 已存在table就append
    index=False            # 不把 DataFrame index 當欄位寫入
)

print(f"成功寫入{len(df)}筆資料進資料庫！")
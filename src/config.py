from pathlib import Path
from dotenv import load_dotenv
import os
import urllib.parse

# --- 讀取 .env ---
load_dotenv()

# 專案根目錄：config.py 請在 src/ 下
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# data資料夾
DATA_DIR = PROJECT_ROOT / 'data'
DATA_RAW = DATA_DIR / 'raw'
DATA_INTERIM = DATA_DIR / 'interim'
DATA_PROCESSED = DATA_DIR / 'processed'
DATA_UPLOAD = DATA_DIR / 'upload'

# Notebook 資料夾
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

# 建立必要資料夾（首次執行會自動創建）
for p in [DATA_RAW, DATA_INTERIM, DATA_PROCESSED, DATA_UPLOAD]:
    p.mkdir(parents=True, exist_ok=True)

# --- 資料庫連線設定 ---
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
password_escaped = urllib.parse.quote(DB_PASSWORD) # @ 放進URI會誤認 要跳脫
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "mountain_db")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{password_escaped}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

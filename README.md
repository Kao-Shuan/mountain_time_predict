```
MOUNTAIN/
├── data/                         # 資料夾
│   ├── interim/                  # 中間處理資料 (準備寫進DB的)
│   ├── processed/                # 最終處理後資料 (ml建模前的最終dataframe?)
│   └── raw/                      # 原始資料 (CSV, GPX ...)
│
├── notebook/                     # JupyterNotebook 測試跟分析
│
├── sql/                          # SQL 初始化腳本
│   └── init.sql
│
├── src/                          # Python 原始程式碼
│   ├── __init__.py
│   │
│   ├── config.py                 # 存重要變數 路徑、sql連線設定
│   │
│   ├── data_process/             # for 資料處理
│   │   ├── to_sql.py             # 把interim的csv寫進DB
│   │   └── weather_parser.py     # 天氣raw data 整理寫進interim
│   │
│   └── scraping/                 # for 爬蟲
│       └── scrape_codis.py       # 爬天氣月報表
│
├── .env                          # 環境變數設定檔 密碼、金鑰啥的
└── README.md                     
```


## 如何執行
在專案根目錄執行任意東西，例如：
python -m src.data_process.weather_parser

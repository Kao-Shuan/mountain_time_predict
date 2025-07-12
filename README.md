```
mountain_time_predict/
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
│   │   ├── to_sql.py             # 把 interim 的 CSV 寫進 DB
│   │   ├── gpx_parser.py         # GPX 解析腳本
│   │   ├── html_parser.py        # HTML 解析腳本
│   │   ├── merge_gpx_html.py     # 合併 GPX 與 HTML
│   │   └── weather_parser.py     # 天氣 raw data 整理寫進 interim
│   │
│   └── scraping/                 # for 爬蟲
│       ├── scrape_hikingnote_gpx.py   # 爬 HikingNote GPX
│       ├── scrape_hikingnote_html.py  # 爬 HikingNote 頁面
│       ├── scrape_codis.py           # 爬天氣月報表
│       └── scrape_stations.py           # 爬氣象站資訊 靜態表/一次性
│
├── .env                          # 環境變數設定檔 密碼、金鑰啥的
└── README.md                     
```

## 如何執行 py 檔
在專案根目錄執行，例如：

```bash
python -m src.data_process.weather_parser
```

## 資料流示意圖

```mermaid
graph TD
    subgraph A [流程A: 處理GPX檔案]
        direction LR
        A1["scrape_hikingnote_gpx.py<br>(爬蟲腳本)"] -- "1. 爬取GPX檔" --> A_manual{"手動放置<br>GPX檔案"}
        A_manual --> A2["/data/raw/gpx/<br>(資料夾)"]
        A2 --> A3["gpx_parser.py<br>(解析腳本)"]
        A3 -- "2. 解析GPX" --> A4["data/interim/gpx/gpx_analysis_results.csv"]
    end

    subgraph B [流程B: 處理HTML頁面資訊]
        direction LR
        B1["scrape_hikingnote_html.py<br>(爬蟲腳本)"] -- "1. 爬取頁面" --> B2["data/raw/html/data_from_HTML_Taoshan.json"]
        B2 --> B3["html_parser.py<br>(解析腳本)"]
        B3 -- "2. 解析JSON轉CSV" --> B4["data/interim/gpx/webscrapping4HTML_Taoshan_en.csv"]
    end

    subgraph C [流程C: 合併爬蟲資料]
        A4 -- "以 end_date, total_time<br>為合併鍵" --> C1["merge_gpx_html.py<br>(合併腳本)"]
        B4 -- "INNER JOIN" --> C1
        C1 --> C2["data/interim/gpx/merged_taoshan_data.csv"]
    end

    subgraph D [流程D: 處理天氣資料]
        D1["scrape_codis.py<br>(爬蟲腳本)"] -- "下載天氣CSV" --> D2["data/raw/weather/<br>(資料夾)"]
        D2 --> D3["weather_parser.py<br>(解析腳本)"]
        D3 --> D4["data/interim/weather/weather.csv"]
    end

    subgraph E [流程E: 匯入資料庫]
        C2 --> E1["to_sql.py"]
        D4 --> E1
        E1 --> E_final["MySQL Database"]
    end
```
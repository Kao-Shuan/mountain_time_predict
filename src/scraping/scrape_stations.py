import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
取得氣象站ID、經緯度、海拔的靜態表
用在算登山路線最靠近的氣象站
這是一次性的靜態表
"""

def get_stn_info():
    url = "https://hdps.cwa.gov.tw/static/state.html"
    res = requests.get(url, verify=False)
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, "html.parser")

    # 抓第一個表格 (現存測站)
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            data.append(cols)

    columns = ["站號", "站名", "站種", "海拔高度(m)", "經度", "緯度", "城市", "地址", "資料起始日期", "撤站日期", "備註", "原站號", "新站號"]# ✅ 請依實際內容修改

    # 建立 DataFrame 並儲存
    df = pd.DataFrame(data, columns=columns) 
    df = df[df['站號'].str.match(r'^(C0|46)')] # 只要 有人 跟 無人氣象站
    df.to_csv(r"data\interim\staions\stations.csv", index=False, encoding="utf-8-sig")
    print("✅ 轉存完成，共筆數：", len(df))

if __name__ == "__name__":
    get_stn_info()

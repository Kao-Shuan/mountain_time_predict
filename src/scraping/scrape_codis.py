import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import DATA_RAW

def get_station_available_date_range(stn_id: str):
    """
    回傳指定測站(stn_id)在CODiS上可選取的最早和最晚年月 (YYYY/MM)。
    """
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new") # 不開瀏覽器
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://codis.cwa.gov.tw/StationData")
    time.sleep(1)

    # 選擇自動氣象站
    stn_type = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='form-check' and .//input[@value='auto_C0']]"))
    )
    stn_type.click()
    time.sleep(3)

    # 輸入測站代號
    stn_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='form-control']")))
    stn_input.clear()
    stn_input.send_keys(stn_id)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'leaflet-interactive')]"))).click()
    time.sleep(3)

    # 點地圖標記圖釘
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'leaflet-interactive')]"))).click()
    time.sleep(3)

    # 點擊 '資料圖表展示' 按鈕
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'show_stn_tool') and contains(@data-stn_id, '{stn_id}')]"))).click()
    time.sleep(3)

    # 點擊月報表
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main_content']/section[2]/div/div/aside/div[2]/div[2]/div[2]/div"))).click()

    # 點擊日期選單
    datetime_panel = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/section[2]/div/div/section/div[6]/div[1]/div[1]/label/div/div[2]/div[1]'))
    )
    datetime_panel.click()

    # 展開年份選擇器
    year_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'vdatetime-popup__year')]")))
    year_selector.click()

    # 抓可用年份
    year_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'vdatetime-year-picker__item') and not(contains(@class, 'disabled'))]"))
    )
    all_years = sorted([int(el.text.strip()) for el in year_elements if el.text.strip().isdigit()])
    earliest_year, latest_year = all_years[0], all_years[-1]

    # 點選最早年份 → 抓該年可用月份
    earliest_year_el = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'vdatetime-year-picker__item') and contains(text(), '{earliest_year}')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", earliest_year_el)
    earliest_year_el.click()

    month_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'vdatetime-month-picker__item') and not(contains(@class, 'disabled'))]"))
    )
    earliest_month = int(month_elements[0].text.strip().replace('月', ''))

    # 點選最新年份 → 抓該年可用月份
    datetime_panel.click()
    year_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'vdatetime-popup__year')]")))
    year_selector.click()

    latest_year_el = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'vdatetime-year-picker__item') and contains(text(), '{latest_year}')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_year_el)
    latest_year_el.click()

    month_elements_latest = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'vdatetime-month-picker__item') and not(contains(@class, 'disabled'))]"))
    )
    latest_month = int(month_elements_latest[-1].text.strip().replace('月', ''))

    driver.quit()

    start = f"{earliest_year}/{earliest_month:02d}"
    end = f"{latest_year}/{latest_month:02d}"
    print(f"氣象站 {stn_id} 可用範圍: {start} ~ {end}")
    return start, end


def download_weather_data(stn_id: str, download_dir=DATA_RAW / 'weather'):
    """
    下載指定氣象站ID(stn_id)從 start 到 end 的月報表資料。
    start, end 格式: 'YYYY/MM' 例如 '2016/04'
    """
    os.makedirs(download_dir, exist_ok=True)
    print(f"檔案將下載到: {download_dir}")

    # 獲取氣象站可用的日期範圍
    print(f"正在獲取氣象站 {stn_id} 的可用日期範圍...")
    start, end = get_station_available_date_range(stn_id)

    if not start or not end:
        print(f"無法獲取氣象站 {stn_id} 的可用日期範圍，無法繼續下載。")
        return

    print(f"確認下載範圍: 從 {start} 到 {end}")

    # 設定 Selenium
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # 日期處理
    start_dt = datetime.strptime(start, "%Y/%m")
    end_dt = datetime.strptime(end, "%Y/%m")

    driver.get("https://codis.cwa.gov.tw/StationData")

    # 選擇自動氣象站 雨量站跟農業站大概沒用 不勾
    stn_type = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='form-check' and .//input[@value='auto_C0']]"))
    )
    stn_type.click()

    # 輸入氣象站ID
    stn_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='form-control']")))
    stn_input.clear()
    stn_input.send_keys(stn_id)
    time.sleep(2)

    # 點地圖標記圖釘
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'leaflet-interactive')]"))).click()
    time.sleep(2)

    # 點擊 '資料圖表展示' 按鈕
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'show_stn_tool') and contains(@data-stn_id, '{stn_id}')]"))).click()
    time.sleep(2)

    # 點月報表
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main_content']/section[2]/div/div/aside/div[2]/div[2]/div[2]/div"))).click()
    time.sleep(2)

    current_dt = start_dt
    while current_dt <= end_dt:
        year, month = current_dt.year, current_dt.month

        # 開啟日期選單
        datetime_panel = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/section[2]/div/div/section/div[6]/div[1]/div[1]/label/div/div[2]/div[1]'))
        )
        datetime_panel.click()
        time.sleep(1)

        # 點擊年份
        year_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'vdatetime-popup__year')]")))
        year_selector.click()
        target_year = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'vdatetime-year-picker__item') and contains(text(), '{year}')]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_year)
        target_year.click()

        # 點擊月份
        target_month = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'vdatetime-month-picker__item') and contains(text(), '{month}月')]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_month)
        target_month.click()

        # 點擊下載
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main_content']/section[2]/div/div/section/div[6]/div[1]/div[2]/div")))
        download_btn.click()
        print(f"下載 {stn_id}-{year}-{month:02d} 中...")
        time.sleep(5)  # 等待檔案下載
        
        # 到下個月
        next_month = (current_dt.month % 12) + 1
        next_year = current_dt.year + (current_dt.month // 12)
        current_dt = datetime(next_year, next_month, 1)

    driver.quit()
    print("瀏覽器已關閉。")


download_weather_data('C0F9Y0') # 桃山 

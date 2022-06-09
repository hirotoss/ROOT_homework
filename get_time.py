# -*- coding: utf-8 -*-
#-----------------------------------
#参考にした記事
#https://note.com/shakeshake108/n/nd76dea39d2a0

#chrome driver
DriverDir = "/usr/local/bin/chromedriver"
LogFileName = "/mnt/c/Users/philo/OneDrive/M1S/ROOT/homework/log.txt"
URLFileName = "/mnt/c/Users/philo/OneDrive/M1S/ROOT/homework/link.csv"

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.common.exceptions as exceptions
import json

def main():    
    #WebDriver関連のオプション指定
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-erroes') #証明書エラー回避
    options.add_argument('--headless') #ブラウザ画面を表示させない            
    
    #ブラウザ立ち上げ
    driver = webdriver.Chrome(DriverDir, options = options, desired_capabilities = caps)
    driver.implicitly_wait(2)

    #タイムアウトを10秒に設定
    driver.set_page_load_timeout(10)

    read_file = open(URLFileName, 'r', encoding='utf_8')
    write_file = open(LogFileName, 'a', encoding='utf_8')

    #各URLへアクセス
    for row in read_file:
        [i, name, url] = row.strip().split(',')
        i = int(i)

        print(f'i = {i}, name = {name}, URL = {url}')
        try:
            #URLアクセス
            driver.get(url)
        except exceptions.WebDriverException:
            print("unreachable error")
            continue
        except exceptions.TimeoutException:
            print("timeout error")
            continue

        #JSONのフォーマット
        netLog = driver.get_log("performance")
        
        #JSONのperformanceを抽出
        events = [json.loads(entry['message'])['message'] for entry in netLog]

        #"method"名にNetwork.responseReceived含むものを抽出
        events = [event for event in events if 'Network.respons' in event['method']]

        #各performanceからタイムスタンプとURLを抽出
        detected_url = []
        timestamp_url = []
        for item in events:
                if "response" in item["params"]:
                    if "url" in item["params"]["response"]:
                        #詳細のアクセスURL
                        detected_url.append(item["params"]["response"]["url"])
                        #timestamp
                        timestamp_url.append(item["params"]["timestamp"])

        #詳細のアクセスURL数
        n = len(detected_url)

        #アクセストータル時間
        totaltime = float(timestamp_url[n - 1]) - float(timestamp_url[0])

        #表示
        print('total time：', totaltime)

        #書き込み
        write_file.write(f'{totaltime},{name},{url}\n')

    write_file.close()
    read_file.close()
    #ブラウザ閉じる
    driver.quit()

if __name__ == "__main__":
    main()
# 【コード付き】Selenium×Pythonの使い方！Chromeブラウザを自動操作してみようー！
# https://toukei-lab.com/selenium-python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
# このchromedriverはブラウザChromeのバージョンと一致させ無ければならない
# Chrome Ver.115以降のchromedriver
# https://voicetechno-jp.secure-web.jp/ChromeDriverV115orNewer.html
# 以下のサイトから、Version: 118.0.5993.70のwin32を使用
# https://googlechromelabs.github.io/chrome-for-testing/
#service = ChromeService(executable_path=r"C:\Users\iwasaki\ChromeDriver\chromedriver.exe")
#driver = webdriver.Chrome(service=service, options=options)

# 次によれば、自動更新できるようである→OK
# 【Selenium】ChromeDriver自動更新で楽する方法【Python】
# https://yuki.world/python-selenium-chromedriver-auto-update/
driver = webdriver.Chrome(options=options)

# 【Python】seleniumの仕様が変わっていた!?(2023/06時点)
# https://zenn.dev/aew2sbee/articles/python-error-selenium

#Googleのブラウザを開く
driver.get('https://www.google.com/')
time.sleep(2)

#スタビジを検索

# 「Selenium4ではfind_element_by_id、nameは非推奨」→動かない
# http://holiday-programmer.net/selenium_ver_check/
search_box = driver.find_element(By.NAME,'q')
search_box.send_keys('スタビジ')
search_box.submit()
time.sleep(60)  # これを入れないとブラウザが閉じてしまう
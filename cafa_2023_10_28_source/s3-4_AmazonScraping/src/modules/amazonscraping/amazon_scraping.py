import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
#from webdriver_manager.chrome import ChromeDriverManager

class AmazonScraping:
    def __init__(self, headress=True):
        options = Options()
        if headress:
            options.add_argument('--headless')  # ブラウザを起動表示するかどうか
        #driver = ChromeDriverManager(
        #    log_level=0,
        #    print_first_line=False,
        #    ).install()
        #self.driver = webdriver.Chrome(driver, options=options)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def __del__(self):
        # webdriver終了
        if hasattr(self, 'driver') == True and self.driver != None:
            self.driver.quit()

    def set_url(self, url):
        # 指定したURLに遷移
        self.driver.get(url)

        # HTMLをBeautifulSoupオブジェクトでパース
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def get_page(self, url):
        return self.driver.page_source
    
    # Amazonの商品を表示し開発ツールで要素を調べる
    # https://www.amazon.co.jp/dp/B097F34YGG/
    def get_productname(self):
        elem = self.soup.find(id='productTitle')
        if elem is not None:
            return str.strip(elem.text)
        else:
            return ''

    def get_price(self):
        div = self.soup.find('div', id='corePriceDisplay_desktop_feature_div')
        span = div.find('span', class_='a-price-whole')

        if span == None:
            span = div.find('span', class_='a-offscreen')

        return span.string.replace('\\', '').replace('￥', '').replace(',', '')

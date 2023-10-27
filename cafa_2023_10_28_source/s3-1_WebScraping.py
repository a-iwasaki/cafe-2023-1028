# 図解！PythonのRequestsを徹底解説！(インストール・使い方)の
#「RequestsでHTMLデータの取得(ダウンロード)」と[BeautifulSoupでYahooからニュース情報のスクレイピング]
# https://ai-inter1.com/python-requests/
# https://ai-inter1.com/python-webscraping/
# https://ai-inter1.com/python-webscraping/#st-toc-h-6
# https://ai-inter1.com/python-webscraping/#st-toc-h-9

# pip install requests
# pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import re

url = 'https://news.yahoo.co.jp'
response = requests.get(url)
#print(response.text[:500])

soup = BeautifulSoup(response.text, "html.parser")
#elems = soup.find_all("a")
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
# print(elems)
print(elems[1].contents[0])

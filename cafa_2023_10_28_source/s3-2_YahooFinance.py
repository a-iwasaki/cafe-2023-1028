# 図解！PythonでWEB スクレイピングを始めよう！の「Yahoo Financeから米国の株価情報の取得」
# https://ai-inter1.com/python-webscraping/#st-toc-h-15

# pip install lxml
# pip install html5lib

# 以下はインストール済み
# pip install bs4
# pip install pandas

import pandas as pd

# ■ Pythonの証明書が不正で[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificateとなる
# Python requests で SSLError が起きて毎回ググってるのでまとめた
# https://stakiran.hatenablog.com/entry/2018/06/12/212914
# Python requestsライブラリは認証局の証明書をどう管理する?
# https://dev.classmethod.jp/articles/how-to-manage-ca-root-certs-for-requets-library/

# ■ SSL: CERTIFICATE_VERIFY_FAILED の仮の回避策
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#url = 'https://info.finance.yahoo.co.jp/ranking/?kd=4'
#data = pd.read_html(url, header = 0)
#print(data[0].head())

# ■ finance.yahoo.com は requestsでheadersがないとだめ
# Getting 404 error for certain stocks and pages on yahoo finance python
# https://stackoverflow.com/questions/68259148/getting-404-error-for-certain-stocks-and-pages-on-yahoo-finance-python
import requests 

url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'
# This is a standard user-agent of Chrome browser running on Windows 10 
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
resp = requests.get(url, headers=headers, timeout=5).text 
#print(resp)
data = pd.read_html(resp, header = 0)
print(data[0].head())

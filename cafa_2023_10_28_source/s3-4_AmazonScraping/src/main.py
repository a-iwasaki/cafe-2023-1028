import os
import sys
import datetime
from modules.excel.excel import Excel
from modules.amazonscraping.amazon_scraping import AmazonScraping
from modules.utils.utils import indexof

# 作業ディレクトリをmain.py格納ディレクトリに設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('---target urls----------')
# Excelを開く
excel = Excel('..\\data\\scraping.xlsx')

# urlシートを取得
ws = excel.get_sheet('url')

urls = []
# A1~A1000までを探索
for i in range(1, 1000):
    cell = 'A' + str(i)
    val = ws[cell].value

    # URLが指定されてなければ終了
    if val == None:
        break

    # URLをリストに取得
    urls.append(val)
    print(val)

# amazonスクレイピングオブジェクト初期化
amazon = AmazonScraping()

print('---get value from target urls----------')
map = {}
for url in urls:
    # amazonスクレイピングオブジェクトにURLを設定
    amazon.set_url(url)
    map[url] = {}

    # 欲しい情報を取得

    # 商品名
    map[url]['商品名'] = amazon.get_productname()
    if(map[url]['商品名'] != ''):
        print(map[url]['商品名'])
    else:
        print('ページが見つかりませんでした。URL：' + url)
        map.pop(url)
        continue

    # 値段
    map[url]['価格'] = amazon.get_price()
    print(map[url]['価格'])

# outputシートを取得
ws = excel.get_sheet('output')
now = datetime.datetime.now()

for key in map.keys():

    product = map[key]['商品名']
    price = int(map[key]['価格'])

    cols = excel.get_row_values(ws, 1)  # outputシートの1列目の値を取り出す
    idx = indexof(cols, product)

    # 商品名列が既にある場合
    if idx > -1:
        col_number = excel.change_col_number_from_index(idx+2)

    # 商品名列がない場合
    else:
        col_number = excel.change_col_number_from_index(ws.max_column+1)
        ws[col_number+str(1)] = product

    row = ws.max_row

    # 日時が出力されていない場合
    if ws['A'+str(row)].value != now:
        row = row+1

    # 日時
    ws['A'+str(row)] = now
    # 価格
    ws[col_number+str(row)] = price

excel.save()

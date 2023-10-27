# [Python] Googleスプレッドシートのデータを読み込み、pandasのDataFrame型として取り込む
# https://note.com/kohaku935/n/nc13bcd11632d

# [Python] Googleスプレッドシートにアクセスするための設定 
# https://note.com/kohaku935/n/ned9e907aac77
# Google Drive、Google Sheets APIを有効にし、「サービスアカウント」を作成する。そのキーをダウンロードし、client_secrets_service.jsonで保存

# pip install gspread pandas
# google-auth-httplib2はインストール済み

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SS_FILE_ID = '1cI-2jnTF5X2NVUy7mjDY3mytRug10pcTv5ZFs7YqIcA'
SS_SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

credentials = ServiceAccountCredentials.from_json_keyfile_name(r'./client_secrets_service.json', SS_SCOPES)
#OAuth2のクレデンシャルを使用してGoogleAPIにログイン
gc = gspread.authorize(credentials)
# IDを指定して、Googleスプレッドシートのワークブックを選択する
workbook = gc.open_by_key(SS_FILE_ID)
# シート名を指定して、ワークシートを選択
worksheetKokyaku = workbook.worksheet('kokyaku')
gssKokyakuDf = pd.DataFrame(worksheetKokyaku.get_values()[1:], columns=worksheetKokyaku.get_values()[0])
KokyakuDf = gssKokyakuDf.set_index('顧客ID')

print(KokyakuDf)

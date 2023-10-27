# SpreadSheet
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Drive
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload
import io
import os

# メール送信
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
import time

import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
DEBUG = config.get('MAIL','DEBUG').lower() !=  'false'
GMAIL_ACOUNNT = config.get('MAIL','GMAIL_ACCOUNT')
GMAIL_PASSWORD = config.get('MAIL','GMAIL_PASSWORD')

CHARSET = "utf-8"

# SpreadSheetsから顧客マスタをPandasに取り込む関数
def GetKokyakuDf():

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
    _KokyakuDf = gssKokyakuDf.set_index('顧客ID')

    return _KokyakuDf

# 指定ファイルをダウンロードする関数
def SeikyushoDownLoad(FileName):

    DRV_SCOPES = ['https://www.googleapis.com/auth/drive']
    DRV_FODLER_ID = '1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd'      # Google DrivでFolderを開いた時のURLのフォルダ部分　https://drive.google.com/drive/folders/1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd

    store = file.Storage('drive_access_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./client_secrets.json', DRV_SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    results = drive_service.files().list(
            q=f"name contains '{FileName}' and '{DRV_FODLER_ID}' in parents",
            pageSize=10, 
            fields="files(id, name)"
        ).execute()

    items = results.get('files', [])

    if not items:
        print('No files found.')
        return None
    else:
        #print('Files:')
        _SaveFileName = None
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            #Download
            if (item['name'] == FileName):
                request = drive_service.files().get_media(fileId=item['id'])
                _SaveFileName = os.path.join(r'C:\Users\iwasaki\pdf_data\download', item['name'])    # item['name']にOSで利用できない文字があれば問題あり
                fh = io.FileIO(_SaveFileName, mode='wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                return _SaveFileName

# メールを送信する関数
def send_gmail(msg):
    """
    引数msgをGmailで送信
    """
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    # ログ出力
    server.set_debuglevel(False)
    # ログインしてメール送信
    server.starttls()
    server.login(GMAIL_ACOUNNT, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()       #■

# MIME形式のメッセージを作成する関数
def make_mime(mail_to, subject, body, full_path=None):
    """
    引数をMIME形式に変換
    """
    if (full_path != None and
        full_path != ''):    
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', CHARSET))
    else:
        msg = MIMEText(body, 'plain', CHARSET)  #メッセージ本文

    #msg['Subject'] = subject #件名
    msg['Subject'] = Header(subject.encode(CHARSET), CHARSET)
    msg['To'] = mail_to #宛先
    msg['From'] = GMAIL_ACOUNNT #送信元

    #ファイル添付
    if (full_path != None and
        full_path != ''):

        with open(full_path, "rb") as f:
            AtchFile = MIMEApplication(f.read())

        file_basename = os.path.basename(full_path)
        AtchFile.add_header("Content-Disposition", "attachment", filename = file_basename)
        msg.attach(AtchFile)

    return msg

if __name__ == '__main__':

    #メール本文を読み込む
    with open("s1-34_mail_body.txt", encoding="utf-8") as f:
        mail_body_template = f.read()
    
    KokyakuDf = GetKokyakuDf()
    #print(KokyakuDf)

    for index, row in KokyakuDf.iterrows():
        kaisha = row["顧客名称"]
        busho = row["部署"]
        tanto = row["担当者"]
        mail_address = row["メールアドレス"]
        sikyusho_file_name = row["請求書ファイル名"]
        #print(index,kaisha, busho, tanto, mail_address, sikyusho_file_name)

        SeikyuShoPdf = SeikyushoDownLoad(sikyusho_file_name)
    
        # f文字列（フォーマット文字列）で（ https://note.nkmk.me/python-f-strings/#f ）文字列の置換
        body_text = mail_body_template.format(
                company=kaisha,
                department=busho,
                person=tanto
        )

        msg = make_mime(
            mail_to=mail_address, 
            subject='関西IT支部からの請求書',
            body=body_text,
            full_path=SeikyuShoPdf)
        
        # gmailで送信
        send_gmail(msg)

        # 1秒スリープ
        time.sleep(1)
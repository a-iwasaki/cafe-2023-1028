# [Python]GoogleDriveAPIの基本的な使い方
# https://zenn.dev/wtkn25/articles/python-googledriveapi-operation
# [Python]GoogleDriveAPIを使う方法
# https://zenn.dev/wtkn25/articles/python-googledriveapi-auth
# 認証後、アクセストークンとして、保存する

# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client

# [Python] Googleドライブ上のファイルをダウンロードする
# https://note.com/kohaku935/n/nd7e984e8676c

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('drive_access_token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('./client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))

FolderId = '1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd'      # Google DrivでFolderを開いた時のURLのフォルダ部分　https://drive.google.com/drive/folders/1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd
results = drive_service.files().list(
        q=f"name contains '.pdf' and '{FolderId}' in parents",
        pageSize=10, 
        fields="files(id, name)"
    ).execute()

items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
        #Download
        request = drive_service.files().get_media(fileId=item['id'])
        SaveFileName = os.path.join(r'C:\Users\iwasaki\pdf_data\download', item['name'])    # item['name']にOSで利用できない文字があれば問題あり
        fh = io.FileIO(SaveFileName, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
# PythonでGoogle Driveの自分のファイルを操作する方法
# https://zenn.dev/karaage0703/articles/9e92e077ad2725
# PyDriveでGoogle Driveの特定フォルダ配下のファイルをすべてダウンロードする
# https://qiita.com/i8b4/items/322dc8d81427717a86e4

# pip install PyDrive2

# Google Cloud Platform での認証情報は「OAuth 2.0 クライアント ID」で作成し、OAuthクライアントのキーをclient_secrets.jsonとして保存
# PythonからGoogleDriveに接続する方法を画像付きで説明
# https://takake-blog.com/python-driveapi/
# 毎回、認証の確認が必要

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#for file1 in file_list:
#    print('title: %s, id: %s' % (file1['title'], file1['id']))

drive_folder_id = '1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd'         # Google DrivでFolderを開いた時　https://drive.google.com/drive/folders/1HfsZn71geZxMjuOyEzQMD__oqO_6Ccxd
save_folder = r'C:\Users\iwasaki\pdf_data\download'

def download_recursively(save_folder, drive_folder_id):
    # 保存先フォルダがなければ作成
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    max_results = 100
    query = "'{}' in parents and trashed=false".format(drive_folder_id)

    for file_list in drive.ListFile({'q': query, 'maxResults': max_results}):
        for file in file_list:
            # mimeTypeでフォルダか判別
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                # 再帰的に検索しているが、今回はやめ
                # download_recursively(os.path.join(save_folder, file['title']), file['id'])
                pass
            else:
                file.GetContentFile(os.path.join(save_folder, file['title']))

if __name__ == '__main__':
    download_recursively(save_folder, drive_folder_id)

# 【RPA】Python×メール(Gmail)送信自動化｜SMTP認証・添付ファイル・プログラム構築までの流れを徹底解説
# https://di-acc2.com/system/rpa/2078/
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
import os

# Gmail設定
#my_account = 'ai.soft.jp@gmail.com'
#my_password = ''
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
DEBUG = config.get('MAIL','DEBUG').lower() !=  'false'
GMAIL_ACOUNNT = config.get('MAIL','GMAIL_ACCOUNT')
GMAIL_PASSWORD = config.get('MAIL','GMAIL_PASSWORD')
MAIL_TO = config.get('MAIL','MAIL_TO')

CHARSET = "iso-2022-jp"

def send_gmail(msg):
    """
    引数msgをGmailで送信
    """
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    # ログ出力
    server.set_debuglevel(False)    #■
    # ログインしてメール送信
    server.starttls()
    server.login(GMAIL_ACOUNNT, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()                   #■

def make_mime(mail_to, subject, body, full_path=None):
    """
    引数をMIME形式に変換
    """
    #メッセージ本文
    if (full_path != None and
        full_path != ''):    
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', CHARSET))
    else:
        msg = MIMEText(body, 'plain', CHARSET)

    #msg['Subject'] = subject  #件名
    msg['Subject'] = Header(subject.encode(CHARSET), CHARSET)   # Headerの使い方が? subject.encode(CHARSET)はなくても良さそう?

    #msg['To'] = mail_to         #宛先
    #msg['From'] = GMAIL_ACOUNNT #送信元
    # 「名前」を入れるには”email.utils.formataddr”を使う
    from email.utils import formataddr
    msg['To'] = formataddr(('テストさん', mail_to), CHARSET)    # ('テストさん', mail_to) はタプル
    msg['From'] = formataddr(('岩崎', GMAIL_ACOUNNT), CHARSET)

    # 実害はないが、米国太平洋標準時(PDT) で送信される。以下の処理を入れてもだめ
    #from email.utils import formatdate
    #msg['Date'] = formatdate()

    #ファイル添付
    if (full_path != None and
        full_path != ''):

        with open(full_path, "rb") as f:
            AtchFile = MIMEApplication(f.read())

        file_basename = os.path.basename(full_path)
        AtchFile.add_header("Content-Disposition", "attachment", filename = file_basename)
        msg.attach(AtchFile)

    return msg

def send_my_message():
    """
    メイン処理
    """
    # MIME形式に変換
    msg = make_mime(
        mail_to=MAIL_TO,    #送信したい宛先を指定
        subject='Pythonメール添付テスト',
        body='メール添付テスト',
        full_path=r'C:\Users\iwasaki\Documents\fies_t4.xls')
    # gmailで送信
    send_gmail(msg)

if __name__ == '__main__':
    send_my_message()
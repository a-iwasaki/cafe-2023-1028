# 【SMTP】PythonでGmailを自動送信する方法
# https://engineer-life.dev/python-gmail-smtp/
import smtplib, ssl
from email.mime.text import MIMEText

# Gmail設定
#my_account = 'ai.soft.jp@gmail.com'
#my_password = ''

# pythonプログラムにおける設定ファイル管理モジュール～configparserの使い方と注意点～
# https://qiita.com/mimitaro/items/3506a444f325c6f980b2
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
DEBUG = config.get('MAIL','DEBUG').lower() !=  'false'
GMAIL_ACOUNNT = config.get('MAIL','GMAIL_ACCOUNT')
GMAIL_PASSWORD = config.get('MAIL','GMAIL_PASSWORD')
MAIL_TO = config.get('MAIL','MAIL_TO')

def send_gmail(msg):
    """
    引数msgをGmailで送信
    """
    # ポート465と587の違いとは？
    # https://sendgrid.kke.co.jp/blog/?p=12945
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) 
    # ログ出力
    server.set_debuglevel(DEBUG)
    # ログインしてメール送信
    server.login(GMAIL_ACOUNNT, GMAIL_PASSWORD)         # パスワードは「アプリパスワード」 https://support.google.com/accounts/answer/185833?hl=ja
    server.send_message(msg)
    server.quit()       #■追加

def make_mime(mail_to, subject, body):
    """
    引数をMIME形式に変換
    """
    # MIMEによるEメールの構造
    # https://azisava.sakura.ne.jp/programming/0021.html
    msg = MIMEText(body, 'plain') #メッセージ本文 デフォルトでUTF-8になる
    msg['Subject'] = subject #件名
    msg['To'] = mail_to #宛先
    msg['From'] = GMAIL_ACOUNNT #送信元
    return msg

def send_my_message():
    """
    メイン処理
    """
    # MIME形式に変換
    msg = make_mime(
        mail_to=MAIL_TO,    #送信したい宛先を指定
        subject='Pythonメール送信',
        body='Pythonメール送信テスト')
    # gmailで送信
    send_gmail(msg)

if __name__ == '__main__':
    send_my_message()
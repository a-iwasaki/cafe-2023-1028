# PDFファイルにページ番号を追加する方法(Pythonで)
# https://qiita.com/achiwa912/items/9d82484183e3b6c9da3c
# pip install reportlab
# pip install pdfrw

from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# フォントの読み込み
pdfmetrics.registerFont(TTFont("Century", "C:/Windows/Fonts/CENTURY.TTF"))

input_file = r"C:\Users\iwasaki\pdf_data\out\kekka.pdf"
output_file = r"C:\Users\iwasaki\pdf_data\out\kekka_page.pdf"

reader = PdfReader(input_file)                  #PDFの読み込み
pages = [pagexobj(p) for p in reader.pages]     #PDFのページをXobjへの変換

canvas = Canvas(output_file)
for page_num, page in enumerate(pages, start=1):
    
    canvas.doForm(makerl(canvas, page))         # ReportLabオブジェクトへの変換、PDF データに展開

    footer_text = f"- {page_num}/{len(pages)} -"
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)           # 色の指定
    #canvas.setFont('Times-Roman', 14)          # フォントの指定
    canvas.setFont('Century', 10)               # フォントの指定CENTURY
    #canvas.drawString(290, 10, footer_text)    # 位置を指定し文字を書き出す
    canvas.drawCentredString(x=105*mm, y=10*mm, text=footer_text)     # 位置を指定し文字を書き出す
    canvas.restoreState()
    canvas.showPage()                           # ページデータの確定

canvas.save()

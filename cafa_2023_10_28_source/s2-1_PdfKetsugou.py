# Python, pypdfでPDFを結合・分割（ファイル全体・個別ページ）
# https://note.nkmk.me/python-pypdf2-pdf-merge-insert-split/
# PythonでPDFを複数まとめて自動結合！日本語ファイルを1つに集約
# https://fastclassinfo.com/entry/python_joins_pdf/
# pip install pypdf
import pypdf
import pathlib  # pathlibの使い方 https://note.nkmk.me/python-pathlib-usage/

# 結合したい(結合元)PDFを取得
infiles = list(pathlib.Path(r"C:\Users\iwasaki\pdf_data\in").glob('*.pdf'))     # glob「Pythonで条件を満たすパスの一覧を再帰的に取得( https://note.nkmk.me/python-glob-usage/ )」

# 結合元PDFを並び替え
s_infiles = sorted(infiles)     # リストをソートするsortとsorted https://note.nkmk.me/python-list-sort-sorted/

merger = pypdf.PdfMerger()

# 入力ファイルを結合する
for file in s_infiles:
    print("infiles", file, type(file))
    merger.append(file)         # fileは文字列にした方がいいでしょう

# 結合したファイルを書き出す
out_path = pathlib.Path(r"C:\Users\iwasaki\pdf_data\out")
merger.write(out_path.joinpath("kekka.pdf"))
merger.close()
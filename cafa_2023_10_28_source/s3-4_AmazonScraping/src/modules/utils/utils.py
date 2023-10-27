# リスト内の要素のインデックスを取得する
def indexof(li, elem, default=-1):
    return li.index(elem) if elem in li else default
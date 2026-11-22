"""python3 pages.py out/mNN.docx NN: baca PDF hasil render, simpan halaman tiap heading ke out/mNN.docx.pages.json"""
import json, re, sys, pymupdf
docx = sys.argv[1]; pdf = docx[:-5] + '.pdf'
import importlib
from gen import Builder
n = sys.argv[2]
c = importlib.import_module('content_%s' % n)
b = Builder(c.META); c.fill(b)
doc = pymupdf.open(pdf)
texts = [re.sub(r'\s+', ' ', pg.get_text()) for pg in doc]
pages = {}
start = 2
for lvl, num, title, bm in b.toc:
    head = (num + '. ' + title) if lvl == 1 else (num + ' ' + title)
    for i in range(start, len(texts)):
        if head in texts[i]:
            pages[bm] = i + 1; start = i; break
    else:
        print('TIDAK DITEMUKAN', head)
json.dump(pages, open(docx + '.pages.json', 'w'))
print(len(doc), 'halaman;', pages)

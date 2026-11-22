"""python3 build.py NN [halaman.json] -> out/mNN.docx"""
import importlib
import json
import os
import sys

from gen import build

HERE = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1]
out = os.path.join(HERE, 'out', 'm%s.docx' % n)
os.makedirs(os.path.dirname(out), exist_ok=True)
pages = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
c = importlib.import_module('content_%s' % n)
b = build(c.META, c.fill, out, pages)
print(out, '-', len(b.body), 'blok,', len(b.images), 'gambar,', len(b.toc), 'entri daftar isi')

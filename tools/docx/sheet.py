"""python3 sheet.py file.pdf keluaran.png halaman_awal halaman_akhir [dpi]: gabungkan beberapa halaman PDF jadi satu gambar untuk pengecekan visual"""
import sys, pymupdf
pdf, out, a, bb = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
doc = pymupdf.open(pdf)
imgs = [doc[p].get_pixmap(dpi=int(sys.argv[5]) if len(sys.argv) > 5 else 45) for p in range(a - 1, min(bb, len(doc)))]
w = sum(i.width for i in imgs); h = max(i.height for i in imgs)
o = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, w, h), False); o.set_rect(o.irect, (120, 120, 120)); x = 0
for i in imgs: i.set_origin(x, 0); o.copy(i, i.irect); x += i.width
o.save(out)

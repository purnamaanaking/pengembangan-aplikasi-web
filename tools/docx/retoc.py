"""Memperbarui nomor halaman daftar isi pada docx modul (desain Modul 09-12) dari hasil render Word.

Dipakai untuk docx yang tidak dibangun oleh gen.py (Modul 09 dan 10). Modul 11 dan 12 memakai twopass.sh.
Setiap entri daftar isi adalah paragraf dengan hyperlink ke bookmark `toc_N`, dan teks terakhirnya adalah
nomor halaman. Skrip ini merender docx dengan Word (render.sh), mencari halaman tempat setiap heading muncul,
menulis nomor itu, lalu mengulang sampai stabil.

Pemakaian (butuh Microsoft Word dan PyMuPDF):
    $PY retoc.py out/m10.docx
    $PY retoc.py out/m09.docx --break-before "5.12 Fallback route"   # paksa heading mulai di halaman baru
"""
import os
import re
import subprocess
import sys
import zipfile

import pymupdf

from gdocs_compat import fill_toc_dots

HERE = os.path.dirname(os.path.abspath(__file__))


def headings(doc_xml):
    """{bookmark: teks heading}"""
    out = {}
    for m in re.finditer(r'<w:p>((?:(?!</w:p>).)*?<w:bookmarkStart w:name="(toc_\d+)"(?:(?!</w:p>).)*)</w:p>', doc_xml, re.S):
        text = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', m.group(1)))
        out[m.group(2)] = text.replace('&amp;', '&').strip()
    return out


def page_map(pdf, heads):
    doc = pymupdf.open(pdf)
    texts = [re.sub(r'\s+', ' ', p.get_text()) for p in doc]
    pages, start = {}, 2
    for bm, text in heads.items():
        for i in range(start, len(texts)):
            if text in texts[i]:
                pages[bm] = i + 1
                start = i
                break
        else:
            raise SystemExit('Heading tidak ditemukan di PDF: %s' % text)
    return pages, len(doc)


def write_pages(path, pages):
    with zipfile.ZipFile(path) as z:
        items = [(n, z.read(n)) for n in z.namelist() if not n.endswith('/')]
    out = []
    for n, data in items:
        if n == 'word/document.xml':
            s = data.decode('utf-8')

            def fix(m):
                para, bm = m.group(0), m.group(1)
                return re.sub(r'(<w:t[^>]*>)\d+(</w:t>)(?!.*<w:t)', r'\g<1>%d\2' % pages[bm], para, flags=re.S)
            s = re.sub(r'<w:p>(?:(?!</w:p>).)*?w:anchor="(toc_\d+)"(?:(?!</w:p>).)*</w:p>', fix, s, flags=re.S)
            s = fill_toc_dots(s)  # jumlah titik bergantung pada lebar nomor halaman
            data = s.encode('utf-8')
        out.append((n, data))
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, data in out:
            z.writestr(n, data)
    os.replace(tmp, path)


def render(path):
    r = subprocess.run([os.path.join(HERE, 'render.sh'), path], capture_output=True, text=True)
    if r.stdout.strip() != 'OK':
        raise SystemExit('Word gagal membuka %s' % path)
    return path[:-5] + '.pdf'


def break_before(path, titles):
    """Tambahkan pageBreakBefore pada paragraf heading yang teksnya persis salah satu dari titles."""
    with zipfile.ZipFile(path) as z:
        items = [(n, z.read(n)) for n in z.namelist() if not n.endswith('/')]
    out = []
    for n, data in items:
        if n == 'word/document.xml':
            s = data.decode('utf-8')
            for title in titles:
                pat = re.compile(r'(<w:p><w:pPr><w:pStyle w:val="Heading\d"/>)(</w:pPr>(?:(?!</w:p>).)*?>%s</w:t>)' % re.escape(title), re.S)
                s, k = pat.subn(r'\1<w:pageBreakBefore/>\2', s)
                if not k and title not in s:
                    raise SystemExit('Heading tidak ditemukan: %s' % title)
            data = s.encode('utf-8')
        out.append((n, data))
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, data in out:
            z.writestr(n, data)
    os.replace(tmp, path)


if __name__ == '__main__':
    args = sys.argv[1:]
    titles = []
    while '--break-before' in args:
        i = args.index('--break-before')
        titles.append(args[i + 1])
        del args[i:i + 2]
    path = os.path.abspath(args[0])
    if titles:
        break_before(path, titles)
    heads = headings(zipfile.ZipFile(path).read('word/document.xml').decode('utf-8'))
    last = None
    for i in range(4):
        pages, n = page_map(render(path), heads)
        if pages == last:
            print('stabil: %d halaman, %d entri daftar isi' % (n, len(pages)))
            break
        write_pages(path, pages)
        last = pages
    else:
        print('nomor halaman belum stabil')

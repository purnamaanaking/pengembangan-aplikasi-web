"""Menyesuaikan docx modul agar tampil rapi saat dibuka di Google Docs.

Word memaafkan beberapa bentuk XML yang diabaikan Google Docs. Skrip ini mengubah bentuk-bentuk itu
tanpa mengubah tampilan di Word:

1. Karakter tab di dalam teks (`<w:t>\\t</w:t>`) diganti elemen `<w:tab/>`.
   Google Docs membuang tab di dalam teks, sehingga daftar isi, footer, dan baris bawah sampul berantakan.
2. Field `PAGEREF` di daftar isi diganti teks nomor halaman biasa (hasil field yang tersimpan).
   Google Docs tidak mendukung field ini dan menghapus nomornya.
3. Jarak baris "exact" yang besar di sampul (judul 980 twip, spacer 900 twip) diganti jarak "auto".
   Google Docs melebarkan jarak exact sehingga sampul tumpah ke halaman kedua.
4. Blok kode boleh terpotong di pergantian halaman (`cantSplit` dan `keepNext` dibuang dari tabel blok kode).
   Google Docs selalu memotong blok kode panjang, sedangkan Word memindahkannya utuh ke halaman berikutnya.
   Dengan aturan yang sama, jumlah halaman di Word dan Google Docs sama, sehingga nomor daftar isi benar di keduanya.
5. Chip tag di sampul diberi latar gelap. Google Docs tidak menampilkan border per-teks, jadi tanpa latar
   chip hanya tampil sebagai teks berwarna.
6. Titik-titik daftar isi ditulis sebagai karakter "." biasa, bukan tab leader. Google Docs tidak mendukung
   tab leader. Jumlah titik dihitung dari lebar karakter Calibri (calibri_widths.json), font yang dipakai
   Word maupun Google Docs, lalu nomor halaman diratakan kanan dengan tab biasa.

Pemakaian:
    python3 gdocs_compat.py file.docx [file2.docx ...]   # mengubah file di tempat
Dari kode:
    from gdocs_compat import fix_xml
"""
import html
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

PARTS = ('word/document.xml', 'word/header1.xml', 'word/footer1.xml')

_T = re.compile(r'<w:t(?: xml:space="preserve")?>([^<]*\t[^<]*)</w:t>')
_R = r'<w:r>(?:(?!</w:r>).)*?'
_PAGEREF = re.compile(
    _R + r'<w:fldChar w:fldCharType="begin"/></w:r>'
    + _R + r'<w:instrText[^>]*>\s*PAGEREF [^<]*</w:instrText></w:r>'
    + _R + r'<w:fldChar w:fldCharType="separate"/></w:r>'
    + r'(<w:r>(?:(?!</w:r>).)*?</w:r>)'
    + _R + r'<w:fldChar w:fldCharType="end"/></w:r>', re.S)


def _split_tabs(m):
    parts = m.group(1).split('\t')
    out = []
    for i, p in enumerate(parts):
        if i:
            out.append('<w:tab/>')
        if p:
            out.append('<w:t xml:space="preserve">%s</w:t>' % p)
    return ''.join(out)


_TBL = re.compile(r'<w:tbl>.*?</w:tbl>', re.S)
_CHIP = re.compile(r'(<w:bdr w:val="single" w:color="E3A97C"[^>]*/>)(?!<w:shd)')


def _loosen_code(m):
    t = m.group(0)
    if '&lt;/&gt; ' in t[:4000] and 'w:color w:val="E3A97C"/><w:sz w:val="15"/>' in t[:4000]:
        t = t.replace('<w:trPr><w:cantSplit/></w:trPr>', '').replace('<w:keepNext/>', '')
    return t


_W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibri_widths.json'), encoding='utf-8'))
_RIGHT = 9638  # posisi tab kanan daftar isi (twip)
_TOC_P = re.compile(r'<w:p>(?:(?!</w:p>).)*?w:anchor="toc_\d+"(?:(?!</w:p>).)*</w:p>', re.S)


def _twips(text, size_half_pt, bold):
    table = _W['bold' if bold else 'regular']
    units = sum(table.get(ch, 500.0) for ch in text)
    return units / 1000.0 * (size_half_pt / 2.0) * 20.0


def _fill_dots(m):
    p = m.group(0).replace(' w:leader="dot"', '')
    tabs = [int(x) for x in re.findall(r'<w:tab w:val="left" w:pos="(\d+)"/>', p)]
    title = re.search(r'<w:hyperlink[^>]*><w:r><w:rPr>((?:(?!</w:rPr>).)*)</w:rPr><w:t[^>]*>([^<]*)</w:t>', p, re.S)
    dots = re.search(r'(<w:r><w:rPr>(?:(?!</w:rPr>).)*?<w:color w:val="BEBAB4"/>(?:(?!</w:rPr>).)*?<w:sz w:val="(\d+)"/>'
                     r'(?:(?!</w:rPr>).)*?</w:rPr>)(?:<w:t[^>]*>[ .]*</w:t>)?<w:tab/></w:r>', p, re.S)
    page = re.findall(r'<w:r><w:rPr>((?:(?!</w:rPr>).)*)</w:rPr><w:t[^>]*>(\d+)</w:t></w:r>', p, re.S)
    if not (tabs and title and dots and page):
        return p
    size = int(dots.group(2))
    title_bold = '<w:b/>' in title.group(1)
    page_rpr, page_text = page[-1]
    page_size = int(re.search(r'<w:sz w:val="(\d+)"/>', page_rpr).group(1))
    start = tabs[0] + _twips(html.unescape(title.group(2)), size, title_bold)
    end = _RIGHT - _twips(page_text, page_size, '<w:b/>' in page_rpr)
    dot = _twips('.', size, False)
    space = _twips(' ', size, False)
    n = int((end - start - 2 * space) / dot) - 1
    fill = ' ' + '.' * max(n, 0) if n > 2 else ''
    new_run = dots.group(1) + ('<w:t xml:space="preserve">%s</w:t>' % fill if fill else '') + '<w:tab/></w:r>'
    return p[:dots.start()] + new_run + p[dots.end():]


def fill_toc_dots(s):
    return _TOC_P.sub(_fill_dots, s)


def fix_xml(s):
    s = _T.sub(_split_tabs, s)
    s = _TBL.sub(_loosen_code, s)
    s = _CHIP.sub(r'\1<w:shd w:fill="3A3330" w:color="auto" w:val="clear"/>', s)
    s = _PAGEREF.sub(r'\1', s)
    s = s.replace('w:line="980" w:lineRule="exact"', 'w:line="240" w:lineRule="auto"')
    s = s.replace('w:before="0" w:line="900" w:lineRule="exact"', 'w:before="860" w:line="240" w:lineRule="auto"')
    s = fill_toc_dots(s)
    return s


def report(s):
    return {
        'tab-teks': len(_T.findall(s)),
        'PAGEREF': s.count('PAGEREF'),
        'exact-besar': len(re.findall(r'w:line="(?:9[0-9]{2}|[6-8][0-9]{2})" w:lineRule="exact"', s)),
        'kode-ditahan': sum(1 for t in _TBL.findall(s) if '&lt;/&gt; ' in t[:4000] and ('<w:cantSplit/>' in t or '<w:keepNext/>' in t)),
        'chip-tanpa-latar': len(_CHIP.findall(s)),
        'tab-leader': s.count('w:leader="dot"'),
    }


def fix_docx(path):
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            z.extractall(tmp)
        for part in PARTS:
            p = os.path.join(tmp, part)
            if os.path.exists(p):
                s = open(p, encoding='utf-8').read()
                open(p, 'w', encoding='utf-8').write(fix_xml(s))
        out = path + '.tmp'
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for n in names:
                if not n.endswith('/'):
                    z.write(os.path.join(tmp, n), n)
        os.replace(out, path)
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        before = {p: report(zipfile.ZipFile(f).read(p).decode()) for p in PARTS}
        fix_docx(f)
        after = {p: report(zipfile.ZipFile(f).read(p).decode()) for p in PARTS}
        print(os.path.basename(f))
        for p in PARTS:
            print('  %-20s %s -> %s' % (p, before[p], after[p]))

"""Membangun docx modul praktikum dengan desain Modul 09/10.

Basis paket (styles, header/footer, theme, gambar sampul) diambil dari docx Modul 10.
Isi dokumen dibangun dari spesifikasi (daftar blok) di content_XX.py.
"""
import os
import re
import shutil
import struct
import zipfile
from xml.sax.saxutils import escape

from gdocs_compat import PARTS, fix_xml
from hl import highlight

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(HERE, 'templates')
BASE_DOCX = os.path.join(REPO, 'docs', 'modul-praktikum', 'Modul-10-Pengenalan-Controller-dan-View-pada-Laravel.docx')
BASE = os.path.join(HERE, 'out', '_base')


def ensure_base():
    """Ekstrak docx Modul 10 sebagai basis paket (styles, header/footer, theme, latar sampul)."""
    if not os.path.isdir(BASE):
        with zipfile.ZipFile(BASE_DOCX) as z:
            z.extractall(BASE)

CAL = '<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
CON = '<w:rFonts w:ascii="Consolas" w:cs="Consolas" w:eastAsia="Consolas" w:hAnsi="Consolas"/>'
NOBI = '<w:b w:val="false"/><w:bCs w:val="false"/><w:i w:val="false"/><w:iCs w:val="false"/>'
SPACER = ('<w:p><w:pPr><w:spacing w:after="140" w:before="0" w:line="120" w:lineRule="exact"/></w:pPr>'
          '<w:r><w:rPr><w:sz w:val="4"/><w:szCs w:val="4"/></w:rPr><w:t xml:space="preserve"></w:t></w:r></w:p>')


def T(s):
    return '<w:t xml:space="preserve">%s</w:t>' % escape(s)


# ---------------------------------------------------------------- inline runs
def runs(text, size=21, code_size=19, color='1F1F1F', bold=False, italic=False):
    """Markup: `kode`, **tebal**."""
    out = []
    for tok in re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', text):
        if not tok:
            continue
        if tok.startswith('`'):
            out.append('<w:r><w:rPr>%s%s<w:color w:val="5E3A20"/><w:sz w:val="%d"/><w:szCs w:val="%d"/>'
                       '<w:shd w:fill="F6F5F3" w:color="auto" w:val="clear"/></w:rPr>%s</w:r>'
                       % (CON, NOBI, code_size, code_size, T(tok[1:-1])))
        else:
            b = bold
            if tok.startswith('**'):
                tok, b = tok[2:-2], True
            bi = ('<w:b/><w:bCs/>' if b else '<w:b w:val="false"/><w:bCs w:val="false"/>') + \
                 ('<w:i/><w:iCs/>' if italic else '<w:i w:val="false"/><w:iCs w:val="false"/>')
            out.append('<w:r><w:rPr>%s%s<w:color w:val="%s"/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>%s</w:r>'
                       % (CAL, bi, color, size, size, T(tok)))
    return ''.join(out)


class Builder:
    def __init__(self, meta):
        self.meta = meta
        self.body = []
        self.toc = []          # (level, nomor, judul, bookmark)
        self.bm = 0
        self.lists = []        # abstractNum decimal tambahan
        self.next_num = 10
        self.images = []       # (rid, nama file sumber)
        self.docpr = 100
        self.fig = 0

    # ------------------------------------------------------------ blok dasar
    def h1(self, text):
        self.bm += 1
        num, title = text.split('. ', 1)
        self.toc.append((1, num, title, 'toc_%d' % self.bm))
        pb = '<w:pageBreakBefore/>' if self.bm == 1 else ''
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Heading1"/>' + pb + '</w:pPr><w:bookmarkStart w:name="toc_%d" w:id="%d"/>'
                         '<w:r>%s</w:r><w:bookmarkEnd w:id="%d"/></w:p>' % (self.bm, self.bm, T(text), self.bm))

    def h2(self, text, page_break=False):
        """page_break=True memaksa subbab mulai di halaman baru. Dipakai bila Word dan Google Docs
        berbeda keputusan untuk heading di dasar halaman, agar nomor daftar isi sama di keduanya."""
        self.bm += 1
        num, title = text.split(' ', 1)
        self.toc.append((2, num, title, 'toc_%d' % self.bm))
        pb = '<w:pageBreakBefore/>' if page_break else ''
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Heading2"/>' + pb + '</w:pPr><w:bookmarkStart w:name="toc_%d" w:id="%d"/>'
                         '<w:r>%s</w:r><w:bookmarkEnd w:id="%d"/></w:p>' % (self.bm, self.bm, T(text), self.bm))

    def h3(self, text):
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Heading3"/></w:pPr><w:r>%s</w:r></w:p>' % T(text))

    def p(self, text, keep_next=False):
        kn = '<w:keepNext/>' if keep_next else ''
        self.body.append('<w:p><w:pPr>%s<w:spacing w:after="130" w:before="0" w:line="276"/></w:pPr>%s</w:p>' % (kn, runs(text)))

    def _list(self, items, num_id):
        for it in items:
            self.body.append('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/>'
                             '<w:numId w:val="%d"/></w:numPr><w:spacing w:after="70" w:before="0" w:line="264"/></w:pPr>%s</w:p>'
                             % (num_id, runs(it)))

    def bullets(self, items):
        self._list(items, 2)

    def checks(self, items):
        self._list(items, 9)

    def steps(self, items):
        nid = self.next_num
        self.next_num += 1
        self.lists.append(nid)
        self._list(items, nid)

    def pagebreak(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ------------------------------------------------------------ callout
    KINDS = {
        'catatan': ('E1E9F4', 'B9CCE8', 'Catatan.'),
        'laravel13': ('E1E9F4', 'B9CCE8', 'Catatan Laravel 13.'),
        'perhatian': ('F8EDD3', 'E6BB5E', 'Perhatian.'),
        'analisis': ('FBEDE2', 'F4D5BD', 'Analisis.'),
        'screenshot': ('E4F0E7', 'B7D8C0', 'Simpan screenshot.'),
    }

    def note(self, kind, text):
        fill, border, label = self.KINDS[kind]
        bd = ''.join('<w:%s w:val="single" w:color="%s" w:sz="4"/>' % (s, border) for s in ('top', 'left', 'bottom', 'right'))
        self.body.append(
            '<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="9638"/><w:tblLayout w:type="fixed"/></w:tblPr>'
            '<w:tblGrid><w:gridCol w:w="9638"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr>'
            '<w:tcW w:type="dxa" w:w="9638"/><w:tcBorders>%s</w:tcBorders><w:shd w:fill="%s" w:color="auto" w:val="clear"/>'
            '<w:tcMar><w:top w:type="dxa" w:w="120"/><w:left w:type="dxa" w:w="200"/><w:bottom w:type="dxa" w:w="120"/>'
            '<w:right w:type="dxa" w:w="200"/></w:tcMar></w:tcPr><w:p><w:pPr><w:spacing w:after="0" w:before="0" w:line="264"/></w:pPr>'
            '%s%s</w:p></w:tc></w:tr></w:tbl>' % (bd, fill, runs(label, size=20, bold=True), runs(' ' + text, size=20, code_size=18)))
        self.body.append(SPACER)

    # ------------------------------------------------------------ code
    def code(self, lang, src, label=None):
        bd = ''.join('<w:%s w:val="single" w:color="3D3D3D" w:sz="4"/>' % s for s in ('top', 'left', 'bottom', 'right'))
        paras = ['<w:p><w:pPr><w:keepNext/><w:spacing w:after="100" w:before="0"/></w:pPr><w:r><w:rPr>%s<w:b/><w:bCs/>'
                 '<w:color w:val="E3A97C"/><w:sz w:val="15"/><w:szCs w:val="15"/></w:rPr>%s</w:r></w:p>'
                 % (CON, T('</> ' + (label or lang)))]
        lines = src.strip('\n').split('\n')
        for ln in lines:
            rs = []
            for t, c, it in highlight(lang, ln):
                ital = '<w:i/><w:iCs/>' if it else '<w:i w:val="false"/><w:iCs w:val="false"/>'
                rs.append('<w:r><w:rPr>%s%s<w:color w:val="%s"/><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr>%s</w:r>'
                          % (CON, ital, c, T(t)))
            if not rs:
                rs = ['<w:r><w:rPr>%s<w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr>%s</w:r>' % (CON, T(''))]
            paras.append('<w:p><w:pPr><w:spacing w:after="0" w:before="0" w:line="252" w:lineRule="auto"/>'
                         '<w:ind w:left="188" w:hanging="188"/></w:pPr>%s</w:p>' % ''.join(rs))
        self.body.append(
            '<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="9638"/><w:tblLayout w:type="fixed"/></w:tblPr>'
            '<w:tblGrid><w:gridCol w:w="9638"/></w:tblGrid><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="9638"/>'
            '<w:tcBorders>%s</w:tcBorders><w:shd w:fill="2B2B2B" w:color="auto" w:val="clear"/><w:tcMar>'
            '<w:top w:type="dxa" w:w="140"/><w:left w:type="dxa" w:w="200"/><w:bottom w:type="dxa" w:w="140"/>'
            '<w:right w:type="dxa" w:w="200"/></w:tcMar></w:tcPr>%s</w:tc></w:tr></w:tbl>' % (bd, ''.join(paras)))
        self.body.append(SPACER)

    # ------------------------------------------------------------ tabel data
    def table(self, header, rows, widths):
        assert sum(widths) == 9638, sum(widths)
        bd = ''.join('<w:%s w:val="single" w:color="E6E5E3" w:sz="4"/>' % s for s in ('top', 'left', 'bottom', 'right'))
        mar = ('<w:tcMar><w:top w:type="dxa" w:w="80"/><w:left w:type="dxa" w:w="120"/><w:bottom w:type="dxa" w:w="80"/>'
               '<w:right w:type="dxa" w:w="120"/></w:tcMar><w:vAlign w:val="center"/>')

        def cell(w, fill, content):
            return ('<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="%d"/><w:tcBorders>%s</w:tcBorders>'
                    '<w:shd w:fill="%s" w:color="auto" w:val="clear"/>%s</w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:after="0" w:before="0" w:line="252"/></w:pPr>%s</w:p></w:tc>'
                    % (w, bd, fill, mar, content))
        trs = ['<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>%s</w:tr>'
               % ''.join(cell(w, '2B2B2B', runs(h, size=19, color='FFFFFF', bold=True)) for w, h in zip(widths, header))]
        for i, row in enumerate(rows):
            fill = 'FFFFFF' if i % 2 == 0 else 'F6F5F3'
            trs.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>'
                       % ''.join(cell(w, fill, runs(c, size=19, code_size=17)) for w, c in zip(widths, row)))
        self.body.append('<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="9638"/><w:tblLayout w:type="fixed"/></w:tblPr>'
                         '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
                         % (''.join('<w:gridCol w:w="%d"/>' % w for w in widths), ''.join(trs)))
        self.body.append(SPACER)

    # ------------------------------------------------------------ gambar
    def image(self, path, caption, descr, width_cm=15.6, numbered=True, border=True):
        w, h = png_size(path)
        cx = int(width_cm * 360000)
        cy = int(cx * h / w)
        rid = 'rIdImg%d' % (len(self.images) + 1)
        self.images.append((rid, path))
        self.docpr += 1
        ln = ('<a:ln w="12700"><a:solidFill><a:srgbClr val="BEBAB4"/></a:solidFill></a:ln>' if border else '<a:ln><a:noFill/></a:ln>')
        self.body.append(
            '<w:p><w:pPr><w:keepNext/><w:spacing w:after="60" w:before="120"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent t="0" r="0" b="0" l="0"/><wp:docPr id="{id}" name="{name}" descr="{descr}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
            '<pic:nvPicPr><pic:cNvPr id="0" name="{name}" descr=""/><pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>'
            '</pic:cNvPicPr></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}" cstate="none"/><a:srcRect/><a:stretch><a:fillRect/></a:stretch>'
            '</pic:blipFill><pic:spPr bwMode="auto"><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{ln}</pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline>'
            '</w:drawing></w:r></w:p>'.format(cx=cx, cy=cy, id=self.docpr, name=escape(os.path.basename(path)),
                                              descr=escape(descr, {'"': '&quot;'}), rid=rid, ln=ln))
        if numbered:
            self.fig += 1
            caption = 'Gambar %d. %s' % (self.fig, caption)
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>%s</w:p>'
                         % runs(caption, size=18, color='6A6763', italic=True))

    # ------------------------------------------------------------ TOC
    def toc_xml(self, pages):
        out = []
        for lvl, num, title, bm in self.toc:
            pg = str(pages.get(bm, 0))
            if lvl == 1:
                ppr = ('<w:pPr><w:keepNext/><w:tabs><w:tab w:val="left" w:pos="560"/><w:tab w:val="right" w:pos="9638" w:leader="dot"/>'
                       '</w:tabs><w:spacing w:after="10" w:before="%s" w:line="252"/></w:pPr>' % ('0' if not out else '110'))
                sz, col, b = 21, '1F1F1F', '<w:b/><w:bCs/>'
            else:
                ppr = ('<w:pPr><w:keepNext w:val="false"/><w:tabs><w:tab w:val="left" w:pos="1240"/><w:tab w:val="right" w:pos="9638" w:leader="dot"/>'
                       '</w:tabs><w:spacing w:after="0" w:before="0" w:line="212" w:lineRule="exact"/><w:ind w:left="560"/></w:pPr>')
                sz, col, b = 18, '3D3D3D', '<w:b w:val="false"/><w:bCs w:val="false"/>'
            rp = '<w:rPr>%s%s<w:color w:val="%s"/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (CAL, b, col, sz, sz)
            out.append(
                '<w:p>%s<w:r><w:rPr>%s<w:b/><w:bCs/><w:color w:val="85532F"/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>%s</w:r>'
                '<w:r><w:rPr><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr><w:t xml:space="preserve">\t</w:t></w:r>'
                '<w:hyperlink w:history="1" w:anchor="%s"><w:r>%s%s</w:r></w:hyperlink>'
                '<w:r><w:rPr><w:color w:val="BEBAB4"/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr><w:t xml:space="preserve">\t</w:t></w:r>'
                '<w:r>%s<w:fldChar w:fldCharType="begin"/></w:r><w:r>%s<w:instrText xml:space="preserve"> PAGEREF %s \\h </w:instrText></w:r>'
                '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r><w:r>%s<w:t>%s</w:t></w:r><w:r>%s<w:fldChar w:fldCharType="end"/></w:r></w:p>'
                % (ppr, CAL, sz, sz, T(num), sz, sz, bm, rp, T(title), sz, sz, rp, rp, bm, rp, rp, pg, rp))
        return ''.join(out)


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    return struct.unpack('>II', head[16:24])


# ---------------------------------------------------------------- sampul
def cover_xml(meta):
    s = open(os.path.join(TPL, 'cover.xml')).read()
    s = re.sub(r' xmlns:\w+="[^"]*"', '', s)

    def sub(old, new, count=1):
        nonlocal s
        o = '>%s</w:t>' % old
        assert o in s, old
        s = s.replace(o, '>%s</w:t>' % escape(new), count)
    sub('&lt;/&gt; MODUL 10 &#183; PRAKTIKUM', '</> MODUL %s · PRAKTIKUM' % meta['no'])
    for old, new in zip(['Controller dan', 'View pada', 'Laravel 13'], meta['title_lines']):
        sub(old, new)
    for key, val in meta['grid'].items():
        old = {'PERANGKAT': 'PHP 8.3+, Composer, Node.js 20.19+ atau 22.12+, Git',
               'FILE PENDUKUNG': 'laravel.png (tautan unduh ada di bagian Pengantar)',
               'PRASYARAT': 'Modul 09: Routing dan Bundling Asset di Laravel',
               'DIPERBARUI': '15 November 2026'}[key]
        sub(old, val)
    # chip tag
    m = re.search(r'(<w:p>(?:(?!<w:p>).)*?> controller </w:t>.*?</w:p>)', s, re.S)
    para = m.group(1)
    runs_ = re.findall(r'<w:r>.*?</w:r>', para, re.S)
    chip = next(r for r in runs_ if '> controller <' in r)
    gap = runs_[runs_.index(chip) + 1]
    ppr = para[:para.index('<w:r>')]
    new = ppr + ''.join(chip.replace('> controller <', '> %s <' % escape(c)) + gap for c in meta['chips']) + '</w:p>'
    s = s.replace(para, new)
    return s


def build(meta, fill, out_path, pages=None):
    ensure_base()
    b = Builder(meta)
    fill(b)
    root = open(os.path.join(BASE, 'word', 'document.xml')).read()
    opening = re.search(r'<w:document[^>]*>', root).group()
    for pfx, uri in (('a', 'http://schemas.openxmlformats.org/drawingml/2006/main'),
                     ('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')):
        if 'xmlns:%s=' % pfx not in opening:
            opening = opening[:-1] + ' xmlns:%s="%s">' % (pfx, uri)
    tochead = re.sub(r' xmlns:\w+="[^"]*"', '', open(os.path.join(TPL, 'tochead.xml')).read())
    sect = re.sub(r' xmlns:\w+="[^"]*"', '', open(os.path.join(TPL, 'sect.xml')).read())
    body = (cover_xml(meta) + tochead + b.toc_xml(pages or {})
            + ''.join(b.body) + sect)
    doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + opening + '<w:body>' + body + '</w:body></w:document>'

    work = out_path + '.d'
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(BASE, work)
    open(os.path.join(work, 'word', 'document.xml'), 'w').write(doc)

    # media: pertahankan image1 (latar sampul), ganti sisanya
    media = os.path.join(work, 'word', 'media')
    for f in os.listdir(media):
        if f != 'image1.png':
            os.remove(os.path.join(media, f))
    rels_path = os.path.join(work, 'word', '_rels', 'document.xml.rels')
    rels = open(rels_path).read()
    rels = re.sub(r'<Relationship Id="rId(1[2-7])"[^>]*/>', '', rels)
    rels = re.sub(r'<Relationship Id="[^"]*" Type="[^"]*/hyperlink"[^>]*/>', '', rels)
    add = []
    for i, (rid, src) in enumerate(b.images):
        name = 'fig%02d.png' % (i + 1)
        shutil.copy(src, os.path.join(media, name))
        add.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                   'Target="media/%s"/>' % (rid, name))
    rels = rels.replace('</Relationships>', ''.join(add) + '</Relationships>')
    open(rels_path, 'w').write(rels)

    # numbering: tambah abstractNum desimal untuk setiap daftar bernomor
    num_path = os.path.join(work, 'word', 'numbering.xml')
    nx = open(num_path).read()
    nx = re.sub(r'<w:abstractNum w:abstractNumId="([4-9])".*?</w:abstractNum>', '', nx, flags=re.S)
    nx = re.sub(r'<w:num w:numId="[3-8]">.*?</w:num>', '', nx, flags=re.S)
    absn, nums = [], []
    for k, nid in enumerate(b.lists):
        aid = 100 + k
        absn.append('<w:abstractNum w:abstractNumId="%d" w15:restartNumberingAfterBreak="0"><w:multiLevelType w:val="hybridMultilevel"/>'
                    '<w:lvl w:ilvl="0" w:tentative="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%%1."/>'
                    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="560" w:hanging="360"/></w:pPr><w:rPr><w:b/><w:bCs/>'
                    '<w:color w:val="85532F"/></w:rPr></w:lvl></w:abstractNum>' % aid)
        nums.append('<w:num w:numId="%d"><w:abstractNumId w:val="%d"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/>'
                    '</w:lvlOverride></w:num>' % (nid, aid))
    first_num = nx.index('<w:num ')
    nx = nx[:first_num] + ''.join(absn) + nx[first_num:]
    nx = nx.replace('</w:numbering>', ''.join(nums) + '</w:numbering>')
    open(num_path, 'w').write(nx)

    # header
    hp = os.path.join(work, 'word', 'header1.xml')
    hx = open(hp).read().replace('MODUL 10', 'MODUL %s' % meta['no'])
    open(hp, 'w').write(hx)

    # docProps
    cp = os.path.join(work, 'docProps', 'core.xml')
    c = open(cp).read()
    c = re.sub(r'<dc:title>.*?</dc:title>', '<dc:title>%s</dc:title>' % escape(meta['doc_title']), c)
    c = re.sub(r'<dcterms:(created|modified) xsi:type="dcterms:W3CDTF">[^<]*', r'<dcterms:\1 xsi:type="dcterms:W3CDTF">2026-11-22T08:00:00.000Z', c)
    open(cp, 'w').write(c)

    # kompatibel dengan Google Docs (tab sebagai <w:tab/>, nomor daftar isi tanpa field, tanpa jarak exact besar)
    for part in PARTS:
        pp = os.path.join(work, part)
        if os.path.exists(pp):
            fixed = fix_xml(open(pp).read())
            open(pp, 'w').write(fixed)

    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(work):
            for f in sorted(fn):
                full = os.path.join(dp, f)
                arc = os.path.relpath(full, work)
                z.write(full, arc)
    shutil.rmtree(work)
    return b

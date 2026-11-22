"""Ambil kode dari project yang sudah diuji, supaya isi modul identik dengan kode yang berjalan."""
import os
import re
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
ASSETS = os.path.join(HERE, 'assets')


def read(mod, path):
    return open(os.path.join(REPO, mod, path)).read().rstrip('\n')


def method(mod, path, name):
    """Blok `public function name(...)` beserta isinya, tanpa docblock, indentasi kelas dibuang."""
    s = read(mod, path)
    m = re.search(r'^( *)public function %s\(.*?^\1\}' % re.escape(name), s, re.S | re.M)
    return textwrap.dedent(m.group(0))


def migration(mod, table):
    d = os.path.join(REPO, mod, 'database', 'migrations')
    f = next(x for x in sorted(os.listdir(d)) if x.endswith('create_%s_table.php' % table) and x[0] == '2')
    return read(mod, 'database/migrations/' + f)


def between(text, start, end):
    """Potongan teks dari baris yang memuat `start` sampai baris yang memuat `end` (inklusif), di-dedent."""
    lines = text.split('\n')
    i = next(k for k, l in enumerate(lines) if start in l)
    j = next(k for k in range(i, len(lines)) if end in lines[k])
    return textwrap.dedent('\n'.join(lines[i:j + 1]))


def asset(name):
    return os.path.join(ASSETS, name)

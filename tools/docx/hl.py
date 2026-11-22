"""Highlighter sederhana dengan palet blok kode Modul 09/10."""
import re

DEF = 'ECEAE6'
KW = 'E8806F'
STR = '7CC08E'
FN = '8FB0DE'
CLS = 'EBBF9C'
VAR = 'E3A97C'
NUM = 'E6BB5E'
COM = '8E8A85'

PHP_KW = set('''abstract and as break case catch class clone const continue declare default do echo else elseif
empty enddeclare endfor endforeach endif endswitch endwhile extends final finally fn for foreach function global if
implements include instanceof interface isset list match namespace new or private protected public readonly require
return static switch throw trait try unset use var while yield true false null self parent void string int array'''.split())


def _php_tokens(s):
    """Token PHP: (teks, warna, miring)."""
    pat = re.compile(r'''
        (?P<com>//[^\n]*|/\*.*?\*/|\#[^\n]*)
      | (?P<open><\?php)
      | (?P<str>'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")
      | (?P<var>\$[A-Za-z_]\w*)
      | (?P<num>\b\d+\b)
      | (?P<name>\\?[A-Za-z_][\w\\]*)
      | (?P<other>\s+|.)
    ''', re.X | re.S)
    out = []
    toks = list(pat.finditer(s))
    for i, m in enumerate(toks):
        k = m.lastgroup
        t = m.group()
        if k == 'com':
            out.append((t, COM, True))
        elif k == 'open':
            out.append((t, KW, False))
        elif k == 'str':
            out.append((t, STR, False))
        elif k == 'var':
            out.append((t, VAR, False))
        elif k == 'num':
            out.append((t, NUM, False))
        elif k == 'name':
            nxt = s[m.end():m.end() + 1]
            prev = s[max(0, m.start() - 2):m.start()]
            if t.lower() in PHP_KW and prev not in ('->', '::'):
                out.append((t, KW, False))
            elif nxt == '(':
                out.append((t, FN if not t[0].isupper() or prev in ('->', '::') else CLS, False))
            elif t[0].isupper() or '\\' in t:
                out.append((t, CLS, False))
            else:
                out.append((t, DEF, False))
        else:
            out.append((t, DEF, False))
    return out


def php(line):
    return _php_tokens(line)


def blade(line):
    """HTML + Blade."""
    out = []
    pat = re.compile(r'''
        (?P<bcom>\{\{--.*?--\}\})
      | (?P<hcom><!--.*?-->)
      | (?P<doctype><!DOCTYPE[^>]*>)
      | (?P<echo>\{\{.*?\}\}|\{!!.*?!!\})
      | (?P<dir>@[A-Za-z]+(?:\((?:[^()]|\([^()]*\))*\))?)
      | (?P<tagopen></?[A-Za-z][\w.-]*)
      | (?P<tagclose>/?>)
      | (?P<text>[^<{@>]+|.)
    ''', re.X)
    in_tag = False
    for m in pat.finditer(line):
        k, t = m.lastgroup, m.group()
        if k == 'bcom':
            out.append((t, COM, True))
        elif k == 'hcom':
            out.append((t, COM, True))
        elif k == 'doctype':
            out.append((t, COM, False))
        elif k == 'echo':
            o = 3 if t.startswith('{!!') else 2
            out.append((t[:o], FN, False))
            out += _php_tokens(t[o:-o])
            out.append((t[-o:], FN, False))
        elif k == 'dir':
            mm = re.match(r'(@[A-Za-z]+)(.*)', t)
            out.append((mm.group(1), FN, False))
            if mm.group(2):
                out += _php_tokens(mm.group(2))
        elif k == 'tagopen':
            out.append((t, KW, False))
            in_tag = True
        elif k == 'tagclose':
            out.append((t, KW, False))
            in_tag = False
        else:
            if in_tag:
                for mm in re.finditer(r'"[^"]*"|\'[^\']*\'|[A-Za-z_:][\w:.-]*|\s+|.', t):
                    x = mm.group()
                    if x[0] in '"\'':
                        # atribut berisi blade echo
                        if '{{' in x:
                            out.append((x[0], STR, False))
                            out += blade(x[1:-1])
                            out.append((x[-1], STR, False))
                        else:
                            out.append((x, STR, False))
                    elif re.match(r'[A-Za-z_:]', x):
                        out.append((x, CLS, False))
                    else:
                        out.append((x, DEF, False))
            else:
                out.append((t, DEF, False))
    return out


def bash(line):
    if line.lstrip().startswith('#'):
        return [(line, COM, True)]
    out = []
    first = True
    for m in re.finditer(r'"[^"]*"|\'[^\']*\'|<[^>]+>|\s+|[^\s]+', line):
        t = m.group()
        if t.isspace():
            out.append((t, DEF, False))
        elif first:
            out.append((t, FN, False))
            first = False
        elif t[0] in '"\'':
            out.append((t, STR, False))
        elif t.startswith('<'):
            out.append((t, VAR, False))
        elif t.startswith('-'):
            out.append((t, NUM, False))
        else:
            out.append((t, DEF, False))
    return out


def env(line):
    if line.lstrip().startswith('#'):
        return [(line, COM, True)]
    if '=' in line:
        k, v = line.split('=', 1)
        return [(k, CLS, False), ('=', DEF, False), (v, STR, False)]
    return [(line, DEF, False)]


def sql(line):
    out = []
    kws = set('select from left join on where as insert into values delete update set create database table and or'.split())
    for m in re.finditer(r"'[^']*'|\w+|\s+|.", line):
        t = m.group()
        if t.lower() in kws:
            out.append((t, KW, False))
        elif t.startswith("'"):
            out.append((t, STR, False))
        else:
            out.append((t, DEF, False))
    return out


LEXERS = {'PHP': php, 'HTML': blade, 'BLADE': blade, 'BASH': bash, 'ENV': env, 'SQL': sql, 'TEXT': lambda l: [(l, DEF, False)]}


def merge(tokens):
    out = []
    for t, c, i in tokens:
        if not t:
            continue
        if out and out[-1][1] == c and out[-1][2] == i:
            out[-1] = (out[-1][0] + t, c, i)
        else:
            out.append((t, c, i))
    return out


def highlight(lang, line):
    return merge(LEXERS[lang](line))

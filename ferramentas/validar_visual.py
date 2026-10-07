#!/usr/bin/env python3
"""Valida roteiro + visual v2 antes do render (pega o que o hyperframes check reprovaria).

  - todo `at`/`*_at` existe literalmente na fala da cena ("trecho#2" = 2ª ocorrência)
  - aviso se o trecho aparece mais de uma vez na cena e não tem #n (casa com a primeira)
  - `label` de shot ≤ 40 caracteres (sem **)
  - `labels` do roteiro: ≤ 4 em kind compare, ≤ 5 nas demais

Uso: validar_visual.py <roteiro/pt.json> <visual/pt-b01.json> [<visual/pt-b02.json> ...]
Sai com código 1 se houver erro.
"""
import json, re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^\w\s-]', ' ', s).split()

def hits(words, cue):
    c = norm(cue)
    return [i for i in range(len(words)) if c and words[i:i + len(c)] == c]

def cues(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if (k == 'at' or k.endswith('_at')) and isinstance(v, str): acc.append(v)
            else: cues(v, acc)
    elif isinstance(o, list):
        for x in o: cues(x, acc)

def shots(o):
    if isinstance(o, dict):
        if 'type' in o: yield o
        for v in o.values(): yield from shots(v)
    elif isinstance(o, list):
        for x in o: yield from shots(x)

roteiro = json.load(open(sys.argv[1]))
roteiro = roteiro['scenes'] if isinstance(roteiro, dict) else roteiro
erros = avisos = 0
for i, s in enumerate(roteiro, 1):
    lim = 4 if s.get('kind') == 'compare' else 5
    if len(s.get('labels', [])) > lim:
        print(f'ERRO roteiro cena {i}: {len(s["labels"])} labels (máx {lim} em {s.get("kind")})'); erros += 1
for f in sys.argv[2:]:
    v = json.load(open(f))
    for num, sc in v['scenes'].items():
        words = norm(roteiro[int(num) - 1]['speech'])
        acc = []; cues(sc, acc)
        for c in acc:
            base, _, k = c.partition('#'); h = hits(words, base)
            if len(h) < int(k or 1):
                print(f'ERRO {f} cena {num}: cue não está na fala: {c!r}'); erros += 1
            elif len(h) > 1 and not k:
                print(f'aviso {f} cena {num}: {c!r} aparece {len(h)}x, casa com a 1ª'); avisos += 1
        for sh in shots(sc):
            lab = (sh.get('label') or '').replace('**', '')
            if len(lab) > 40:
                print(f'ERRO {f} cena {num}: label com {len(lab)} caracteres (máx 40): {lab!r}'); erros += 1
print('OK' if not erros else f'{erros} erro(s)', f'{avisos} aviso(s)')
sys.exit(1 if erros else 0)

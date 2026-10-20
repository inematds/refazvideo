#!/usr/bin/env python3
"""Corta da referência os trechos animados listados em lista.json ([[ini, fim, nome.mp4], ...]), sem áudio.
Uso: cortar.py --src <video.mp4> --rosto <rosto.json> --dir <pasta dos clipes> [--caixa x,y,w,h] [--livre ate_s] [--refaz]
- trecho com o apresentador em tela cheia: avisa (ajustar ini/fim ou confirmar na folha que é página branca);
- apresentador no canto (pip a ±1,5 s do trecho): coberto com delogo na --caixa (padrão 1560,240,355,500);
- --livre N: trechos que terminam até N s não levam cobertura (ex.: abertura com foto de pessoas no canto).
Depois monta folhaNN.jpg (início/meio/fim de cada clipe) para conferir antes do render."""
import argparse, json, subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True); ap.add_argument('--rosto', required=True); ap.add_argument('--dir', required=True)
ap.add_argument('--caixa', default='1560,240,355,500'); ap.add_argument('--livre', type=float, default=0)
ap.add_argument('--refaz', action='store_true')
a = ap.parse_args()
D = Path(a.dir); R = json.load(open(a.rosto)); lista = json.load(open(D / 'lista.json'))
x, y, w, h = a.caixa.split(',')
erros, feitos = [], set()
for ini, fim, nome in lista:
    if nome in feitos: continue
    feitos.add(nome)
    cheia = [q['t'] for q in R if ini <= q['t'] <= fim and q['full']]
    if cheia: erros.append(f'{nome}: tela cheia em {cheia}')
    pip = any(q['pip'] for q in R if ini - 1.5 <= q['t'] <= fim + 1.5) and fim > a.livre
    vf = (f'delogo=x={x}:y={y}:w={w}:h={h},' if pip else '') + 'format=yuv420p'
    out = D / nome
    if a.refaz or not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ini), '-i', a.src, '-t', f'{fim - ini:.2f}', '-an', '-vf', vf,
                        '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-g', '15', '-movflags', '+faststart', str(out)], check=True)
tmp = D / 'folha'; tmp.mkdir(exist_ok=True)
for f in tmp.glob('*.jpg'): f.unlink()
for f in D.glob('folha*.jpg'): f.unlink()
k = 0
for ini, fim, nome in lista:
    for frac in (0.05, 0.5, 0.95):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{(fim - ini) * frac:.2f}', '-i', str(D / nome), '-frames:v', '1',
                        '-vf', f"scale=320:-1,drawtext=text='{ini:.0f}':x=4:y=4:fontsize=22:fontcolor=yellow:box=1", str(tmp / f'{k:04d}.jpg')])
        k += 1
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-pattern_type', 'glob', '-i', str(tmp / '*.jpg'), '-vf', 'tile=9x8', str(D / 'folha%02d.jpg')])
print('clipes:', len(feitos), '| folhas:', sorted(p.name for p in D.glob('folha*.jpg')))
print('\n'.join(erros) if erros else 'sem tela cheia')

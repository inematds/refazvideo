#!/usr/bin/env python3
"""Mapa do rosto do apresentador da referência, 2 quadros por segundo.
Uso: rosto_mapa.py <video.mp4> <saida.json>
Cada item: {t, full, pip, n}
- full: quadro claro (média de luz > 70) = apresentador em tela cheia (fundo cinza). Página branca também
  dispara (falso positivo): conferir na folha e, se for página, pode usar o trecho.
- pip: caixa [x0,y0,x1,y1] da pele no canto direito (x > 82% da largura), em pixels 1920x1080.
Calibrado em telas escuras (hhHkaZRwBBU). Em referência de fundo claro, revisar os limiares."""
import json, subprocess, sys
import numpy as np

src, saida = sys.argv[1], sys.argv[2]
W, H = 384, 216
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps=2,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                   capture_output=True, check=True)
a = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3).astype(int)
x0 = int(W * 0.82)
out = []
for i, f in enumerate(a):
    full = f.mean(axis=2).mean() > 70
    r = f[:, x0:, :]
    skin = (r[..., 0] > 120) & (r[..., 0] > r[..., 1] + 15) & (r[..., 1] > r[..., 2]) & (r.mean(axis=2) > 90)
    ys, xs = np.nonzero(skin)
    box = [int((xs.min() + x0) * 5), int(ys.min() * 5), int((xs.max() + x0) * 5), int(ys.max() * 5)] if len(ys) > 40 else None
    out.append({'t': i / 2, 'full': bool(full), 'pip': box, 'n': int(len(ys))})
json.dump(out, open(saida, 'w'))

def trechos(chave):
    r, ini = [], None
    for x in out:
        if x[chave] and ini is None: ini = x['t']
        if not x[chave] and ini is not None: r.append((ini, x['t'])); ini = None
    if ini is not None: r.append((ini, out[-1]['t']))
    return r
print('tela cheia:', trechos('full'))
print('canto:', [t for t in trechos('pip') if t[1] - t[0] >= 1])

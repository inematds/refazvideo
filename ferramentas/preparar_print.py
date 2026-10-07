#!/usr/bin/env python3
"""Prepara um print da referência para o shot `media` do explicavideos v2.

  --cobrir x,y,w,h   (repetível) cobre a área (px) com um bloco liso da cor do fundo — para webcam/rosto.
                     Não use blur: vira mancha colorida.
  --modo linha|bloco  linha (padrão): cada linha recebe a cor vizinha da esquerda; bloco: cor única de --cor.
  --cor x,y          ponto de onde tirar a cor do fundo (padrão: x=20, 30 px acima da borda inferior).
  --crop x,y,w,h     recorta antes de tudo (ex.: slide à esquerda e webcam à direita).
  --pad              acrescenta margens laterais da cor do fundo até 2052×1080 (slide estreito cabe no quadro 1330×700).

Uso: preparar_print.py entrada.png saida.png [--crop ...] [--cobrir ...] [--cor x,y] [--pad]
"""
import argparse
from collections import Counter
from PIL import Image, ImageDraw

def box(s): return tuple(int(v) for v in s.split(','))

ap = argparse.ArgumentParser()
ap.add_argument('entrada'); ap.add_argument('saida')
ap.add_argument('--crop', type=box)
ap.add_argument('--cobrir', type=box, action='append', default=[])
ap.add_argument('--cor', type=box, default=None)
ap.add_argument('--pad', action='store_true')
ap.add_argument('--modo', choices=['linha', 'bloco'], default='linha')
a = ap.parse_args()

im = Image.open(a.entrada).convert('RGB')
if a.crop:
    x, y, w, h = a.crop; im = im.crop((x, y, x + w, y + h))
cor = im.getpixel(a.cor or (20, im.height - 30))
d = ImageDraw.Draw(im)
for x, y, w, h in a.cobrir:
    if a.modo == 'bloco':
        d.rectangle((x, y, x + w - 1, y + h - 1), fill=cor); continue
    # linha: cada linha recebe a cor mais comum da faixa logo à esquerda da área — continua fundo, barras e linhas
    # horizontais da própria tela, sem deixar mancha (use uma caixa que inclua a sombra da webcam).
    px = im.load()
    for yy in range(y, min(y + h, im.height)):
        faixa = [px[xx, yy] for xx in range(max(0, x - 160), max(1, x - 4))]
        q = Counter(tuple(v // 6 for v in c) for c in faixa).most_common(1)[0][0]
        med = next(c for c in faixa if tuple(v // 6 for v in c) == q)  # cor mais comum (fundo vence o texto)
        d.line((x, yy, min(x + w, im.width) - 1, yy), fill=med)
if a.pad:
    W = max(im.width, round(im.height * 2052 / 1080))
    bg = Image.new('RGB', (W, im.height), cor); bg.paste(im, ((W - im.width) // 2, 0)); im = bg
im.save(a.saida)
print(a.saida, im.size, 'cor', cor)

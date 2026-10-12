#!/usr/bin/env python3
"""Tira o amarelado que o gerador de imagem (Codex image_gen) põe nas fotos.

  python3 cor_neutra.py medir   img1.png img2.png ...    só mede
  python3 cor_neutra.py corrigir img1.png img2.png ...   corrige no lugar (guarda <nome>-orig.png na 1ª vez)

Medida: amarelo = (R+G)/2 - B da imagem inteira (0-255). Foto neutra fica em 0-10; o gerador entrega 25-55.
Acima de 18 a imagem é puxada para o cinza até ~12 (mantém o calor da pele). Idempotente.
Mesma regra do portão de imagens do reel7etapas (cmd cor). Imagem que PRECISA ser quente (fogo, pôr do sol): não passe.
"""
import shutil, sys
from pathlib import Path
from PIL import Image, ImageStat

CORRIGE, ALVO = 18.0, 12.0


def amarelo(im):
    r, g, b = ImageStat.Stat(im.convert("RGB").resize((256, 256))).mean
    return (r + g) / 2 - b


def corrigir(a):
    im = Image.open(a).convert("RGB"); antes = amarelo(im)
    if antes <= CORRIGE:
        return antes, antes
    orig = a.with_name(a.stem + "-orig" + a.suffix)
    if not orig.exists():
        shutil.copy2(a, orig)
    r, g, b = ImageStat.Stat(im.resize((256, 256))).mean; cinza = (r + g + b) / 3
    for k in range(1, 21):
        gs = [(cinza / c) ** (k / 20) for c in (r, g, b)]
        out = Image.merge("RGB", [ch.point(lambda v, m=m: min(255, int(v * m + .5))) for ch, m in zip(im.split(), gs)])
        if amarelo(out) <= ALVO:
            break
    out.save(a); return antes, amarelo(out)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("medir", "corrigir"):
        sys.exit(__doc__)
    for p in map(Path, sys.argv[2:]):
        if sys.argv[1] == "medir":
            v = amarelo(Image.open(p)); print(f"{p.name}: amarelo {v:.0f}{'  ← corrigir' if v > CORRIGE else ''}")
        else:
            antes, depois = corrigir(p); print(f"{p.name}: {antes:.0f} → {depois:.0f}")

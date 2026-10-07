#!/usr/bin/env python3
"""Storyboard HTML (prévia para aprovação): cena → fala → prints da referência.

Uso: montar_storyboard.py <OUT> <mapa.json>
  mapa.json: lista com 1 item por cena, cada um a lista dos tempos (s) dos prints, ex. [[33],[39],[63,93],[]]
  Lê <OUT>/roteiro/pt.json e <OUT>/media/s-<t>.png; usa o modelo exemplos/decisions-jev/storyboard-template.html.
  Grava <OUT>/preview/storyboard.html (imagens embutidas; publicar como Artifact ou abrir no navegador).
"""
import base64, io, json, pathlib, sys
from PIL import Image

out = pathlib.Path(sys.argv[1]); MAP = json.loads(pathlib.Path(sys.argv[2]).read_text())
tpl = pathlib.Path(__file__).resolve().parent.parent / 'exemplos/decisions-jev/storyboard-template.html'
scenes = json.loads((out / 'roteiro/pt.json').read_text())

def jpg(t):
    im = Image.open(out / f'media/s-{t}.png').convert('RGB'); im.thumbnail((1100, 1100))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=72)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

imgs = {t: jpg(t) for m in MAP for t in m}
html = tpl.read_text().replace('__SCENES__', json.dumps(scenes, ensure_ascii=False)) \
    .replace('__IMGS__', json.dumps(imgs)).replace('__MAP__', json.dumps(MAP))
(out / 'preview').mkdir(exist_ok=True)
(out / 'preview/storyboard.html').write_text(html)
print(out / 'preview/storyboard.html', len(html) // 1024, 'KB')

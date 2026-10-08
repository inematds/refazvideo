# telas_pt — refazer as telas da referência em português

Kit usado no vídeo "AI harness" (ref. lNum1UFDYn0, 07/10/2026): 12 quadros brancos refeitos em PT, 49 PNGs.

- `base.css` — estilo quadro branco (caixas `.b` + cor `.y .bl .pk .gr .or .vi .gy .tq`, texto `.t`, centro `.c`, rodapé `.foot`).
- `base.js` — ícones (`<i class="ic" data-i="robot|brain|doc|terminal|…" data-s="80">`), setas (`marker-end="url(#ar|#ag|#ab)"`),
  etapas (`data-step="N"`, `data-ate="N"`) e `fit()` (caixa curta para o texto em PT alarga até +25% e reduz a fonte até 80%).
- `render.mjs` — renderiza todo `NN-*.html` da pasta em cada etapa para `../media/pt/` e avisa texto vazando e fonte ausente.
- `Excalifont.woff2` — subconjunto latino da Excalifont (Excalidraw, SIL OFL 1.1), com ç ã õ é í ú â ê ô.

Coordenadas em espaço 1920×1080 (dá para copiar as posições do quadro original); a página tem 2052×1080 para o shot `media`.

# Lições (mais recente no topo)

| data | o que quebrou | proteção |
|---|---|---|
| 2026-10-07 | Rosto do autor apareceu a partir de 4 min: a webcam estava no canto SUPERIOR nos prints 453/471 e eu cobri o inferior (mesma caixa para todos) | Localizar a webcam em cada print (folha de recortes do canto) e usar a caixa certa por print |
| 2026-10-07 | Bloco liso sobre a webcam ficou evidente ("escondeu, mas ficou claro") | `--modo linha`: cada linha recebe a cor mais comum da faixa à esquerda, continuando o fundo |
| 2026-10-07 | Blur (boxblur) na webcam do apresentador original virou mancha rosa visível no print | Cobrir com retângulo liso da cor do fundo (`preparar_print.py --cobrir`) |
| 2026-10-07 | v2: `label` de shot `media` com 42–48 caracteres sobrepôs a legenda da fala (`content_overlap`) | `label` ≤ 40 caracteres (39–40 passaram) (checado em `validar_visual.py`) |
| 2026-10-07 | v1: cenas `compare` com 6–7 `labels` estouraram o quadro no `hyperframes check` | `labels` ≤ 4 em `compare`, ≤ 5 nas demais (checado em `validar_visual.py`) |
| 2026-10-07 | v1: CUDA out of memory no Whisper local (GPU dividida); `produce_blocks.py` marca `failed` e não repete | Zerar a chave em `production.json` e subir o render de novo |
| 2026-10-07 | `build_block --strict` avisou 10–11 s sem mudança visual | Acrescentar highlight/statement com cue no meio do trecho |
| 2026-10-07 | Cue "e a Decisions API" existia 2× na cena e casou com a primeira (antes do shot) | Usar trecho único ou `"trecho#2"` |
| 2026-10-07 | HeyGen ficou ~1 h em 0% e depois terminou em minutos; o 2º bloco só começa depois do 1º | Esperar (baixador com até 2 h por bloco); não reenviar |

# refazvideo — playbook do agente

Você recebe um **pedido** (`PEDIDO.md`, modelo em `modelos/pedido.md`) com **assunto** e **vídeo de referência**
e entrega um vídeo novo, em português, com o avatar e a voz do apresentador (HeyGen), telas reais da
referência e animações. A produção roda no **explicavideos** (`~/projetos/explicavideos`); este projeto
é o método e as ferramentas em volta dele.

Caso real completo: `exemplos/decisions-jev/` (vídeo publicado: https://www.youtube.com/watch?v=p34w1bBPjpc).

## Regras que não mudam

- **Não citar o autor/canal da referência** (nem na fala, nem na tela, nem na descrição) se o pedido disser.
  Rosto do apresentador original nunca aparece: cobrir a webcam com **bloco liso da cor do fundo** (blur vira mancha).
- **Termos técnicos não se traduzem** (API, evidence, choice, refusal…). A fala é PT natural; a tela pode
  manter o print em inglês.
- **HeyGen custa crédito.** Só enviar com o "pode fazer" explícito do dono no momento, gravado em
  `<out>/v1/APROVADO_HEYGEN` (data, blocos, minutos). Pelo **estúdio** (`heygen-studio.mjs`), nunca pela API.
- Nada de API sem autorização explícita (exceto o que o dono liberar). Publicar no YouTube só quando pedido.
- Tetos sempre: `systemd-run --user --scope -p MemoryMax=16G -p MemorySwapMax=0` em render/transcrição.

## Pastas

`OUT=~/projetos/output/explica-<id-do-video>/` com `src/ frames/ media/ roteiro/ visual/ preview/ v1/ v2/`.

## Passo a passo

1. **Baixar e transcrever a referência** (inemavox):
   `python3 ~/projetos/inemavox/baixar_v1.py --url <URL> --outdir $OUT/src --quality 1080p`
   `python3 ~/projetos/inemavox/transcrever_v1.py --in $OUT/src/video.mp4 --outdir $OUT/src --whisper-model large-v3`
2. **Ver o vídeo**: `ferramentas/extrair_frames.sh $OUT` → folhas `frames/sheet*.jpg` (1 quadro a cada 6 s,
   numerados). Escolher os tempos com telas úteis (slides, demos, tabelas).
3. **Prints**: `ffmpeg -ss <t> -i src/video.mp4 -frames:v 1 media/raw-<t>.png`, depois
   `ferramentas/preparar_print.py` — `--cobrir x,y,w,h` (webcam/rosto) e `--pad` (slide estreito → 2052×1080
   para caber no quadro 1330×700 do shot `media`).
4. **Roteiro** `roteiro/pt.json`: lista de cenas `{chapter,title,kind,labels,takeaway,source,speech,svg:null}`
   (modelo: `exemplos/decisions-jev/roteiro-pt.json`). Reescrever, não traduzir frase a frase. ~150 palavras/min.
   `labels`: **≤ 4 em `kind: compare`, ≤ 5 nas demais**, curtos. Fecha com CTA "inema ponto club".
5. **Prévia para o dono**: storyboard (cena → fala → prints). Esperar o "pode fazer".
6. **Config explicavideos**: copiar `modelos/config-v1.json` e `modelos/config-v2.json` para
   `~/projetos/explicavideos/examples/<id>.json` e `<id>-v2.json` (trocar `<ID>`, `<OUT>`, `whisper_prompt`
   com nomes e termos). `EXPLICAVIDEOS_CONFIG=examples/<id>.json python3 explica.py prepare` → `v1/blocos/`.
7. **HeyGen pelo estúdio** (após APROVADO_HEYGEN), por bloco, com Xvfb `:99` no ar:
   `DISPLAY=:99 node engine/heygen-studio.mjs --titulo <TÍTULO> --fala-arquivo $OUT/v1/blocos/pt-bNN.txt --perfil ~/.cache/inemaccbot/perfil-heygen --template TEMPLATE-AVATAR16`
   Gravar o id (`create-v4/<id>` do log) no `manifest.json` (`status: submitted`, `via: estudio`).
   Baixar: `ferramentas/baixa_blocos.sh $OUT` (espera até 2 h por bloco; HeyGen fica em 0% um bom tempo e depois anda).
8. **Render v1** (sincroniza avatar e fala; não suba `submit`, `monitor` nem `publish`):
   unidades `render` (`engine/produce_blocks.py`) e `assemble` (`engine/wait_assembly.py`) via `systemd-run`
   (comando exato em `exemplos/decisions-jev/COMANDOS.md`). Pronto quando existir `v1/verification/assembled-pt.json`.
   Falha em `v1/verification/production.json` → corrigir, zerar a chave e subir o render de novo.
9. **Visual v2** `visual/pt-bNN.json` (contrato em `~/projetos/explicavideos/engine/v2/AUTHORING.md`; modelo em
   `exemplos/decisions-jev/`). Cada `at` é um trecho literal de 1–5 palavras da fala daquela cena; repetido → `"trecho#2"`.
   Trocar o visual a cada ≤ 10 s. `label` de `media` **≤ 40 caracteres**.
   Validar: `ferramentas/validar_visual.py $OUT/roteiro/pt.json $OUT/visual/pt-b*.json` → `OK`.
10. **Render v2**: `setup_output.py` → copiar `visual/*.json` para `v2/visual-v2/` → `build_block.py N --strict`
    (zero warnings) → `run_lane.sh 1 2 …` → `assemble_languages.py`. Final: `v2/final/<id>-pt.mp4`.
11. **Conferir quadros** (folha de 11 quadros espalhados) antes de entregar: rosto alheio, texto cortado, sobreposição.
12. **Entregar**: bot v3 (`ferramentas/enviar_bot_v3.mjs`, ≤ 49 MB → cópia 720p) e/ou YouTube
    (`~/projetos/yt-pubx/yt-pubx publicar … --dry-run`, olhar thumb, publicar com `--plano`).

## Armadilhas já vistas (ver `LICOES.md`)

CUDA OOM no Whisper do v1 (repetir), `compare` com 6–7 labels estoura o quadro, label longo encosta na
legenda, blur do rosto vira mancha, cue que aparece duas vezes na cena casa com a primeira.

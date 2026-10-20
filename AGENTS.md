# refazvideo — playbook do agente

Você recebe um **pedido** (`PEDIDO.md`, modelo em `modelos/pedido.md`) com **assunto** e **vídeo de referência**
e entrega um vídeo novo, em português, com o avatar e a voz do apresentador (HeyGen), telas reais da
referência e animações. A produção roda no **explicavideos** (`~/projetos/explicavideos`); este projeto
é o método e as ferramentas em volta dele.

Caso real completo: `exemplos/decisions-jev/` (vídeo publicado: https://www.youtube.com/watch?v=O2061m5FG_I).

## Regras que não mudam

- **Sem crédito da fonte** (dono, 08/10/2026: "a gente está construindo tudo e validando"): a fala não cita o autor
  da referência e **nada escrito** no vídeo nem na descrição do YouTube; o takeaway final é a frase-síntese do vídeo.
  Só pôr crédito se o pedido disser explicitamente.
- **Rosto do apresentador original nunca aparece.** A webcam muda de lugar entre os trechos do vídeo: conferir
  **cada print** e cobrir com `preparar_print.py --cobrir` (modo `linha`, continua o fundo da tela; caixa incluindo a
  sombra). Blur vira mancha; bloco liso fica evidente. Conferir com uma folha dos prints antes do render.
- **Termos técnicos não se traduzem** (API, evidence, choice, refusal…). A fala é PT natural; a tela pode
  manter o print em inglês.
- **HeyGen custa crédito.** Só enviar com o "pode fazer" explícito do dono no momento, gravado em
  `<out>/v1/APROVADO_HEYGEN` (data, blocos, minutos). Pelo **estúdio** (`heygen-studio.mjs`), nunca pela API.
- Nada de API sem autorização explícita (exceto o que o dono liberar). Publicar no YouTube só quando pedido.
- Tetos sempre: `systemd-run --user --scope -p MemoryMax=16G -p MemorySwapMax=0` em render/transcrição.

## Pastas

`OUT=~/projetos/output/explica-<id-do-video>/` com `src/ frames/ media/ roteiro/ visual/ preview/ v1/ v2/`.

## Três modos: clipes, aula ou viral

- **`modo clipes`** (PADRÃO quando a referência é um explicativo com animações/diagramas — 20/10/2026): o visual do
  nosso vídeo são **os próprios trechos animados da referência**, cortados e sincronizados com a fala PT do Nei.
  Foi o que o dono pediu ao dizer "refazvideo": no ia-crescendo (hhHkaZRwBBU) eu fiz viral com artes novas e telas
  redesenhadas e ele reprovou ("as imagens, os exemplos, as animações, nada disso temos no nosso vídeo").
  Passos (depois do roteiro e do avatar, 1–8):
  1. Texto da referência: primeiro a **legenda do YouTube** (`yt-dlp --skip-download --write-subs --write-auto-subs
     --sub-langs en`); Whisper/Parakeet só sem legenda.
  2. `ferramentas/clipes/rosto_mapa.py src/video.mp4 clips/rosto.json` → trechos com o apresentador em tela cheia
     (fora) e no canto (cobertos).
  3. Folhas de 6 s (`extrair_frames.sh`) + legenda com tempos → para cada deixa da fala PT, o trecho `[ini, fim]` do
     original que mostra a mesma coisa. Escrever `visual/gerar_visual.py` com `c("deixa", ini, fim)` (modelo:
     `exemplos/ia-crescendo/gerar_visual.py`): gera `visual/pt-bNN.json` (shot `media` com `.mp4`) e `clips/lista.json`.
  4. `ferramentas/clipes/cortar.py --src src/video.mp4 --rosto clips/rosto.json --dir clips` → clipes mudos, canto
     coberto com `delogo`, e `clips/folhaNN.jpg` (início/meio/fim de cada um). **Ler as folhas**: nenhum rosto do autor;
     aviso de "tela cheia" em página branca é falso positivo, em rosto é ajustar `ini`.
  5. `build_block.py N --strict` sem avisos (trecho curto congela no último quadro: se acusar > 10 s parado, pôr outro
     trecho na fala seguinte) → render → folha de 16 quadros do final.
  Parte da fala que o original não tem (dicas, CTA) usa telas PT ou statement.
  Caso real: ia-crescendo, 82 trechos, 7min05, https://www.youtube.com/watch?v=Fgfzax3fibo.
- **`modo aula`** (vídeo longo/didático de slides ou quadro branco): o passo a passo abaixo, explicavideos v2 de sempre.
- **`modo viral`** (reel, notícia, número; "refaz esse reel", "de forma viral"): mesma entrada (passos 1–8: baixar,
  fatos, roteiro, 1 gravação HeyGen, v1), mas o visual é o **perfil viral** do explicavideos:
  `"profile_visual": "viral"` na config v2 (16:9 e `-916` com `reel_profile`), peças de tela cheia
  (`capa`, `foto`, `capitulo`, `bignum`, `escala`, `barra`, `carimbo`, `cinetica`, `rosto`, `cta`), troca ≤ 2 s,
  `som_viral.py` (trilha + efeitos locais) e `qa_viral.py` (reprova tela vazia/parada). Regras e contrato:
  `~/projetos/explicavideos/engine/v2/PADRAO-VIRAL.md`. Molde completo (visual, configs, script):
  `~/projetos/output/explica-DeQDKiBglmh/` (`visual/viral-pt-b01.json`, `piloto_viral.sh`).
  O TeraFab no modo aula foi reprovado ("apresentação muito ruim"); no viral, aprovado.

## Passo a passo

1. **Baixar e transcrever a referência** (inemavox):
   `python3 ~/projetos/inemavox/baixar_v1.py --url <URL> --outdir $OUT/src --quality 1080p`
   `python3 ~/projetos/inemavox/transcrever_v1.py --in $OUT/src/video.mp4 --outdir $OUT/src --whisper-model large-v3`
2. **Ver o vídeo**: `ferramentas/extrair_frames.sh $OUT` → folhas `frames/sheet*.jpg` (1 quadro a cada 6 s,
   numerados). Escolher os tempos com telas úteis (slides, demos, tabelas).
3. **Prints**: `ffmpeg -ss <t> -i src/video.mp4 -frames:v 1 media/raw-<t>.png`, depois
   `ferramentas/preparar_print.py` — `--cobrir x,y,w,h` (webcam/rosto) e `--pad` (slide estreito → 2052×1080
   para caber no quadro 1330×700 do shot `media`).
   **Telas refeitas em PT** (quando o dono pedir, ou a referência for quadro branco/slides com texto): copiar
   `ferramentas/telas_pt/` para `$OUT/telas-pt/`, escrever um `NN-<slug>.html` por tela (modelo: `exemplo-*.html`;
   elementos com `data-step` montam em etapas, `data-ate` some depois), `node render.mjs` → `media/pt/NN-<slug>-sK.png`
   (2052×1080, Excalifont com acentos). Conferir numa folha antes do storyboard. Sem print original → sem webcam para cobrir.
4. **Roteiro** `roteiro/pt.json`: lista de cenas `{chapter,title,kind,labels,takeaway,source,speech,svg:null}`
   (modelo: `exemplos/decisions-jev/roteiro-pt.json`). Reescrever, não traduzir frase a frase. ~150 palavras/min.
   `labels`: **≤ 4 em `kind: compare`, ≤ 5 nas demais**, curtos. Fecha com CTA "inema ponto club".
5. **Prévia para o dono**: storyboard (cena → fala → prints). Esperar o "pode fazer".
6. **Config explicavideos**: copiar `modelos/config-v1.json` e `modelos/config-v2.json` para
   `~/projetos/explicavideos/examples/<id>.json` e `<id>-v2.json` (trocar `<ID>`, `<OUT>`, `whisper_prompt`
   com nomes e termos). `python3 explica.py --config examples/<id>.json prepare` (o env EXPLICAVIDEOS_CONFIG é ignorado pelo explica.py) → `v1/blocos/`.
   Se o `prepare` recusar ("Generation started…"), rodar `engine/prepare.py` **e** `engine/build_scene_templates.py` (sem os templates o render v1 falha com `templates/pt/scene-01.html` ausente).
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
   Trocar o visual a cada ≤ 10 s. Ilustração: `media` com `calm: true` (dissolve, imagem inteira) e re-enquadramento da mesma imagem com `cont`+`from`, zoom ≤ 1,25 (o Nei reprovou choque e close que corta texto, 09/10). `label` de `media` **≤ 40 caracteres**.
   **Abertura obrigatória:** cena 1 começa com shot `hook` em `"at": "@start"` (imagem de impacto gerada no flux2-klein local
   + promessa de 3–6 palavras) e, na frase "neste vídeo eu explico…", uma grade-prévia do conteúdo com um quadro "no fim: …"
   (gatilho de atenção). O roteiro de fala deve anunciar o que vem logo no começo.
   Validar: `ferramentas/validar_visual.py $OUT/roteiro/pt.json $OUT/visual/pt-b*.json` → `OK`.
10. **Render v2**: `setup_output.py` → copiar `visual/*.json` para `v2/visual-v2/` → `build_block.py N --strict`
    (zero warnings) → `run_lane.sh 1 2 …` → `assemble_languages.py`. Final: `v2/final/<id>-pt.mp4`.
11. **Conferir quadros** (folha de 11 quadros espalhados) antes de entregar: rosto alheio, texto cortado, sobreposição.
12. **Entregar**: bot v3 (`ferramentas/enviar_bot_v3.mjs`, ≤ 49 MB → cópia 720p) e/ou YouTube
    (`~/projetos/yt-pubx/yt-pubx publicar … --dry-run`, olhar thumb, publicar com `--plano`).

## Armadilhas já vistas (ver `LICOES.md`)

CUDA OOM no Whisper do v1 (repetir), `compare` com 6–7 labels estoura o quadro, label longo encosta na
legenda, blur do rosto vira mancha, cue que aparece duas vezes na cena casa com a primeira.

# Decisions API × Jev — o que foi rodado (07/10/2026)

Referência: https://www.youtube.com/watch?v=uTU5Ihgl_7Q (9m38s, inglês). Resultado: 5m42s em PT, 11 cenas, 2 blocos HeyGen.
Publicado: https://www.youtube.com/watch?v=p34w1bBPjpc (canal lives1). `OUT=~/projetos/output/explica-uTU5Ihgl_7Q`.

## Pedido
- Assunto: o que é a Decisions API da OpenAI e como se compara ao Jev (custo, velocidade, acerto, 3 demos).
- Fala sem citar o apresentador original; crédito escrito no fim ("Fonte: vídeo de Mark Kashef no YouTube", pedido depois). Termos técnicos em inglês. Fechar com inema ponto club.
- Entrega: bot v3; depois "publica na lives1".

## Comandos
```bash
# 1. referência
python3 ~/projetos/inemavox/baixar_v1.py --url "https://www.youtube.com/watch?v=uTU5Ihgl_7Q" --outdir $OUT/src --quality 1080p
python3 ~/projetos/inemavox/transcrever_v1.py --in $OUT/src/video.mp4 --outdir $OUT/src --whisper-model large-v3
ferramentas/extrair_frames.sh $OUT

# 2. prints (20 tempos escolhidos nas folhas)
for t in 33 39 63 93 117 171 255 297 309 321 339 357 393 423 453 471 495 525 537 549; do
  ffmpeg -v error -y -ss $t -i $OUT/src/video.mp4 -frames:v 1 $OUT/media/raw-$t.png; done
# slides com webcam à direita: recorte 1250×1080 e pad para 2052×1080
ferramentas/preparar_print.py $OUT/media/raw-33.png $OUT/media/p-33.png --crop 0,0,1250,1080 --pad
# telas de demo: webcam em 3 posições diferentes (conferir CADA print) → preenchimento por linha
for t in 357 393 423 453 471; do ferramentas/preparar_print.py $OUT/media/raw-$t.png $OUT/media/s-$t.png --cobrir 1516,52,377,362; done
for t in 297 309 321 495 525 537; do ferramentas/preparar_print.py $OUT/media/raw-$t.png $OUT/media/s-$t.png --cobrir 1516,676,377,362; done
ferramentas/preparar_print.py $OUT/media/raw-339.png $OUT/media/s-339.png --cobrir 1610,22,310,292

# 3. roteiro ($OUT/roteiro/pt.json = roteiro-pt.json) + storyboard → aprovação
ferramentas/montar_storyboard.py $OUT mapa.json

# 4. explicavideos v1 (configs = modelos/ com <ID>=decisions-jev, <OUT>=$OUT)
cd ~/projetos/explicavideos
EXPLICAVIDEOS_CONFIG=examples/decisions-jev.json python3 explica.py prepare
# Xvfb :99 (se não estiver no ar)
systemd-run --user --collect --unit=explicavideos-display /usr/bin/Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp
# HeyGen pelo estúdio (depois de gravar $OUT/v1/APROVADO_HEYGEN)
for n in 01 02; do DISPLAY=:99 timeout 600 node engine/heygen-studio.mjs --titulo EXPLICA-DECISIONS-JEV-PT-B$n-v1 \
  --fala-arquivo $OUT/v1/blocos/pt-b$n.txt --perfil ~/.cache/inemaccbot/perfil-heygen --template TEMPLATE-AVATAR16 \
  > $OUT/v1/verification/submit-pt-$n.log 2>&1; grep -o 'create-v4/[a-f0-9]\{32\}' $OUT/v1/verification/submit-pt-$n.log | head -1; done
# → gravar cada id em v1/blocos/manifest.json ("id", "status":"submitted", "via":"estudio")
~/projetos/refazvideo/ferramentas/baixa_blocos.sh $OUT
# render + montagem v1 (sem submit/monitor/publish)
for s in render:produce_blocks.py assemble:wait_assembly.py; do
  systemd-run --user --collect --unit=explica-decisions-jev-${s%%:*} --slice=explica.slice -p MemoryMax=16G -p MemorySwapMax=0 \
    --property=WorkingDirectory=$PWD --setenv=EXPLICAVIDEOS_CONFIG=$PWD/examples/decisions-jev.json /usr/bin/python3 $PWD/engine/${s#*:}; done
# pronto quando existir $OUT/v1/verification/assembled-pt.json

# 5. v2
export EXPLICAVIDEOS_CONFIG=examples/decisions-jev-v2.json
python3 engine/v2/setup_output.py
cp $OUT/visual/pt-b0*.json $OUT/v2/visual-v2/
~/projetos/refazvideo/ferramentas/validar_visual.py $OUT/roteiro/pt.json $OUT/visual/pt-b0*.json
python3 engine/v2/build_block.py 1 --strict; python3 engine/v2/build_block.py 2 --strict
systemd-run --user --scope --slice=explica.slice -p MemoryMax=16G -p MemorySwapMax=0 env EXPLICAVIDEOS_CONFIG=$EXPLICAVIDEOS_CONFIG \
  bash -c 'engine/v2/run_lane.sh 1 2 && python3 engine/assemble_languages.py'

# 6. entrega
ffmpeg -i $OUT/v2/final/decisions-jev-pt.mp4 -vf scale=1280:720 -c:v libx264 -b:v 850k -maxrate 1100k -bufsize 2200k -c:a aac -b:a 96k -movflags +faststart $OUT/v2/final/decisions-jev-pt-720p.mp4
node ~/projetos/refazvideo/ferramentas/enviar_bot_v3.mjs $OUT/v2/final/decisions-jev-pt-720p.mp4 "Decisions API × Jev · em português"
~/projetos/yt-pubx/yt-pubx publicar $OUT/v2/final/decisions-jev-pt.mp4 --canal lives1 --legenda $OUT/v2/final/decisions-jev-pt.srt --contexto "..." --dry-run
```

## Tempo real
Preparação (roteiro, prints, visual): ~1 h de agente. HeyGen: ~1 h em fila + minutos por bloco. v1: ~10 min. v2: ~15 min por passada.

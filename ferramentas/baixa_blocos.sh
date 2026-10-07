#!/usr/bin/env bash
# Baixa os blocos do avatar SÓ pelo estúdio HeyGen (sem API), um por vez, e registra em blocos-downloads.json.
# Lê ids e títulos de <OUT>/v1/blocos/manifest.json (campo "id" gravado após o envio pelo estúdio).
# Uso: ferramentas/baixa_blocos.sh <OUT>     (precisa do Xvfb :99 no ar e do perfil HeyGen logado)
set -u
OUT=${1:?uso: baixa_blocos.sh <OUT>}/v1
EV=${EXPLICAVIDEOS:-$HOME/projetos/explicavideos}
PERFIL=${PERFIL_HEYGEN:-$HOME/.cache/inemaccbot/perfil-heygen}
mkdir -p "$OUT/assets" "$OUT/verification"
python3 -c "import json,sys;[print('%s-b%02d:%s:%s'%(b['language'],b['part'],b['id'],b['title'])) for b in json.load(open(sys.argv[1]))]" "$OUT/blocos/manifest.json" |
while IFS=: read -r key id titulo; do
  arq="$OUT/assets/nei-$key.mp4"
  [ -s "$arq" ] && continue
  (cd "$EV" && DISPLAY=:99 timeout 7500 node engine/heygen-estudio-baixar.mjs --id "$id" --saida "$arq" \
     --perfil "$PERFIL" --minutos 120 --intervalo 120) > "$OUT/verification/baixar-$key.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ] || [ ! -s "$arq" ]; then echo "$key falhou rc=$rc (ver $OUT/verification/baixar-$key.log)"; exit 1; fi
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$arq")
  python3 - "$OUT/verification/blocos-downloads.json" "$key" "$id" "$titulo" "$arq" "$dur" <<'EOF'
import json,sys,pathlib
p=pathlib.Path(sys.argv[1]);d=json.loads(p.read_text()) if p.exists() else {}
d[sys.argv[2]]=dict(id=sys.argv[3],title=sys.argv[4],status='completed',downloaded=True,file=sys.argv[5],duration=float(sys.argv[6]),via='estudio')
s=json.dumps(d,ensure_ascii=False,indent=2);p.write_text(s)
EOF
  echo "$key baixado ($dur s)"
done || exit 1
echo TUDO_BAIXADO

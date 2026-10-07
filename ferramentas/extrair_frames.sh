#!/usr/bin/env bash
# Folhas de contato da referência: 1 quadro a cada N s (padrão 6), numerados, 24 por folha.
# Uso: ferramentas/extrair_frames.sh <OUT> [intervalo_s]   (lê <OUT>/src/video.mp4, grava <OUT>/frames/)
# Quadro n da folha ≈ tempo n*intervalo s no vídeo.
set -euo pipefail
OUT=${1:?uso: extrair_frames.sh <OUT> [intervalo_s]}; N=${2:-6}
mkdir -p "$OUT/frames"
ffmpeg -v error -y -i "$OUT/src/video.mp4" -vf "fps=1/$N,scale=480:-1" "$OUT/frames/t%03d.jpg"
ffmpeg -v error -y -pattern_type glob -i "$OUT/frames/t*.jpg" \
  -vf "drawtext=text='%{n}':x=5:y=5:fontsize=28:fontcolor=yellow:box=1:boxcolor=black,tile=6x4" "$OUT/frames/sheet%02d.jpg"
ls "$OUT"/frames/sheet*.jpg

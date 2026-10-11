# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-11 | terafab (16:9+9:16 de 1 gravação): `reel_profile` no config v1 fez o QA de reel reprovar o v1 16:9 (formato/fps/loudness); o --strict do 9:16 reprovou por 23/221 palavras interpoladas (Whisper escreveu "2 %", "200", "16 ,8", "para") | `reel_profile` só no config v2 9:16; reescrever a grafia no `v1/verification/transcript-*.json` (mesmos tempos) antes do `setup_output` | infra |
| 2026-10-09 | render v1 do contexto-portatil falhou (`templates/pt/scene-01.html` ausente): rodei só `engine/prepare.py` quando o `explica.py prepare` recusou, e a espera ficou 2 h porque só olhava a unit `render` E `assemble` | rodar também `build_scene_templates.py`; a espera sai ao ver `"failed"` no `production.json` | prompt |

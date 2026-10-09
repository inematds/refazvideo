# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-09 | render v1 do contexto-portatil falhou (`templates/pt/scene-01.html` ausente): rodei só `engine/prepare.py` quando o `explica.py prepare` recusou, e a espera ficou 2 h porque só olhava a unit `render` E `assemble` | rodar também `build_scene_templates.py`; a espera sai ao ver `"failed"` no `production.json` | prompt |

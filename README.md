# refazvideo

Refaz um vídeo de referência como **vídeo explicativo em português**, com o avatar e a voz do
apresentador (HeyGen), as telas reais da referência com destaques sincronizados à fala e animações.

**Como usar:** abra o Claude Code (ou Codex) nesta pasta e peça:

> Faça um vídeo novo. Assunto: \<tema\>. Referência: \<URL do vídeo\>. Não citar: \<autor\>. Entrega: bot v3.

O agente segue o `AGENTS.md`: baixa e transcreve a referência, escolhe os prints, escreve o roteiro,
mostra um storyboard para aprovação, gera o avatar no HeyGen **só depois do "pode fazer"**, renderiza,
confere quadros e entrega (Telegram e/ou YouTube). O formulário do pedido está em `modelos/pedido.md`.

## Conteúdo

| pasta | o quê |
|---|---|
| `AGENTS.md` | o passo a passo que o agente segue (regras, comandos, critérios de pronto) |
| `LICOES.md` | o que já quebrou e a proteção para cada caso |
| `modelos/` | pedido, configs v1/v2 do explicavideos |
| `ferramentas/` | folhas de quadros, preparo de print (cobrir rosto, pad), validação do visual, storyboard, download dos blocos HeyGen pelo estúdio, envio pelo bot v3 |
| `exemplos/decisions-jev/` | caso real: roteiro, visual dos 2 blocos, comandos rodados ([vídeo publicado](https://www.youtube.com/watch?v=p34w1bBPjpc)) |

## Pré-requisitos

- [`explicavideos`](https://github.com/inematds/explicavideos) (motor de render, HyperFrames 0.8.77) e `inemavox` (download/transcrição).
- Conta HeyGen com avatar próprio, logada num perfil de navegador (`heygen-studio.mjs` usa o estúdio, não a API).
- `ffmpeg`, Python 3 com Pillow, Node 20+. Opcional: bot Telegram (openpcbotv3) e `yt-pubx`.

Os caminhos de exemplo são os da máquina do INEMA (`/home/nmaldaner/...`); troque pelos seus.

## Uso responsável

Use referências que você pode reaproveitar. O vídeo novo é uma explicação própria, com roteiro reescrito;
não reproduza o vídeo original nem mostre o rosto de quem o apresentou.

Projetos e cursos gratuitos: https://inema.club

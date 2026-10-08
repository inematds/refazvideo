# refazvideo

[![refazvideo](guia/assets/banner-es.jpg)](https://inematds.github.io/refazvideo/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

refazvideo es un paso a paso, con herramientas listas, para que un agente de IA (Claude Code o Codex) rehaga un video que te pareció bueno como un video explicativo tuyo, en portugués. Sirve para quien produce contenido y quiere explicar un tema nuevo sin grabarse a sí mismo. Entregas el tema y el enlace; el agente descarga, transcribe, escribe un guion nuevo, muestra una vista previa y solo genera el avatar después de tu "adelante". Para usarlo necesitas el motor explicavideos, una cuenta de HeyGen con tu avatar y una máquina con GPU.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/refazvideo/guia/es/**

---

Rehace un video de referencia como **video explicativo en portugués**, con el avatar y la voz del
presentador (HeyGen), las pantallas reales de la referencia con resaltados sincronizados con el habla y animaciones.

**Cómo usarlo:** abre Claude Code (o Codex) en esta carpeta y pide:

> Haz un video nuevo. Tema: \<tema\>. Referencia: \<URL del video\>. No mencionar: \<autor\>. Entrega: bot v3.

El agente sigue el `AGENTS.md` (en portugués): descarga y transcribe la referencia, elige las capturas, escribe el guion,
muestra un storyboard para aprobación, genera el avatar en HeyGen **solo después del "adelante"**, renderiza,
revisa cuadros y entrega (Telegram y/o YouTube). El formulario del pedido está en `modelos/pedido.md`.

## Contenido

| carpeta | qué |
|---|---|
| `AGENTS.md` | el paso a paso que sigue el agente (reglas, comandos, criterios de terminado) |
| `LICOES.md` | lo que ya se rompió y la protección para cada caso |
| `modelos/` | pedido, configs v1/v2 de explicavideos |
| `ferramentas/` | hojas de cuadros, preparación de capturas (cubrir rostro, pad), validación del visual, storyboard, descarga de los bloques de HeyGen desde el estudio, envío por el bot v3 |
| `exemplos/decisions-jev/` | caso real: guion, visual de los 2 bloques, comandos ejecutados ([video publicado](https://www.youtube.com/watch?v=O2061m5FG_I)) |

## Requisitos previos

- [`explicavideos`](https://github.com/inematds/explicavideos) (motor de render, HyperFrames 0.8.77) e `inemavox` (descarga/transcripción).
- Cuenta de HeyGen con avatar propio, con sesión iniciada en un perfil de navegador (`heygen-studio.mjs` usa el estudio, no la API).
- `ffmpeg`, Python 3 con Pillow, Node 20+. Opcional: bot de Telegram (openpcbotv3) y `yt-pubx`.

Las rutas de ejemplo son las de la máquina de INEMA (`/home/nmaldaner/...`); cámbialas por las tuyas.

## Uso responsable

Usa referencias que puedas reaprovechar. El video nuevo es una explicación propia, con guion reescrito;
no reproduzcas el video original ni muestres el rostro de quien lo presentó.

Proyectos y cursos gratuitos: https://inema.club

#!/usr/bin/env python3
"""refazvideo do hhHkaZRwBBU (20/10/2026): mesma fala/avatar da versão completa, visual = trechos animados do original.
c(deixa, ini, fim) = clipe do original [ini, fim] s, cortado por ../clips/cortar.py (rosto do autor coberto).
Grava visual/pt-b01.json, pt-b02.json e clips/lista.json."""
import json
from pathlib import Path

O = Path(__file__).resolve().parent.parent
CL = O / "clips"
CAPA = str(Path.home() / "projetos/output/ia-crescendo/media/01-capa-base.png")
PT = str(O / "media" / "pt") + "/"
LISTA = []

def c(at, a, b, **kw):
    nome = f"c_{a:06.1f}_{b:06.1f}.mp4"
    LISTA.append([a, b, nome])
    d = {"type": "media", "at": at, "src": str(CL / nome), "focus": [0.5, 0.5], "zoom": [1.0, 1.0]}
    d.update(kw); return d

def m(at, nome, k):   # tela PT da versão completa (só nas dicas finais, que o original não tem)
    return {"type": "media", "at": at, "src": f"{PT}{nome}-s{k}.png", "focus": [0.5, 0.5], "zoom": [1.0, 1.06], "calm": True}

def st(at, txt): return {"type": "statement", "at": at, "text": txt}

S = {
 "1": [
   {"type": "hook", "at": "@start", "text": "**7×** em 12 meses", "kicker": "A IA DO GOOGLE CRESCEU", "sub": "o que acontece no enviar", "src": CAPA},
   c("Há dois anos", 351.5, 355.5), c("No ano passado", 355, 358.5), c("Hoje, mais de", 358, 362),
   c("três quatrilhões", 361.5, 366.4), c("E só o ChatGPT", 6, 12),
   st("Mas quase ninguém", "Quase ninguém sabe o que acontece no **enviar**"),
   c("Tecnologia avançada demais", 1.6, 6),
   c("Neste vídeo eu", 15.5, 22.4), c("viaja até o data", 714.5, 719.9),
   st("E no final", "No fim: **as dicas práticas**"),
 ],
 "2": [
   c("Etapa um", 22.4, 26.5),
   c("O ChatGPT não", 24.5, 30.5), c("aplicativo em volta", 30, 36),
   c("Quando você escreve", 36, 42), c("Primeiro o prompt", 42, 48),
   c("passa de três", 48, 53), c("começa pela data", 52.5, 59.5),
   c("Depois vêm as", 59, 66), c("a conversa inteira", 72, 84), c("O modelo não tem", 66, 72),
 ],
 "3": [
   c("E aqui mora", 84, 94), c("Cada conta intermediária", 107, 119), c("quanto maior a entrada", 95, 106),
   st("Isso tem nome", "**Context rot**: o contexto apodrecendo"),
 ],
 "4": [
   c("Etapa dois", 123.3, 127),
   c("Modelos menores ficam", 127, 138), c("São os classificadores", 138, 156),
   c("Na Anthropic", 156, 161.5), c("uns cinco por cento", 161, 167.5), c("hoje custa menos", 167, 174),
   c("A OpenAI faz", 174, 183.5), c("menos de dezoito", 186.6, 192.4),
 ],
 "5": [
   c("Etapa três", 198.5, 203),
   c("Quem faz a conversão", 220, 234), c("A pergunta o que", 249, 256), c("A palavra ChatGPT", 254, 258.5),
   c("E strawberry", 258, 268), c("O modelo não vê", 264, 274),
 ],
 "6": [
   c("Com números acontece", 274, 284), c("São picados em", 284, 296), c("é por isso que a IA erra", 296, 310),
   c("Hello world", 316, 323), c("A mesma frase em hindi", 321, 327), c("O inglês é uma", 324, 335.4),
 ],
 "7": [
   c("Etapa quatro", 341, 345),
   c("O modelo não mora", 343, 349), c("Mora em prédios", 347.5, 353), c("o Google processa", 367.6, 372),
   c("E o seu pedido", 372, 380), c("junto com o de outras", 378, 389.9),
   st("E aqui vem", "Quem divide a GPU **muda a sua resposta**"),
   c("A mesma pergunta", 398.6, 406), c("porque as contas mudam", 404, 414.9),
 ],
 "8": [
   c("Etapa cinco", 417.5, 421),
   c("Seus tokens passam", 421, 427), c("Pensa numa equação", 426, 432),
   c("Quase tudo isso", 432, 438.4), c("Ele propôs a atenção", 440.6, 450), c("Se a frase tem banco e rio", 450, 460), c("Se tem banco e empréstimo", 460, 470),
   c("O GPT três", 483.2, 491), c("organizados em matrizes", 490, 502.9),
 ],
 "9": [
   c("Etapa seis", 509.6, 513),
   c("Cada passada inteira", 512, 515.4), c("Para gerar o próximo", 518.6, 531), c("Até a palavra ChatGPT", 532, 540),
   c("E é por isso", 551, 572),
   st("E repara no principal", "O modelo não diz a verdade: escolhe o **mais provável**"),
   c("Pergunta a capital", 579.2, 583), c("Quando o provável", 582, 584.9),
 ],
 "10": [
   c("Etapa sete", 592.2, 596),
   c("o modelo decide entre", 596, 603), c("parar, raciocinar ou usar", 602.5, 606.9),
   c("Raciocinar é devolver", 608.2, 616), c("cinco, cem, até mil", 616, 624),
   c("E repara nas palavras", 624, 638), c("Como o modelo sempre", 638, 650), c("É assim que ele confere", 650, 657.9),
 ],
 "11": [
   c("O outro caminho", 663.2, 669), c("Hoje os modelos estão", 666, 672), c("O programa recebe texto", 671, 678),
   c("Uma busca na web", 677, 684), c("o site e o período", 681, 688), c("o programa consulta", 688, 697),
   c("Quem busca é o programa", 696, 701.5), c("Com o resultado na", 701, 712),
   c("Essa volta inteira", 713, 719.9),
   st("E vai ficar cada", "Quase na **velocidade do pensamento**"),
 ],
 "12": [
   m("E agora, as dicas", "12-dicas", 1), m("Dois:", "12-dicas", 2), m("Três:", "12-dicas", 3), m("Quatro:", "12-dicas", 4), m("Cinco:", "12-dicas", 5),
   st("A IA cresceu sete", "A IA cresceu **7×** em um ano"),
   st("Eu montei um curso", "Curso grátis: **as 7 etapas** com diagramas e prática"),
   {"type": "media", "at": "Tá tudo no", "src": str(Path.home() / "projetos/output/ia-crescendo/media/cta-print.png"), "focus": [0.5, 0.4], "zoom": [1.0, 1.08], "calm": True, "label": "**inema.club**"},
 ],
}

for b, cenas in (("pt-b01", range(1, 7)), ("pt-b02", range(7, 13))):
    out = {"block": b, "scenes": {str(n): {"shots": S[str(n)]} for n in cenas}}
    (O / "visual" / f"{b}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
CL.mkdir(exist_ok=True)
(CL / "lista.json").write_text(json.dumps(LISTA))
print("ok", len(LISTA), "clipes")

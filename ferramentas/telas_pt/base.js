// Ícones e setas no estilo quadro branco. Uso: <i class="ic" data-i="robot" data-s="80" style="left:..;top:.."></i>
const K = 'stroke="#1e1e1e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"';
const ICONS = {
  brain: (c) => `<svg viewBox="-6 -6 212 152"><ellipse cx="100" cy="70" rx="96" ry="66" fill="${c||'#fcc2d7'}" ${K}/><path d="M38 62 C62 22 84 38 104 74 S150 74 166 50" fill="none" stroke="#c2255c" stroke-width="5" stroke-linecap="round"/></svg>`,
  terminal: () => `<svg viewBox="0 0 100 80"><rect x="4" y="4" width="92" height="72" rx="8" fill="#d0bfff" ${K}/><line x1="4" y1="20" x2="96" y2="20" ${K}/><path d="M22 36 L36 46 L22 56 M44 58 H64" fill="none" ${K}/></svg>`,
  cloud: () => `<svg viewBox="0 0 100 70"><path d="M24 64 H78 C94 64 96 40 80 38 C80 18 56 10 46 26 C36 16 18 24 22 40 C6 42 8 64 24 64 Z" fill="#b2f2bb" ${K}/></svg>`,
  clock: () => `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#ffd8a8" ${K}/><path d="M50 24 V52 H68" fill="none" ${K}/></svg>`,
  eye: () => `<svg viewBox="0 0 100 60"><path d="M4 30 C30 -4 70 -4 96 30 C70 64 30 64 4 30 Z" fill="#fff" ${K}/><circle cx="50" cy="30" r="15" fill="#74c0fc" ${K}/><circle cx="50" cy="30" r="6" fill="#1e1e1e"/></svg>`,
  cursor: () => `<svg viewBox="0 0 70 100"><path d="M8 6 L8 80 L26 62 L40 94 L52 88 L38 58 L62 58 Z" fill="#fff" ${K}/></svg>`,
  checklist: () => `<svg viewBox="0 0 80 100"><rect x="4" y="4" width="72" height="92" rx="6" fill="#b2f2bb" ${K}/><rect x="14" y="18" width="14" height="14" fill="#fff" ${K}/><rect x="14" y="44" width="14" height="14" fill="#fff" ${K}/><rect x="14" y="70" width="14" height="14" fill="#fff" ${K}/><path d="M36 25 H66 M36 51 H66 M36 77 H66" ${K}/></svg>`,
  x: () => `<svg viewBox="0 0 60 60"><path d="M10 10 L50 50 M50 10 L10 50" fill="none" stroke="#e03131" stroke-width="7" stroke-linecap="round"/></svg>`,
  ok: () => `<svg viewBox="0 0 70 60"><path d="M6 32 L26 52 L64 8" fill="none" stroke="#2f9e44" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  robot: (c) => `<svg viewBox="0 0 100 100"><line x1="50" y1="26" x2="50" y2="10" ${K}/><circle cx="50" cy="9" r="6" fill="#e03131" ${K}/><rect x="14" y="26" width="72" height="58" rx="12" fill="${c||'#96f2d7'}" ${K}/><circle cx="36" cy="52" r="8" fill="#1e1e1e"/><circle cx="64" cy="52" r="8" fill="#1e1e1e"/><path d="M38 70 H62 M6 55 H14 M86 55 H94" ${K}/></svg>`,
  bolt: () => `<svg viewBox="0 0 70 110"><path d="M42 4 L8 64 H34 L26 106 L62 40 H38 Z" fill="#ffec99" ${K}/></svg>`,
  flag: () => `<svg viewBox="0 0 70 110"><path d="M14 100 V8" ${K}/><path d="M14 8 L62 22 L14 38 Z" fill="#ffc9c9" ${K}/><ellipse cx="14" cy="100" rx="12" ry="5" fill="#fff" ${K}/></svg>`,
  folder: () => `<svg viewBox="0 0 100 80"><path d="M4 16 V74 H96 V24 H46 L38 10 H8 Z" fill="#ffec99" ${K}/><line x1="4" y1="28" x2="96" y2="28" ${K}/></svg>`,
  doc: () => `<svg viewBox="0 0 80 100"><path d="M6 4 H54 L74 24 V96 H6 Z" fill="#fff" ${K}/><path d="M54 4 V24 H74 M18 46 H62 M18 62 H62 M18 78 H50" fill="none" ${K}/></svg>`,
  flask: () => `<svg viewBox="0 0 80 100"><path d="M28 6 H52 M32 6 V38 L8 92 H72 L48 38 V6" fill="none" ${K}/><path d="M18 70 H62 L70 90 H10 Z" fill="#b2f2bb"/><path d="M28 6 H52 M32 6 V38 L8 92 H72 L48 38 V6" fill="none" ${K}/></svg>`,
  lupa: () => `<svg viewBox="0 0 100 100"><circle cx="40" cy="40" r="30" fill="#b2f2bb" ${K}/><path d="M62 62 L92 92" stroke="#1e1e1e" stroke-width="9" stroke-linecap="round"/></svg>`,
  lapis: () => `<svg viewBox="0 0 100 100"><path d="M70 8 L92 30 L32 90 L8 94 L12 70 Z" fill="#b2f2bb" ${K}/><path d="M60 18 L82 40" ${K}/></svg>`,
  camera: () => `<svg viewBox="0 0 100 80"><path d="M6 20 H30 L38 8 H62 L70 20 H94 V74 H6 Z" fill="#a5d8ff" ${K}/><circle cx="50" cy="46" r="17" fill="#fff" ${K}/></svg>`,
  agenda: () => `<svg viewBox="0 0 100 100"><rect x="6" y="14" width="88" height="80" rx="6" fill="#b2f2bb" ${K}/><path d="M6 34 H94 M30 4 V22 M70 4 V22 M42 54 L58 70 M58 54 L42 70" fill="none" ${K}/></svg>`,
  email: () => `<svg viewBox="0 0 100 70"><rect x="4" y="4" width="92" height="62" rx="5" fill="#ffc9c9" ${K}/><path d="M4 8 L50 40 L96 8" fill="none" ${K}/></svg>`,
  janela: () => `<svg viewBox="0 0 100 80"><rect x="4" y="4" width="92" height="72" rx="6" fill="#fff" ${K}/><path d="M4 20 H96" ${K}/><rect x="14" y="30" width="26" height="36" fill="#d0bfff" ${K}/><path d="M50 34 H86 M50 48 H86 M50 62 H86" ${K}/></svg>`,
  pote: () => `<svg viewBox="0 0 120 150"><rect x="24" y="6" width="72" height="18" rx="4" fill="#dee2e6" ${K}/><path d="M18 24 H102 V136 Q102 146 92 146 H28 Q18 146 18 136 Z" fill="#f8f9fa" ${K}/><ellipse cx="60" cy="88" rx="32" ry="24" fill="#fcc2d7" ${K}/><path d="M38 84 C48 68 56 74 62 92 S80 92 84 80" fill="none" stroke="#c2255c" stroke-width="4"/></svg>`,
  calc: () => `<svg viewBox="0 0 80 100"><rect x="6" y="4" width="68" height="92" rx="8" fill="#e7f5ff" ${K}/><rect x="16" y="14" width="48" height="20" fill="#fff" ${K}/><g fill="#1e1e1e"><circle cx="24" cy="50" r="5"/><circle cx="40" cy="50" r="5"/><circle cx="56" cy="50" r="5"/><circle cx="24" cy="66" r="5"/><circle cx="40" cy="66" r="5"/><circle cx="56" cy="66" r="5"/><circle cx="24" cy="82" r="5"/><circle cx="40" cy="82" r="5"/><circle cx="56" cy="82" r="5"/></g></svg>`,
};
document.querySelectorAll('i.ic').forEach((el) => {
  const s = +(el.dataset.s || 80);
  const tmp = document.createElement('div');
  tmp.innerHTML = ICONS[el.dataset.i](el.dataset.c);
  const svg = tmp.firstChild;
  svg.setAttribute('class', 'ic');
  svg.setAttribute('style', el.getAttribute('style') || '');
  svg.style.width = s + 'px';
  svg.style.height = (el.dataset.h || s) + 'px';
  if (el.dataset.step) svg.dataset.step = el.dataset.step;
  el.replaceWith(svg);
});
// Marcadores de seta (preto, verde, azul) usados por <path marker-end="url(#ar)">.
document.body.insertAdjacentHTML('afterbegin', `<svg width="0" height="0" style="position:absolute"><defs>
${[['ar','#1e1e1e'],['ag','#2f9e44'],['ab','#1971c2']].map(([id,c]) => `<marker id="${id}" viewBox="0 0 20 20" refX="17" refY="10" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M2 2 L18 10 L2 18" fill="none" stroke="${c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></marker>`).join('')}
</defs></svg>`);
// Etapas: elementos com data-step > N ficam ocultos. ?step=N ou window.setStep(N).
window.maxStep = Math.max(1, ...[...document.querySelectorAll('[data-step]')].map((e) => +e.dataset.step));
// data-ate="N": some depois da etapa N (ex.: estado "antes" que é substituído).
window.setStep = (n) => document.querySelectorAll('[data-step]').forEach((e) => {
  const ate = e.dataset.ate ? +e.dataset.ate : Infinity;
  e.style.visibility = +e.dataset.step <= n && n <= ate ? 'visible' : 'hidden';
});
const q = new URLSearchParams(location.search).get('step');
window.setStep(q ? +q : window.maxStep);
// Caixa curta para o texto em PT: alarga para os dois lados (até +25%) e, se ainda faltar, reduz a fonte (até 80%).
window.fit = () => document.querySelectorAll('.b').forEach((e) => {
  if (e.scrollWidth <= e.clientWidth + 1) return;
  const w0 = e.offsetWidth, l0 = e.offsetLeft;
  const falta = e.scrollWidth - e.clientWidth + 8;
  const ganho = Math.min(falta, Math.round(w0 * 0.25));
  e.style.width = (w0 + ganho) + 'px';
  e.style.left = (l0 - ganho / 2) + 'px';
  let fs = parseFloat(getComputedStyle(e).fontSize); const min = fs * 0.8;
  while (e.scrollWidth > e.clientWidth + 1 && fs > min) { fs -= 1; e.style.fontSize = fs + 'px'; }
});

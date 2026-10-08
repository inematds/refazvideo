// Renderiza cada telas-pt/NN-*.html em todas as etapas -> media/pt/NN-<slug>-sK.png (2052x1080).
// Uso: node render.mjs [filtro]
import { createRequire } from 'node:module';
import { readdirSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/nmaldaner/.npm-global/lib/node_modules/playwright');
const dir = dirname(fileURLToPath(import.meta.url));
const out = join(dir, '..', 'media', 'pt');
mkdirSync(out, { recursive: true });
const filtro = process.argv[2] || '';
const files = readdirSync(dir).filter((f) => /^\d\d-.*\.html$/.test(f) && f.includes(filtro)).sort();
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 2052, height: 1080 } });
  const erros = [];
  page.on('pageerror', (e) => erros.push(e.message));
  for (const f of files) {
    await page.goto('file://' + join(dir, f));
    await page.evaluate(() => document.fonts.ready);
    const fonte = await page.evaluate(() => document.fonts.check('40px Excali'));
    await page.evaluate(() => window.fit());
    const max = await page.evaluate(() => window.maxStep);
    for (let k = 1; k <= max; k++) {
      await page.evaluate((n) => window.setStep(n), k);
      const png = join(out, f.replace('.html', `-s${k}.png`));
      await page.screenshot({ path: png });
    }
    // Texto que vaza do quadro ou elementos fora da tela
    const vaza = await page.evaluate(() => [...document.querySelectorAll('.b,.t,.foot,.title span')]
      .filter((e) => e.scrollWidth > e.clientWidth + 2 || e.getBoundingClientRect().right > 2052 || e.getBoundingClientRect().left < 0)
      .map((e) => e.textContent.trim().slice(0, 40)));
    console.log(`${f}: ${max} etapas, fonte=${fonte}${vaza.length ? ' VAZA: ' + vaza.join(' | ') : ''}`);
  }
  if (erros.length) console.log('ERROS JS:', erros);
} finally {
  await browser.close();
}

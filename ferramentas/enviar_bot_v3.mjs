// Envia um arquivo pelo bot v3 (@inemav3bot) ao chat permitido. Recibo em <arquivo>.envio-v3.json (não reenvia).
// Uso: node ferramentas/enviar_bot_v3.mjs <arquivo> "<legenda>" [--dry-run]
// .mp4 → sendVideo · .jpg/.png → sendPhoto (prévia, folha de telas) · outros (storyboard .html…) → sendDocument.
// Limite do bot API: 49 MB. Acima disso, faça antes uma cópia 720p:
//   ffmpeg -i final.mp4 -vf scale=1280:720 -c:v libx264 -b:v 850k -maxrate 1100k -bufsize 2200k -c:a aac -b:a 96k -movflags +faststart final-720p.mp4
import { readFileSync, writeFileSync, existsSync, statSync, openAsBlob } from 'node:fs';
import { basename } from 'node:path';
import { carregarEnv, lerConfig, validarTokenTelegram } from '/home/nmaldaner/projetos/openpcbotv3/dist/config/env.js';

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const [file, caption = ''] = args;
const dry = process.argv.includes('--dry-run');
if (!file || !existsSync(file)) throw new Error('Arquivo não encontrado: ' + file);
const receipt = file + '.envio-v3.json';
if (existsSync(receipt)) { console.log('já enviado:', readFileSync(receipt, 'utf8')); process.exit(0); }
const mb = statSync(file).size / 1048576;
if (mb > 49) throw new Error(`${mb.toFixed(1)} MB > 49 MB (limite do bot API)`);

carregarEnv();
const config = lerConfig();
if (!dry && (!validarTokenTelegram(config.telegramToken).ok || !config.chatPermitido)) throw new Error('Invalid bot v3 configuration');
const chat = String(config.chatPermitido || '');
if (dry) { console.log(`[dry-run] ${file} (${mb.toFixed(1)} MB)\n${caption}`); process.exit(0); }
const base = `https://api.telegram.org/bot${config.telegramToken}/`;
const me = await (await fetch(base + 'getMe')).json();
if (!me.ok || me.result.username !== 'inemav3bot') throw new Error('Unexpected bot identity');
const fd = new FormData();
const ext = file.toLowerCase().split('.').pop();
const [metodo, campo] = ext === 'mp4' ? ['sendVideo', 'video'] : ['jpg', 'jpeg', 'png'].includes(ext) ? ['sendPhoto', 'photo'] : ['sendDocument', 'document'];
fd.set('chat_id', chat); fd.set('caption', caption.slice(0, 1024));
if (campo === 'video') fd.set('supports_streaming', 'true');
fd.set(campo, await openAsBlob(file), basename(file));
const r = await (await fetch(base + metodo, { method: 'POST', body: fd })).json();
if (!r.ok) throw new Error(`Telegram ${r.error_code} ${r.description}`);
writeFileSync(receipt, JSON.stringify({ message_id: r.result.message_id, at: new Date().toISOString(), bytes: statSync(file).size }, null, 2));
console.log('enviado message_id', r.result.message_id);

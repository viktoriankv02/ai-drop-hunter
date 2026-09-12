import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { randomBytes } from 'node:crypto';
import { PlanStore as Store } from './plan-store.mjs';
import { sources, DiscoveryService } from './discovery.mjs';
import { Monitor } from './monitor.mjs';
import { networks } from './networks.mjs';
import { buildAgenda } from './agenda.mjs';

export function createApp(store, options = {}) {
  const discovery = options.discovery || new DiscoveryService(store);
  const monitor = new Monitor(store, discovery);
  if (options.monitor) monitor.start();
  const token = randomBytes(32).toString('hex');
  const app = createServer(async (req, res) => {
    const reply = (status, value) => { res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' }); res.end(JSON.stringify(value)); };
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'");
    const host = `127.0.0.1:${req.socket.localPort}`;
    if (req.headers.host !== host) return reply(403, { error: 'Invalid host' });
    if (req.headers.origin && req.headers.origin !== `http://${host}`) return reply(403, { error: 'Invalid origin' });
    try {
      const path = new URL(req.url, `http://${host}`).pathname;
      if (req.method === 'GET' && (path === '/api/state' || path === '/api/agenda')) {
        const projects=store.list();const agenda=buildAgenda(projects,store.clock ? store.clock().getTime() : Date.now());
        if(path==='/api/agenda')return reply(200,agenda);
        return reply(200,{token,networks,projects,agenda,events:store.history(),sources:sources.map(s=>({...s,lastScan:store.latestScan?.(s.id)||null})),monitor:store.setting?monitor.state():null});
      }
      const draftMatch=path.match(/^\/api\/projects\/([\w-]+)\/research-draft$/);
      if(req.method==='GET' && draftMatch)return reply(200,store.researchDraft(draftMatch[1]));
      if (req.method === 'POST') {
        if (req.headers['x-session-token'] !== token) return reply(403, { error: 'Оновіть сторінку для продовження' });
        if (!req.headers['content-type']?.startsWith('application/json')) return reply(415, { error: 'Expected JSON' });
        const chunks = []; let bytes = 0; for await (const chunk of req) { bytes += chunk.length; if (bytes > 65536) return reply(413, { error: 'Запит завеликий' }); chunks.push(chunk); }
        const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        if (!body || typeof body !== 'object' || Array.isArray(body)) throw new Error('Некоректний запит');
        if (path === '/api/projects') return reply(201, store.create(body));
        const planMatch=path.match(/^\/api\/projects\/([\w-]+)\/research-plan$/);
        if(planMatch)return reply(200,store.adoptResearch(planMatch[1],body));
        const assessmentMatch = path.match(/^\/api\/projects\/([\w-]+)\/assessment$/);
        if (assessmentMatch) return reply(201,store.saveAssessment(assessmentMatch[1],body));
        if (path === '/api/discovery/scan') return reply(200, await discovery.scan(body.sourceId));
        if (path === '/api/monitor') { if (typeof body.enabled !== 'boolean') throw new Error('Потрібне enabled: boolean'); store.setSetting('monitorEnabled', body.enabled); return reply(200, monitor.state()); }
        const match = path.match(/^\/api\/projects\/([\w-]+)\/(verify|tasks)$/);
        if (match) return reply(200, match[2] === 'verify' ? store.verify(match[1], body) : store.addTask(match[1], body));
        const scheduleMatch=path.match(/^\/api\/tasks\/([\w-]+)\/schedule$/);
        if(scheduleMatch) return reply(200,store.scheduleTask(scheduleMatch[1],body));
        const task = path.match(/^\/api\/tasks\/([\w-]+)\/complete$/);
        if (task) return reply(200, store.complete(task[1], body));
      }
      const files = { '/agenda.js': ['agenda.js','text/javascript'], '/research.js': ['research.js','text/javascript'], '/schedule.js': ['schedule.js','text/javascript'], '/assessment.js': ['assessment.js', 'text/javascript'], '/': ['index.html', 'text/html'], '/app.js': ['app.js', 'text/javascript'], '/style.css': ['style.css', 'text/css'] };
      if (req.method === 'GET' && Object.hasOwn(files, path)) {
        const [file, type] = files[path]; const data = await readFile(new URL(`../public/${file}`, import.meta.url));
        res.writeHead(200, { 'Content-Type': `${type}; charset=utf-8` }); return res.end(data);
      }
      reply(404, { error: 'Не знайдено' });
    } catch (error) { reply(400, { error: error.message }); }
  });
  app.on('close', () => monitor.stop());
  return app;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const store = new Store(fileURLToPath(new URL('../data/drop-hunter.sqlite', import.meta.url)));
  const app = createApp(store, { monitor: true });
  app.listen(Number(process.env.PORT || 4317), '127.0.0.1', () => console.log(`Drop Hunter: http://127.0.0.1:${app.address().port}`));
  for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => app.close(() => { store.close(); process.exit(0); }));
}

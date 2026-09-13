import {test} from 'node:test';import assert from 'node:assert/strict';import {PlanStore} from '../src/plan-store.mjs';import {AnalysisQueue} from '../src/analysis-queue.mjs';
test('queue deduplicates, skips obsolete versions, retries failure and recovers interrupted work',async()=>{
 const s=new PlanStore(':memory:');const p=s.create({name:'Queue',network:'unknown',source:'https://example.com'});let hash='new',fail=true,calls=0;const agents={busy:false,materials:{latest(){return {hash};}},async analyze(id,version){calls++;assert.equal(id,p.id);assert.equal(version,hash);if(fail)throw Error('Offline');}};const q=new AnalysisQueue(s,agents);
 try{q.enqueue(p.id,'old');q.enqueue(p.id,'new');q.enqueue(p.id,'new');assert.equal(s.db.prepare('SELECT COUNT(*) n FROM analysis_jobs').get().n,2);await q.tick();assert.equal(calls,0);await q.tick();assert.equal(q.latest(p.id).status,'failed');fail=false;q.retry(p.id);await q.tick();assert.equal(q.latest(p.id).status,'succeeded');
 s.db.prepare("UPDATE analysis_jobs SET status='running' WHERE materialHash='new'").run();agents.busy=true;q.start();assert.equal(q.latest(p.id).status,'pending');q.stop();
 }finally{q.stop();s.close();}
});

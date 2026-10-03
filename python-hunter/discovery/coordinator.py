import asyncio, json, os
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
from core.workspace import utcnow
from discovery.cryptorank_api import fetch_map
from core.source_policy import source_allows_url, canonical_url
from discovery.evidence import read_html, material, catalog, telegram_messages, SourceUnavailable
from ai_analyzer.grounded import analyze
from ai_analyzer.gateway import OLLAMA_MODEL
from core.participation import VERSION as PARTICIPATION_VERSION
from core.campaign_guide import VERSION as GUIDE_VERSION
from discovery.public_search import search_public_sources

class Coordinator:
    def __init__(self,store):
        self.store=store
        self.stop=asyncio.Event()
        self.current_job=None
    def progress(self,index,total):
        if self.current_job:
            with self.store.db() as c:
                c.execute("UPDATE jobs SET phase=? WHERE id=?",
                          (f"Ollama: частина {index}/{total}; локальна CPU-модель",self.current_job))
    async def discover(self,sid):
        sources=[s for s in self.store.sources() if s["id"]==sid and s["enabled"]]
        if not sources: raise SourceUnavailable("Джерело вимкнено або видалено")
        s=sources[0]
        if s["adapter"]=="manual":
            raise SourceUnavailable("Для цього джерела ще потрібен окремий адаптер; автоматичний збір не реалізовано.")
        host=urlsplit(s["url"]).hostname
        try:
            if s["adapter"]=="cryptorank" and os.getenv("CRYPTORANK_API_KEY"):
                candidates=await fetch_map()
                data={"history_complete":False,"route":"official_api_map","tasks_included":False,
                      "scope":"Повний отриманий API-каталог назв; статуси, завдання і mainnet ще не перевірені."}
            else:
                html,url=await read_html(s["url"],{host})
            if s["adapter"]=="cryptorank" and os.getenv("CRYPTORANK_API_KEY"):
                pass
            elif s["kind"]=="telegram":
                if s["added_by"]!="user": raise SourceUnavailable("Канал не доданий користувачем")
                previous=datetime.fromisoformat(s["last_check"]) if s["last_check"] else None
                data=telegram_messages(html,datetime.now(timezone.utc),previous)
                candidates=data["messages"]
            else:
                candidates=catalog(html,url,s["adapter"])
                data={"history_complete":False,"scope":"Посилання з однієї доступної сторінки; пагінація ще не реалізована."}
            if not candidates: raise SourceUnavailable("Не знайдено карток у доступному HTML. Це не означає відсутність проєктів.")
            added=0;fresh_ids=[]
            limit=len(candidates) if data.get("route")=="official_api_map" else 200
            for item in candidates[:limit]:
                # Do not invent rating, costs or participation tasks from a catalogue title.
                pid,fresh=self.store.add_project(item["title"],item["url"],s["name"],item.get("text",""),prepare=False)
                added+=fresh
                if fresh:fresh_ids.append(pid)
                if fresh and data.get("route")=="official_api_map":
                    with self.store.db() as c:
                        c.execute("UPDATE projects SET check_status='catalog_only' WHERE id=?",(pid,))
            for pid in fresh_ids[:20]:self.store.prepare_project(pid)
            outcome={"found":len(candidates),"added":added,"duplicates":min(len(candidates),limit)-added,
                     "limited":len(candidates)>limit,**{k:v for k,v in data.items() if k!="messages"}}
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='partial',last_error=NULL WHERE id=?",(utcnow(),sid))
            return outcome
        except Exception as error:
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='failed',last_error=? WHERE id=?",(utcnow(),str(error)[:600],sid))
            raise
    async def _read_primary_and_reviewed(self,p):
        """Fallback only to reviewed official URLs, never arbitrary links suggested by a model."""
        try:
            html,url=await read_html(p["source_url"],{urlsplit(p["source_url"]).hostname})
            primary=material(html,url)
            documents=[{**primary,"purpose":"reward_rules" if urlsplit(url).hostname in {"cryptorank.io","incrypted.com"} else "unclassified"}];errors=[]
            # Follow explicit campaign/rules links only; no model-generated URLs.
            seen={url}
            for link in primary.get("links",[]):
                label=(link.get("label","")+" "+link.get("url","")).lower()
                if len(documents)>=4: break
                if not any(word in label for word in ("eligibility","airdrop","reward","campaign","quest","claim","правила","умови")): continue
                try:
                    target=canonical_url(link["url"])
                    if target in seen: continue
                    seen.add(target)
                    if urlsplit(target).hostname in {"t.me","twitter.com","x.com","discord.com","discord.gg"}: continue
                    extra_html,resolved=await read_html(target,{urlsplit(target).hostname})
                    doc=material(extra_html,resolved)
                    doc["purpose"]="unclassified"
                    documents.append(doc)
                except Exception as error: errors.append(str(error)[:200])
            if len(documents)==1: return primary,"web"
            text="\n\n".join("Джерело: "+d["url"]+"\n"+d["text"] for d in documents)
            return {**primary,"text":text[:60000],"characters_available":len(text),
                    "truncated":len(text)>60000 or any(d.get("truncated") for d in documents),
                    "links":([{"url":d["url"],"label":"Документ кампанії"} for d in documents]+[link for d in documents for link in d.get("links",[])])[:150],
                    "documents":documents,"source_errors":errors,
                    "provenance":"Прочитано картку та пов’язані сторінки. Статус додаткових документів потребує перевірки."},"linked_documents"
        except SourceUnavailable as primary_error:
            notes=self.store.rows("SELECT body_json FROM snapshots WHERE project_id=? AND via='reviewed_research_note' ORDER BY id DESC LIMIT 1",(p["id"],))
            if not notes: raise
            note=json.loads(notes[0]["body_json"]).get("research_note",{})
            sources=[x for x in note.get("sources",[]) if x.get("access")=="official_document"][:3]
            documents=[];errors=[]
            for source in sources:
                try:
                    url=canonical_url(source["url"])
                    html,resolved=await read_html(url,{urlsplit(url).hostname})
                    doc=material(html,resolved)
                    doc["purpose"]=source.get("purpose","unclassified")
                    documents.append(doc)
                except Exception as error:
                    errors.append(str(error)[:200])
            if not documents:
                raise SourceUnavailable(str(primary_error)+" Офіційні документи також недоступні.")
            text="\n\n".join("Джерело: "+d["url"]+"\n"+d["text"] for d in documents)
            links=[{"url":d["url"],"label":"Офіційна документація"} for d in documents]
            links.extend(link for d in documents for link in d["links"])
            return {"url":p["source_url"],"text":text,"links":links[:150],
                    "truncated":True,"characters_available":len(text),
                    "documents":documents,"source_errors":errors,
                    "provenance":"Агрегатор недоступний. Прочитано раніше перевірені офіційні документи; загальне досьє неповне."},"official_documents_fallback"

    async def read_project(self,p):
        documents=[];errors=[];via="project_resources";original=None
        try:
            body,via=await self._read_primary_and_reviewed(p)
            original=body
            documents=body.get("documents") or [{**body,"purpose":"reward_rules" if urlsplit(body["url"]).hostname in {"cryptorank.io","incrypted.com"} else "product_manual"}]
            errors.extend(body.get("source_errors",[]))
        except Exception as error: errors.append(str(error)[:400])
        resources=self.store.rows("SELECT * FROM project_resources WHERE project_id=? ORDER BY CASE purpose WHEN 'reward_rules' THEN 0 WHEN 'product_manual' THEN 1 ELSE 2 END,url",(p["id"],))
        for doc in list(documents):
            for link in doc.get("links",[]):
                label=link.get("label","").lower()
                if not any(word in label for word in ("official","website","documentation","eligibility","rules","guide","сайт","офіційн","правила","документац")):continue
                host=urlsplit(link["url"]).hostname
                if host in {"t.me","x.com","twitter.com","discord.com","discord.gg"}:continue
                purpose="product_manual" if any(word in label for word in ("official","website","сайт","офіційн")) else "secondary"
                self.store.add_resource(p["id"],link["url"],link.get("label","Документ"),purpose,"source_link")
        resources=self.store.rows("SELECT * FROM project_resources WHERE project_id=? ORDER BY CASE purpose WHEN 'reward_rules' THEN 0 WHEN 'product_manual' THEN 1 ELSE 2 END,url",(p["id"],))
        # A blocked aggregator is not the end of project research.
        if (not documents and (not resources or all(r.get('last_status')=='failed' for r in resources))) or (documents and sum(len(d['text']) for d in documents)<500):
            try:
                for result in await search_public_sources(p["title"]):
                    self.store.add_resource(p["id"],result["url"],result["label"],"secondary","public_web_search")
                resources=self.store.rows("SELECT * FROM project_resources WHERE project_id=?",(p["id"],))
            except Exception as error:errors.append("Вебпошук: "+str(error)[:200])
        if original and not resources:return original,via
        seen={d['url'] for d in documents}
        for resource in resources[:6]:
            if resource['url'] in seen:continue
            try:
                html,resolved=await read_html(resource['url'],None)
                doc=material(html,resolved);doc['purpose']=resource['purpose'];documents.append(doc);seen.add(resolved)
                self.store.resource_checked(p['id'],resource['url'])
            except Exception as error:
                self.store.resource_checked(p['id'],resource['url'],error);errors.append(resource['url']+": "+str(error)[:200])
        if not documents:raise SourceUnavailable("; ".join(errors)[:900] or "Не знайдено доступних джерел")
        if len(documents)==1 and not errors:return documents[0],via
        text="\n\n".join("Джерело: "+d['url']+"\n"+d['text'] for d in documents)
        links=[{'url':d['url'],'label':'Прочитане джерело'} for d in documents]+[l for d in documents for l in d.get('links',[])]
        return {'url':p['source_url'],'text':text[:60000],'links':links[:150],'documents':documents,
                'characters_available':len(text),'truncated':bool(errors) or len(text)>60000 or any(d.get('truncated') for d in documents),
                'source_errors':errors,'provenance':'Багатоджерельне дослідження. Первинні правила, довідка продукту та вторинні матеріали розрізняються.'},'multi_source_research'

    @staticmethod
    def attach_provenance(result,body):
        if body.get("provenance"):
            result["provenance"]=body["provenance"]
            result.setdefault("unknowns",[]).extend(body.get("source_errors",[]))
            for item in ([result["overview"]] if result.get("overview") else [])+result.get("campaigns",[])+[step for campaign in result.get("campaigns",[]) for step in campaign.get("steps",[])]+result.get("facts",[])+result.get("tasks",[])+result.get("requirements",[]):
                matches=[d["url"] for d in body.get("documents",[]) if item.get("quote") and item["quote"] in d["text"]]
                matches=list(dict.fromkeys(matches))
                if len(matches)==1:
                    item["source_url"]=matches[0]
                elif len(matches)>1:
                    item.pop("source_url",None)
                    item["source_urls"]=matches
                    item["evidence_status"]="ambiguous_source_match"
                    item["requires_review"]=True
                    if item is result.get("overview"):
                        result["overview"]=None
                        result.setdefault("unknowns",[]).append("Опис потребує перевірки: цитата є в кількох джерелах.")
            reward_sources={d["url"] for d in body.get("documents",[]) if d.get("purpose")=="reward_rules"}
            for requirement in result.get("requirements",[]):
                if requirement.get("source_url") not in reward_sources:
                    requirement["necessity"]="unknown"
                    requirement["evidence_status"]="platform_reference_not_reward_rule"
            tasks=result.get("tasks",[])
            result["reference_actions"]=[t for t in tasks if t.get("source_url") not in reward_sources]
            result["tasks"]=[t for t in tasks if t.get("source_url") in reward_sources]
            if result["reference_actions"]:
                result.setdefault("unknowns",[]).append("Інструкції платформи не підтверджують завдання кампанії; їх винесено в довідку.")

    def project_research_allowed(self,p):
        if any(source_allows_url(s,p['source_url']) for s in self.store.sources()):return True
        return urlsplit(p['source_url']).hostname!='t.me' and bool(self.store.rows("SELECT 1 FROM project_research_scope WHERE project_id=? AND enabled=1",(p['id'],)))

    async def research(self,pid):
        p=self.store.project(pid)
        host=urlsplit(p["source_url"]).hostname
        permitted=[s for s in self.store.sources() if source_allows_url(s,p["source_url"])]
        if not self.project_research_allowed(p): raise SourceUnavailable("Джерело не ввімкнене в дозволеному списку")
        if permitted and all(s["adapter"]=="manual" for s in permitted):
            raise SourceUnavailable("Автоматичне читання цього джерела ще не реалізовано")
        body,via=await self.read_project(p)
        body["project_title"]=p["title"]
        url=p["source_url"]
        sid,changed=self.store.save_snapshot(pid,url,body,via=via)
        previous=self.store.rows("SELECT body_json,created_at FROM reports WHERE project_id=? AND snapshot_id=? ORDER BY id DESC LIMIT 1",(pid,sid))
        new_feedback=self.store.rows("SELECT 1 FROM feedback WHERE project_id=? AND created_at>? LIMIT 1",(pid,previous[0]["created_at"] if previous else ""))
        if not changed and previous and json.loads(previous[0]["body_json"]).get("coverage",{}).get("complete") and not new_feedback and json.loads(previous[0]["body_json"]).get("participation_version")==PARTICIPATION_VERSION and json.loads(previous[0]["body_json"]).get("guide_version")==GUIDE_VERSION:
            return {"snapshot_id":sid,"changed":False,"analysis":"unchanged"}
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(pid,))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.attach_provenance(result,body)
        self.store.save_report(pid,sid,result,OLLAMA_MODEL)
        return {"snapshot_id":sid,"changed":changed,"analysis":result["status"],"coverage":result["coverage"]}
    async def analyze_snapshot(self,sid):
        rows=self.store.rows("SELECT * FROM snapshots WHERE id=?",(sid,))
        if not rows: raise ValueError("Матеріал не знайдено")
        snapshot=rows[0]
        project=self.store.project(snapshot["project_id"])
        if not self.project_research_allowed(project):
            raise SourceUnavailable("Джерело вимкнене: аналіз призупинено.")
        body=json.loads(snapshot["body_json"])
        body["project_title"]=project["title"]
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(snapshot["project_id"],))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.attach_provenance(result,body)
        self.store.save_report(snapshot["project_id"],sid,result,OLLAMA_MODEL)
        return {"snapshot_id":sid,"analysis":result["status"],"coverage":result["coverage"]}
    async def run(self):
        self.store.recover_jobs()
        while not self.stop.is_set():
            job=self.store.claim_job()
            if not job:
                try: await asyncio.wait_for(self.stop.wait(),timeout=2)
                except TimeoutError: pass
                continue
            self.current_job=job["id"]
            try:
                if job["kind"]=="discover": result=await self.discover(job["target_id"])
                elif job["kind"]=="analyze": result=await self.analyze_snapshot(job["target_id"])
                else: result=await self.research(job["target_id"])
                self.store.finish_job(job["id"],result=result)
            except asyncio.CancelledError:
                # Leave the running record for recovery on next startup.
                raise
            except Exception as error:
                message=str(error)[:700]
                if job["kind"]=="research": self.store.check_failed(job["target_id"],message)
                self.store.finish_job(job["id"],error=message)
    async def schedule(self):
        while not self.stop.is_set():
            cutoff=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat()
            for source in self.store.sources():
                if source["enabled"] and source["purpose"]=="discovery" and source["adapter"]!="manual" and (not source["last_check"] or source["last_check"]<cutoff):
                    self.store.enqueue("discover",source["id"])
            for incoming in self.store.pending_preparation():
                self.store.prepare_project(incoming['id'])
            for project in self.store.due_projects():
                if self.project_research_allowed(project):
                    self.store.enqueue("research",project["id"])
            try: await asyncio.wait_for(self.stop.wait(),timeout=60)
            except TimeoutError: pass

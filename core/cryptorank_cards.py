"""Public CryptoRank captures: source instructions, never fabricated AI reports."""
import json,re
from urllib.parse import urlsplit
from core.source_policy import canonical_url
from discovery.source_quality import document_issue

def initialize(c):
    c.execute("""CREATE TABLE IF NOT EXISTS project_public_guides(
        project_id INTEGER PRIMARY KEY REFERENCES projects(id),
        snapshot_id INTEGER NOT NULL REFERENCES snapshots(id),
        body_json TEXT NOT NULL, updated_at TEXT NOT NULL)""")

def public_guide(text, sections, source, gated=False):
    if document_issue("",{"url":source,"text":text}):
        raise ValueError("Замість інструкції отримано перевірку браузера.")
    gated=bool(gated or re.search(r"Войдите, чтобы|Войти, чтобы|Sign in to|Log in to|lorem ipsum",text,re.I))
    result=[]
    # A login overlay can leave hidden sections in the DOM; never import them.
    visible_sections=sections[:1] if gated else sections[:30]
    for section in visible_sections:
        title=section.get("title","").strip()[:200]
        content=section.get("text","").strip()
        if not title or title not in content or content not in text:
            continue
        if re.search(r"lorem ipsum",content,re.I):continue
        links=[]
        for link in section.get("links",[])[:60]:
            try: target=canonical_url(link["url"])
            except (ValueError,KeyError):continue
            if target not in {x["url"] for x in links}:links.append({"url":target,"label":link.get("label","")[:150]})
        steps=[]
        for line in content.splitlines():
            line=line.strip()
            if not re.match(r"^\d{1,2}[.)]\s+\S",line):continue
            if len(line)>900:continue
            sensitive=bool(re.search(r"приватн\w* ключ|private key|seed|сид[- ]фраз|секретн",line,re.I))
            steps.append({"text":line,"manual_only":True,"sensitive":sensitive})
        result.append({"title":title,"steps":steps,"links":links,
                       "sensitive":bool(re.search(r"приватн\w* ключ|private key|seed|сид[- ]фраз",content,re.I)),
                       "status":"ended" if re.search(r"^Завершено\s*$",content,re.M) else "unconfirmed",
                       "excerpt":re.sub(r"(?m)^(?:Выполнено|Новое)\s*$","",re.split(r"(?m)^\s*\d{1,2}[.),]\s+",content,maxsplit=1)[0]).strip()[:1600]})
    return {"source_url":source,"access":"partial_login" if gated else "no_public_tasks" if not result and re.search(r"0\s*/\s*0\s*выполнено",text) else "public_visible",
            "complete":False,"campaigns":result,
            "notice":"Збережено лише відкритий текст браузера. Приховані та нерозгорнуті інструкції не прочитані; актуальність і нагорода потребують перевірки.",
            "reader":"browser-visible-v1","ai_analysis":False}

def import_capture(store, capture):
    from core.workspace import utcnow
    source=canonical_url(capture["source"])
    if urlsplit(source).hostname!="cryptorank.io":raise ValueError("Лише CryptoRank")
    rows=store.rows("SELECT id,title FROM projects WHERE source_url=?",(source,))
    if not rows:raise ValueError("Картки немає в локальному каталозі")
    pid=rows[0]["id"]
    text=capture["text"]
    guide=public_guide(text,capture.get("sections",[]),source,capture.get("gated",False))
    if not guide["campaigns"] and guide["access"] not in ("partial_login","no_public_tasks"):
        raise ValueError("Не знайдено відкритих інструкцій або явного повідомлення про обмеження доступу")
    links=[link for section in guide["campaigns"] for link in section["links"]]
    body={"url":source,"text":text,"links":links[:150],"truncated":True,
          "characters_available":len(text),"project_title":rows[0]["title"],
          "access":guide["access"],"provenance":guide["notice"],
          "documents":[{"url":source,"text":text,"links":links[:150],"purpose":"reward_rules"}]}
    sid,changed=store.save_snapshot(pid,source,body,via="browser_public_capture")
    with store.db() as c:
        initialize(c)
        c.execute("""INSERT INTO project_public_guides VALUES (?,?,?,?)
            ON CONFLICT(project_id) DO UPDATE SET snapshot_id=excluded.snapshot_id,
            body_json=excluded.body_json,updated_at=excluded.updated_at""",
            (pid,sid,json.dumps(guide,ensure_ascii=False),utcnow()))
    return {"project_id":pid,"snapshot_id":sid,"changed":changed,
            "campaigns":len(guide["campaigns"]),"steps":sum(len(x["steps"]) for x in guide["campaigns"]),
            "access":guide["access"]}

def inventory(store):
    rows=store.rows("""SELECT p.id,p.title,p.source_url,p.status,p.check_status,
        g.updated_at AS public_read_at,
        json_extract(g.body_json,'$.access') AS public_access,
        COALESCE(json_array_length(json_extract(g.body_json,'$.campaigns')),0) AS public_campaigns,
        EXISTS(SELECT 1 FROM project_overviews o WHERE o.project_id=p.id) AS has_overview,
        EXISTS(SELECT 1 FROM reports r WHERE r.project_id=p.id) AS has_analysis
        FROM projects p LEFT JOIN project_public_guides g ON g.project_id=p.id
        WHERE p.source_url LIKE 'https://cryptorank.io/%'
        ORDER BY (g.project_id IS NOT NULL),p.id DESC""")
    for row in rows:
        row["missing"]=[]
        if not row["has_overview"]:row["missing"].append("Опис")
        if not row["public_read_at"]:row["missing"].append("Читання публічної сторінки")
        if not row["public_campaigns"]:row["missing"].append("Відкриті інструкції")
        if not row["has_analysis"]:row["missing"].append("ШІ-аналіз")
        if row["public_access"]=="partial_login":row["missing"].append("Дані за входом")
    return rows

"""Reject challenge pages and unrelated search documents before inference."""
import re
from urllib.parse import urlsplit
from discovery.public_search import NON_PROJECT_HOSTS, search_relevance

VERSION="source-quality-v1"

def document_issue(title, document, resource=None):
    text=document.get("text","")
    lower=text.lower()
    if any(marker in lower for marker in (
        "verify you are human", "cf-chl-", "триває перевірка безпеки",
        "performing security verification",
    )) or (len(text)<3000 and any(marker in lower for marker in (
        "just a moment", "трохи зачекайте", "checking your browser",
    ))):
        return "Замість інструкції збережено перевірку браузера."
    host=(urlsplit(document.get("url","")).hostname or "").lower()
    if any(host==blocked or host.endswith("."+blocked) for blocked in NON_PROJECT_HOSTS):
        return "Стороння сторінка: автомобілі або словник, а не джерело криптопроєкту."
    if resource and resource.get("discovered_via")=="public_web_search":
        if not search_relevance(title,document.get("url",""),text):
            return "Пошуковий результат не підтверджує назву та криптовалютний контекст проєкту."
    return None

def inspect_documents(title, body, resources=()):
    by_url={r["url"]:r for r in resources}
    accepted=[];rejected=[]
    for document in body.get("documents") or [body]:
        reason=document_issue(title,document,by_url.get(document.get("url")))
        if reason:rejected.append({"url":document.get("url"),"reason":reason})
        else:accepted.append(document)
    return accepted,rejected

def clean_material(title, body, resources=()):
    # Imported source text may have come through an older, less strict reader.
    from discovery.evidence import SourceUnavailable
    accepted,rejected=inspect_documents(title,body,resources)
    if not rejected:return body
    if not accepted:
        raise SourceUnavailable("Матеріал відхилено до ШІ-аналізу: "+rejected[0]["reason"])
    text="\n\n".join("Джерело: "+d.get("url","")+"\n"+d.get("text","") for d in accepted)
    blocked={r["url"] for r in rejected}
    return {**body,"documents":accepted,"text":text[:60000],
            "links":[link for d in accepted for link in d.get("links",[]) if link.get("url") not in blocked][:150],
            "characters_available":len(text),"truncated":True,
            "source_errors":body.get("source_errors",[])+[r["reason"] for r in rejected],
            "quality_rejections":rejected,
            "provenance":"Частковий матеріал: сторонні або заблоковані сторінки відсіяно перед аналізом."}

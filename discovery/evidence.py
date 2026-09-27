"""Bounded readers for configured public sources, with explicit blocked/unsupported outcomes."""
import asyncio, ipaddress, json, re, socket
from urllib.parse import urljoin, urlsplit
from datetime import datetime, timezone
import httpx
from bs4 import BeautifulSoup
from core.source_policy import canonical_url, telegram_window

class SourceUnavailable(RuntimeError): pass

async def read_html(url, allowed_hosts):
    url=canonical_url(url)
    async with httpx.AsyncClient(timeout=25, follow_redirects=False, trust_env=False,
                                 headers={"User-Agent":"AI-Drop-Hunter/0.6 (public research reader)"}) as client:
        for _ in range(4):
            host=urlsplit(url).hostname
            if host not in allowed_hosts: raise SourceUnavailable("Перенаправлення поза дозволеним джерелом")
            records=await asyncio.get_running_loop().getaddrinfo(host,443,type=socket.SOCK_STREAM)
            if not records or any(not ipaddress.ip_address(r[4][0]).is_global for r in records):
                raise SourceUnavailable("Джерело має непублічну мережеву адресу")
            async with client.stream("GET",url) as response:
                if response.status_code in (301,302,303,307,308):
                    url=canonical_url(urljoin(url,response.headers.get("location","")))
                    continue
                if response.status_code in (401,403,429):
                    raise SourceUnavailable(f"HTTP {response.status_code}: потрібен доступ/перевірка або пауза. Дані не прочитані.")
                response.raise_for_status()
                if "html" not in response.headers.get("content-type",""):
                    raise SourceUnavailable("Джерело не повернуло HTML")
                content=bytearray()
                async for chunk in response.aiter_bytes():
                    content.extend(chunk)
                    if len(content)>2_000_000: raise SourceUnavailable("Сторінка завелика для одного читання")
                text=bytes(content).decode("utf-8","replace")
                sample=text[:25000].lower()
                if any(x in sample for x in ("cf-chl-","verify you are human","just a moment...","трохи зачекайте","enable javascript and cookies to continue")):
                    raise SourceUnavailable("Сторінка перевірки браузера: потрібен імпорт відкритого матеріалу")
                return text,url
    raise SourceUnavailable("Забагато перенаправлень")

def material(html,url):
    soup=BeautifulSoup(html,"lxml")
    node=soup.select_one("article .entry-content, .entry-content, article, main") or soup
    for tag in node.select("script,style,nav,footer,header,aside,form"): tag.decompose()
    paragraphs=[]
    for tag in node.select("h1,h2,h3,h4,p,li"):
        value=re.sub(r"\s+"," ",tag.get_text(" ",strip=True)).strip()
        if value and (not paragraphs or value!=paragraphs[-1]):
            paragraphs.append(value)
    text="\n\n".join(paragraphs) or node.get_text(" ",strip=True)
    if len(text)<100: raise SourceUnavailable("Недостатньо тексту для аналізу; можлива JS-сторінка")
    links=[]
    for a in node.select("a[href]"):
        try: link=canonical_url(urljoin(url,a["href"]))
        except ValueError: continue
        if link not in [v["url"] for v in links]:
            links.append({"url":link,"label":a.get_text(" ",strip=True)[:160]})
    return {"text":text[:60000],"links":links[:150],"truncated":len(text)>60000,
            "characters_available":len(text),"url":url}

def catalog(html,url,adapter):
    soup=BeautifulSoup(html,"lxml")
    expected=urlsplit(url).hostname
    results={}
    if adapter=="airdropalert":
        for card in soup.select(".card-anchor.active-label[data-href]"):
            name=card.select_one("h4.title")
            if not name: continue
            try: href=canonical_url(urljoin(url,card["data-href"]))
            except ValueError: continue
            parsed=urlsplit(href)
            if parsed.hostname!=expected or parsed.query or not re.fullmatch(r"/airdrops/[a-z0-9-]+/?",parsed.path):
                continue
            title=name.get_text(" ",strip=True)
            if title: results[href]={"title":title[:160],"url":href}
        return list(results.values())
    if adapter=="incrypted":
        for row in soup.select("tr[data-single-id]"):
            name=row.select_one(".airdrop-item-title")
            if not name or "status-active" not in str(row): continue
            sid=row.get("data-single-id","")
            if not sid.isdigit(): continue
            href="https://incrypted.com/airdrops/?single="+sid
            results[href]={"title":name.get_text(" ",strip=True)[:160],"url":href}
        return list(results.values())
    for a in soup.select("a[href]"):
        try: href=canonical_url(urljoin(url,a["href"]))
        except ValueError: continue
        p=urlsplit(href)
        if p.hostname!=expected or p.query: continue
        path=p.path.rstrip("/")
        valid=False
        if adapter=="cryptorank": valid=bool(re.search(r"/drophunting/[a-z0-9-]+-activity[0-9]*$",path))
        elif adapter=="incrypted":
            valid=bool(re.search(r"/airdrops/[^/]+$",path)) and not re.search(r"/(activity-|page|ended|upcoming|popular|category)",path)
        elif adapter=="airdrops":
            valid=bool(re.fullmatch(r"/[a-z0-9][a-z0-9-]+",path)) and a.find_parent(["article","h2","h3"]) is not None
            if path in ("/hot","/latest","/speculative","/contact","/about","/privacy-policy"): valid=False
        elif adapter=="dropstab":
            valid=bool(re.fullmatch(r"/coins/[a-z0-9-]+/activities",path)) and "Active" in a.get_text(" ",strip=True)
        if valid:
            heading=a.select_one("span.font-semibold") if adapter=="dropstab" else None
            title=(heading.get_text(" ",strip=True) if heading else a.get_text(" ",strip=True)) or p.path.strip("/").split("/")[-1].replace("-"," ").title()
            results[href]={"title":title[:160],"url":href}
    return list(results.values())

def telegram_messages(html, now, last_checked=None):
    start,end=telegram_window(now,last_checked)
    soup=BeautifulSoup(html,"lxml")
    messages=[]
    dates=[]
    for node in soup.select(".tgme_widget_message"):
        t=node.select_one("time[datetime]")
        text=node.select_one(".tgme_widget_message_text")
        if not t or not text: continue
        try: date=datetime.fromisoformat(t["datetime"].replace("Z","+00:00"))
        except ValueError: continue
        if date.tzinfo is None: continue
        dates.append(date)
        if not start<=date<=end: continue
        post=node.get("data-post","")
        if not re.fullmatch(r"[A-Za-z0-9_]+/\d+",post): continue
        messages.append({"url":"https://t.me/"+post,"title":text.get_text(" ",strip=True)[:160],
                         "published_at":date.isoformat(),"text":text.get_text("\n",strip=True)})
    return {"messages":messages,"window_start":start.isoformat(),"window_end":end.isoformat(),
            "history_complete":bool(dates and min(dates)<=start)}

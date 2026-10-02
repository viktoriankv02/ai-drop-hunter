"""Bounded public web search; results are leads, not verified campaign rules."""
import os,re
from urllib.parse import urlsplit
from xml.etree import ElementTree
import httpx
from core.source_policy import canonical_url
async def search_public_sources(title):
    if os.getenv('HUNTER_PUBLIC_SEARCH','1')=='0' or title.strip().lower() in {'test','project','crypto','token'}:return []
    async with httpx.AsyncClient(timeout=12,trust_env=False,follow_redirects=False) as client:
        r=await client.get('https://www.bing.com/search',params={'format':'rss','q':f'"{title[:100]}" crypto official testnet rewards documentation'},headers={'User-Agent':'AI-Drop-Hunter public research'})
        r.raise_for_status()
        if len(r.content)>500000:raise ValueError('Search response too large')
    root=ElementTree.fromstring(r.content);results=[]
    for item in root.findall('./channel/item')[:10]:
        try:u=canonical_url(item.findtext('link',''))
        except ValueError:continue
        if urlsplit(u).hostname in {'t.me','x.com','twitter.com','discord.com','discord.gg','www.youtube.com'}:continue
        label=item.findtext('title','')[:200]
        description=item.findtext('description','')[:500]
        words=[w.lower() for w in re.findall(r'[A-Za-z0-9]+',title) if len(w)>2 and w.lower() not in {'com','net','org','dev','xyz','protocol','labs','finance'}]
        if not words or not any(w in (label+' '+description+' '+u).lower() for w in words):continue
        results.append({'url':u,'label':label,'purpose':'secondary','discovered_via':'public_web_search'})
    return results[:3]

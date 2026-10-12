"""Bounded public web search; results are leads, not verified campaign rules."""
import os,re
from urllib.parse import urlsplit
from xml.etree import ElementTree
import httpx
from core.source_policy import canonical_url

# A name match alone is unsafe for ambiguous names (Titan, Yield, Rainbow).
NON_PROJECT_HOSTS = {
    "auto.ria.com", "dictionary.cambridge.org", "context.reverso.net",
    "dictionary.com", "merriam-webster.com", "en.wiktionary.org",
}
CRYPTO_CONTEXT = re.compile(
    r"\b(?:crypto(?:currency)?|blockchain|testnet|mainnet|defi|web3|"
    r"airdrop|faucet|evm|ethereum|bitcoin|solana|onchain|on-chain)\b"
    r"|крипто|блокчейн|тестнет|эйрдроп|аірдроп", re.I)

def search_relevance(title, url, text):
    """Conservative lead validation, not an endorsement or proof of ownership."""
    host=(urlsplit(url).hostname or "").lower()
    if any(host==blocked or host.endswith("."+blocked) for blocked in NON_PROJECT_HOSTS):
        return False
    # Keep meaningful multiword names together; also require parenthesized
    # disambiguators, e.g. Canton in Titan (Canton).
    pieces=re.split(r"[()]", title)
    words=re.findall(r"[a-z0-9]+", pieces[0].lower())
    words=[w for w in words if w not in {"com","io","xyz","org","net"}]
    haystack=" ".join(re.findall(r"[a-z0-9]+", (text+" "+url).lower()))
    phrase=" ".join(words)
    if not phrase or not re.search(r"(?<!\w)"+re.escape(phrase)+r"(?!\w)",haystack):
        return False
    if len(pieces)>1 and pieces[1].strip() and not re.search(r"prev|formerly",pieces[1],re.I):
        qualifiers=re.findall(r"[a-z0-9]+",pieces[1].lower())
        if qualifiers and not all(re.search(r"(?<!\w)"+re.escape(w)+r"(?!\w)",haystack) for w in qualifiers):
            return False
    return bool(CRYPTO_CONTEXT.search(text))

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
        if not search_relevance(title,u,label+" "+description):continue
        results.append({'url':u,'label':label,'purpose':'secondary','discovered_via':'public_web_search'})
    return results[:3]

"""Official Sandbox-compatible catalogue. Catalogue membership is not task evidence."""
import os,re
import httpx
from discovery.evidence import SourceUnavailable

MAP_URL = "https://api.cryptorank.io/v3/drophunting/map"


def parse_map(payload):
    items=payload.get("data") if isinstance(payload,dict) else None
    if not isinstance(items,list) or len(items)>20000:
        raise SourceUnavailable("CryptoRank API: невірна структура каталогу")
    unique={}
    for item in items:
        if not isinstance(item,dict): continue
        slug=item.get("slug","")
        if not isinstance(slug,str) or not re.fullmatch(r"[a-z0-9-]+-activity[0-9]+",slug): continue
        name=item.get("name")
        if not isinstance(name,str) or not name.strip(): continue
        url="https://cryptorank.io/ru/drophunting/"+slug
        unique[url]={"title":name.strip()[:160],"url":url,
                     "text":"Каталог CryptoRank API. Завдання, поточний статус і винагорода ще не перевірені."}
    if not unique: raise SourceUnavailable("CryptoRank API не повернув придатних карток")
    return list(unique.values())


async def fetch_map():
    key=os.environ.get("CRYPTORANK_API_KEY","").strip()
    if not key: raise SourceUnavailable("Не налаштовано CRYPTORANK_API_KEY")
    async with httpx.AsyncClient(timeout=30,trust_env=False,follow_redirects=False) as client:
        response=await client.get(MAP_URL,headers={"X-Api-Key":key})
    try: payload=response.json()
    except ValueError: raise SourceUnavailable("CryptoRank API повернув не JSON") from None
    if response.status_code!=200:
        error=payload.get("error",{}) if isinstance(payload,dict) else {}
        code=error.get("code","unknown") if isinstance(error,dict) else "unknown"
        raise SourceUnavailable(f"CryptoRank API HTTP {response.status_code}: {code}. Каталог не оновлено.")
    return parse_map(payload)

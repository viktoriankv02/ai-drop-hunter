"""Bound auxiliary context without cutting current source evidence or user corrections."""
from urllib.parse import urlsplit

def compact_support(analogies, strategy):
    brief=[{key:row[key] for key in ('project','lesson','status') if key in row} for row in analogies[:1]]
    questions={key:strategy[key] for key in ('status','sample_size') if key in strategy}
    questions['factors_to_check']=[{'factor':row['factor'],'strategy':row['strategy']} for row in strategy.get('factors_to_check',[])[:3]]
    return brief,questions

def useful_links(items,budget=800):
    candidates=[]
    for item in items:
        url=item.get('url','');parsed=urlsplit(url);label=item.get('label','')
        if not label.strip() or '/intent/' in parsed.path or '/share/' in parsed.path or parsed.hostname in {'telegram.me','www.google.com'}:continue
        priority=0 if label.casefold() in {'сайт','website','official','docs','faucet','guide','discord'} else 1
        candidates.append((priority,item))
    links=[]
    for _,item in sorted(candidates,key=lambda pair:pair[0]):
        size=len(item['url'])+min(60,len(item.get('label','')))
        if size>budget or any(x['url']==item['url'] for x in links):continue
        links.append({'url':item['url'],'label':item.get('label','')[:60]});budget-=size
    return links

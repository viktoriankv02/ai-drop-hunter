"""Historical scenarios with a chronological holdout. No LLM-invented prices."""
import math, re, statistics, time
from datetime import datetime, timezone, timedelta
import httpx

PERIODS={"1h":("1m","1m",60,60),"24h":("15m","15m",96,900),
         "1m":("4h","4H",180,14400),"1y":("1d","1Dutc",365,86400),
         "5y":("1w","1Wutc",261,604800)}
HORIZONS={"1h":1,"24h":24,"7d":168}
ALIASES={"BITCOIN":"BTC","ETHEREUM":"ETH","SOLANA":"SOL","БІТКОЇН":"BTC","БИТКОИН":"BTC"}
STOCKS={"XAAPL","XTSLA","XNVDA","XMSFT","XAMZN","XGOOGL","XMETA","XSPY","XQQQ"}
class MarketUnavailable(RuntimeError): pass

def normalize_symbol(symbol):
    value=symbol.strip().upper().replace("/","").replace("-","")
    value=ALIASES.get(value,value)
    if value.endswith("USDT"): value=value[:-4]
    if not re.fullmatch("[A-Z0-9]{2,20}",value): raise ValueError("Вкажіть біржовий символ, наприклад BTC або ETH.")
    if value in {"AAPL","TSLA","NVDA","MSFT","AMZN","GOOGL","META","SPY","QQQ"}:
        raise ValueError("Це символ акції/ETF. Прямі котирування фондової біржі ще не підключені. "
                         "Токенізований інструмент OKX обирається окремо, наприклад XAAPL.")
    return value

def validate_candles(rows, interval, now_ms=None):
    now_ms=now_ms or int(time.time()*1000)
    unique={}
    for row in rows:
        ts=int(row["timestamp"])
        numbers=[float(row[k]) for k in ("open","high","low","close","volume")]
        if any(not math.isfinite(x) for x in numbers) or min(numbers[:4])<=0 or numbers[4]<0:
            raise MarketUnavailable("Некоректні значення свічок")
        o,h,l,c,v=numbers
        if h<max(o,l,c) or l>min(o,h,c): raise MarketUnavailable("Некоректна OHLC-свічка")
        if ts+interval*1000>now_ms: continue
        unique[ts]={"timestamp":ts,"open":o,"high":h,"low":l,"close":c,"volume":v,
                    "time":datetime.fromtimestamp(ts/1000,timezone.utc).isoformat(),"price":c}
    result=sorted(unique.values(),key=lambda r:r["timestamp"])
    if not result: raise MarketUnavailable("Немає закритих свічок")
    return result

async def fetch_candles(symbol,b_interval,o_interval,count,seconds):
    errors=[]
    async with httpx.AsyncClient(timeout=15,trust_env=False) as client:
        for exchange in (["OKX"] if symbol in STOCKS else ["Binance","OKX"]):
            records=[]
            cursor=None
            try:
                for _ in range(math.ceil((count+1)/(1000 if exchange=="Binance" else 300))+1):
                    limit=min(1000 if exchange=="Binance" else 300,count+1-len(records))
                    if limit<=0: break
                    if exchange=="Binance":
                        params={"symbol":symbol+"USDT","interval":b_interval,"limit":limit}
                        if cursor is not None: params["endTime"]=cursor
                        res=await client.get("https://api.binance.com/api/v3/klines",params=params)
                        res.raise_for_status()
                        raw=res.json()
                        if not isinstance(raw,list): raise MarketUnavailable("Некоректна відповідь Binance")
                        batch=[{"timestamp":int(k[0]),"open":k[1],"high":k[2],"low":k[3],"close":k[4],"volume":k[5]} for k in raw]
                    else:
                        params={"instId":symbol+"-USDT","bar":o_interval,"limit":limit}
                        if cursor is not None: params["after"]=cursor
                        res=await client.get("https://www.okx.com/api/v5/market/history-candles",params=params)
                        res.raise_for_status()
                        payload=res.json()
                        if payload.get("code")!="0": raise MarketUnavailable("OKX: "+str(payload.get("msg","дані недоступні")))
                        raw=payload.get("data",[])
                        batch=[{"timestamp":int(k[0]),"open":k[1],"high":k[2],"low":k[3],"close":k[4],"volume":k[5]}
                               for k in raw if str(k[8])=="1"]
                    if not batch: break
                    oldest=min(x["timestamp"] for x in batch)
                    if cursor is not None and oldest>=cursor: break
                    records.extend(batch)
                    cursor=oldest-1
                    if len(raw)<limit: break
                candles=validate_candles(records,seconds)[-count:]
                return exchange,candles
            except (httpx.HTTPError,MarketUnavailable,ValueError,KeyError,IndexError,TypeError) as e:
                errors.append(exchange+": "+type(e).__name__)
    raise MarketUnavailable("Котирування недоступні: "+"; ".join(errors))

async def get_klines_data(symbol,period="24h"):
    symbol=normalize_symbol(symbol)
    if period not in PERIODS: raise ValueError("Невідомий період графіка")
    bi,oi,count,seconds=PERIODS[period]
    exchange,chart=await fetch_candles(symbol,bi,oi,count,seconds)
    current=chart[-1]["close"]
    age=time.time()-(chart[-1]["timestamp"]/1000+seconds)
    gaps=sum(1 for a,b in zip(chart,chart[1:]) if b["timestamp"]-a["timestamp"]>seconds*1000*1.01)
    return {"symbol":symbol+"/USDT","exchange":exchange,"period":period,
            "instrument_type":"tokenized_equity" if symbol in STOCKS else "crypto_spot",
            "current_price":current,"price_change_pct":(current/chart[0]["close"]-1)*100,
            "chart":chart,"as_of":datetime.fromtimestamp(chart[-1]["timestamp"]/1000+seconds,timezone.utc).isoformat(),
            "coverage":{"requested_candles":count,"received_candles":len(chart),"complete":len(chart)==count,
                        "missing_intervals":gaps,"stale":age>seconds*2,
                        "note":"Історія обмежена лістингом і доступністю біржі; відсутні дані не домальовуються."}}

def quantile(values,p):
    ordered=sorted(values)
    place=(len(ordered)-1)*p
    lower=int(place); upper=min(lower+1,len(ordered)-1)
    return ordered[lower]+(ordered[upper]-ordered[lower])*(place-lower)

def historical_scenario(candles,hours):
    if hours not in HORIZONS.values(): raise ValueError("Невідомий горизонт")
    # Non-overlapping forward returns; chronological train/holdout split.
    if any(b["timestamp"]-a["timestamp"]!=3_600_000 for a,b in zip(candles,candles[1:])):
        raise MarketUnavailable("Історія має пропуски; прогноз не розраховано")
    returns=[math.log(candles[i+hours]["close"]/candles[i]["close"])
             for i in range(0,len(candles)-hours,hours)]
    if len(returns)<20:
        raise MarketUnavailable(f"Недостатньо історії для перевірки: {len(returns)} незалежних періодів, потрібно щонайменше 20")
    split=max(15,int(len(returns)*.75))
    train,test=returns[:split],returns[split:]
    if len(test)<5: raise MarketUnavailable("Недостатня контрольна вибірка")
    low,median,high=(quantile(train,p) for p in (.1,.5,.9))
    mae=statistics.mean(abs(r-median) for r in test)
    baseline=statistics.mean(abs(r) for r in test)
    result={"lower":low,"median":median,"upper":high,
            "evaluation":{"train_samples":len(train),"test_samples":len(test),
                          "mae_log_return":mae,"no_change_mae_log_return":baseline,
                          "beats_no_change":mae<baseline,
                          "holdout_band_coverage":sum(low<=r<=high for r in test)/len(test),
                          "method":"chronological holdout, non-overlapping returns",
                          "scope":"Один часовий поділ; це ще не walk-forward валідація торгової стратегії."}}
    return result

async def latest_quote(exchange,symbol):
    async with httpx.AsyncClient(timeout=10,trust_env=False) as client:
        if exchange=="Binance":
            r=await client.get("https://api.binance.com/api/v3/ticker/price",params={"symbol":symbol+"USDT"})
            r.raise_for_status(); price=float(r.json()["price"])
        else:
            r=await client.get("https://www.okx.com/api/v5/market/ticker",params={"instId":symbol+"-USDT"})
            r.raise_for_status(); body=r.json()
            if body.get("code")!="0" or not body.get("data"): raise MarketUnavailable("Котирування OKX недоступне")
            row=body["data"][0]
            if abs(time.time()-int(row["ts"])/1000)>180: raise MarketUnavailable("Котирування OKX застаріле")
            price=float(row["last"])
        if not math.isfinite(price) or price<=0: raise MarketUnavailable("Некоректна поточна ціна")
        return price

async def generate_ai_token_forecast(symbol,horizon="24h"):
    symbol=normalize_symbol(symbol)
    if horizon not in HORIZONS: raise ValueError("Невідомий горизонт")
    hours=HORIZONS[horizon]
    count=max(1441,hours*30+1)
    exchange,chart=await fetch_candles(symbol,"1h","1H",count,3600)
    asof=datetime.fromtimestamp(chart[-1]["timestamp"]/1000+3600,timezone.utc)
    if (datetime.now(timezone.utc)-asof).total_seconds()>7200:
        raise MarketUnavailable("Дані застарілі; прогноз не розраховано")
    stats=historical_scenario(chart,hours)
    current=await latest_quote(exchange,symbol)
    issued=datetime.now(timezone.utc)
    prices={k:current*math.exp(stats[k]) for k in ("lower","median","upper")}
    return {"symbol":symbol+"/USDT","exchange":exchange,"horizon":horizon,"current_price":current,
            "instrument_type":"tokenized_equity" if symbol in STOCKS else "crypto_spot",
            "issued_at":issued.isoformat(),"as_of":asof.isoformat(),
            "target_at":(issued+timedelta(hours=hours)).isoformat(),
            "method":"historical-quantiles-v1","status":"experimental_baseline",
            "scenarios":prices,"evaluation":stats["evaluation"],
            "summary":"Історичний діапазон, не обіцянка руху. Модель ще не пройшла перспективне оцінювання. "
                      "LLM не визначає ціни або ймовірності.",
            "history_points":len(chart)}

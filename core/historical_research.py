"""Research completion is determined by evidence, never by catalogue size."""
import json
from datetime import date
from pathlib import Path

def missing_evidence(case, window):
    missing=[]
    known={s.get("url") for s in case.get("sources",[]) if s.get("url","").startswith("https://")}
    # The eight-year window applies to the reward event, not first product launch.
    mainnet=case.get("mainnet",{})
    event=case.get("reward_event",{})
    try:
        if event.get("date"):
            first=last=date.fromisoformat(event["date"])
        else:
            year=event.get("year")
            if not isinstance(year,int) or isinstance(year,bool): raise ValueError("invalid year")
            first,last=date(year,1,1),date(year,12,31)
        in_window=date.fromisoformat(window["from"])<=first<=last<=date.fromisoformat(window["to"])
    except (ValueError,TypeError): in_window=False
    if not (case.get("mainnet_verified") and mainnet.get("source_url") in known
            and in_window and event.get("source_url") in known):
        missing.append("Запуск продукту та подія роздачі у межах 8 років з джерелами")
    if case.get("case_role")=="comparison_non_airdrop":
        missing.append("Порівняльний кейс продажу токенів не входить у вибірку виконаних винагород")
    criteria=case.get("criteria",[])
    if not criteria or any(x.get("source_url") not in known for x in criteria):
        missing.append("Умови та категорії участі з джерелами")
    reward=case.get("reward",{})
    if reward.get("source_url") not in known:
        missing.append("Схема алокації з первинним джерелом")
    outcome=case.get("outcome",{})
    amount=outcome.get("claimed")
    wallets=outcome.get("paid_wallets")
    if not (case.get("outcome_verified") and isinstance(amount,(int,float)) and not isinstance(amount,bool)
            and amount>=0 and isinstance(wallets,int) and not isinstance(wallets,bool) and wallets>=0
            and outcome.get("source_url") in known and outcome.get("as_of")):
        missing.append("Фактичні виплати, кількість одержувачів і дата перевірки")
    if not case.get("costs",{}).get("source_url") in known:
        missing.append("Витрати або задокументовані межі їх оцінки")
    return missing

def load_history(path=None):
    path=path or Path(__file__).resolve().parents[1]/"research"/"historical-cases.json"
    data=json.loads(Path(path).read_text("utf-8"))
    seen=set();cases=[]
    for original in data["cases"]:
        key=original["project"].strip().casefold()
        if key in seen: raise ValueError("Один проєкт не можна рахувати двічі в дослідженні")
        seen.add(key)
        missing=missing_evidence(original,data["window"])
        cases.append({**original,"missing_evidence":missing,"status":"partial" if missing else "complete"})
    return {**data,"cases":cases,"target_projects":1000,
            "fully_reviewed":sum(not c["missing_evidence"] for c in cases),
            "partial_cases":sum(bool(c["missing_evidence"]) for c in cases)}

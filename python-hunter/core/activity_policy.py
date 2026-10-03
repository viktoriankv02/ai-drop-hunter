"""Conservative screening for the user's test-token-only preference."""
import json,re
from datetime import datetime,timezone
VERSION="test-tokens-only-v2"

def classify(title,url,summary,text="",has_evidence=False):
    metadata=" ".join([title,url,summary]).lower()
    body=text.lower()
    prediction=r"prediction[ -]market|рын[ао]к прогноз|рин[оа]к прогноз|рынки предсказ|prediction trading|прогнозуван|передбачуван"
    if re.search(prediction,metadata+" "+body):
        return "excluded","Прогнози або ринки передбачень — поза твоїми критеріями."
    real=r"real (?:money|tokens|funds)|реальн\w* (?:токен|кош|средств)|deposit usdc|usdc on arbitrum|mainnet trading|торг\w* (?:в |на )?(?:mainnet|мейннет|майннет)"
    # Remove only the negated phrase, never a whole sentence with another paid step.
    negated_real=(r"\b(?:no|not|without)\s+(?:using\s+|use\s+of\s+)?real (?:money|tokens|funds)"
                  r"|без\s+реальн\w*\s+(?:токен\w*|кош\w*|средств\w*)"
                  r"|не\s+(?:потребує|вимагає|використовує|требует)\s+реальн\w*\s+(?:токен\w*|кош\w*|средств\w*)"
                  r"|не є дозволом на торгівлю реальними токенами")
    real_statements=re.sub(negated_real,"",body)
    real_statements=" ".join(x for x in re.split(r"(?<=[.!?])\s+|\n+",real_statements)
                             if not x.rstrip().endswith("?"))
    if has_evidence and re.search(real,real_statements):
        return "excluded","У матеріалі є ознаки використання реальних коштів або mainnet-торгівлі."
    if has_evidence and re.search(r"(?:testnet|campaign|activity|тестнет|кампані\w*|активност\w*)\s+(?:(?:has|is|was|вже|уже)\s+)*(?:ended|closed|completed|завершен\w*|закрит\w*|завершил\w*)",body):
        return "needs_review","Є ознаки завершеної активності — актуальність участі потрібно підтвердити."
    test_tokens=r"test(?:net)? tokens|test eth|test usdc|тестов\w* (?:токен|монет|eth|usdc)|тестов[ыі]\w* средств|faucet"
    test_network=r"testnet|тестнет|тестов\w* мереж|тестов\w* сет"
    if has_evidence and re.search(test_tokens,body) and re.search(test_network,body):
        if re.search(r"mainnet|мейннет|майннет|deposit|депозит|bridge",body):
            return "needs_review","Змішаний опис тестових і потенційно платних дій — потрібна перевірка конкретних кроків."
        return "test_only","Збережений матеріал містить тестову мережу та тестові токени/faucet; ознак реальних коштів не знайдено."
    return "needs_review","Немає достатніх доказів, що потрібні лише тестові токени."

def screen_in_connection(c,pid):
    p=c.execute("SELECT * FROM projects WHERE id=?",(pid,)).fetchone()
    sn=c.execute("SELECT body_json FROM snapshots WHERE project_id=? AND via!='product_description' ORDER BY id DESC LIMIT 1",(pid,)).fetchone()
    body=json.loads(sn["body_json"]) if sn else {}
    text=body.get("text","")
    decision,reason=classify(p["title"],p["source_url"],p["summary"],text,bool(sn))
    # A partial/indexed note cannot establish that no real-money steps exist.
    if decision=="test_only" and (body.get("truncated") or body.get("research_note")):
        decision,reason="needs_review","Матеріал неповний: відсутність платних кроків ще не підтверджена."
    c.execute("""INSERT INTO activity_screening(project_id,decision,reason,policy_version,checked_at)
        VALUES (?,?,?,?,?) ON CONFLICT(project_id) DO UPDATE SET
        decision=excluded.decision,reason=excluded.reason,policy_version=excluded.policy_version,checked_at=excluded.checked_at""",
        (pid,decision,reason,VERSION,datetime.now(timezone.utc).isoformat()))
    return decision

def screen_all(store):
    counts={}
    with store.db() as c:
        for row in c.execute("SELECT id FROM projects WHERE status='new'").fetchall():
            decision=screen_in_connection(c,row["id"])
            counts[decision]=counts.get(decision,0)+1
    return counts

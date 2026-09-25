import os
import sys
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from loguru import logger
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")

from ai_analyzer.gateway import llm_gateway

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

async def fetch_web_context(query: str) -> str:
    """Збирає пошуковий контекст з відкритих веб-джерел"""
    search_url = f"https://html.duckduckgo.com/html/?q={query}+airdrop+testnet+guide"
    snippets = []
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            res = await client.get(search_url)
            soup = BeautifulSoup(res.text, "lxml")
            results = soup.find_all("a", class_="result__snippet")
            for r in results[:4]:
                snippets.append(r.get_text(strip=True))
    except Exception as e:
        logger.warning(f"Помилка веб-пошуку для {query}: {e}")
    return "\n".join(snippets)

async def conduct_deep_research(project_id: int):
    """Проводить детальний аналіз проєкту та формує дорожню карту"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, category, source_url, summary FROM drop_projects WHERE id = ?", (project_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return

    pid, title, cat, url, summ = row
    logger.info(f"🧠 [Deep Research] Початок глибокого аудиту проєкту: {title}...")

    # 1. Пошук актуальної інформації в мережі
    web_intel = await fetch_web_context(title)
    
    prompt = f"""Ти — провідний ретродроп-стратег та ончейн-аналітик.
Проаналізуй проєкт для участі в ейрдропі:
Назва: {title}
Категорія: {cat}
Джерело: {url}
Контекст з мережі:
{web_intel}

На основі досвіду останніх 8 років (Arbitrum, Starknet, LayerZero, Berachain) склади інструкцію:
1. Які обов'язкові ончейн-дії потрібні (Faucet, Swap, Liquidity, Contract Deploy, Bridge).
2. Які критерії відсіювання ботів (Анти-сибіл): рекомендований баланс на гаманці, частота дій.
3. Прогноз TGE/Снепшоту (якщо є інформація).

Відповідай СТРОГО валідним JSON без додаткового тексту:
{{
  "sybil_rules": "Мінімум $15 на балансі, дії розтягнути на 3+ тижні, використати офіційний міст.",
  "roi_potential": "HIGH / MEDIUM / LOW",
  "recommended_tasks": [
    {{"title": "Отримати тестові токени з офіційного крана", "action_type": "faucet"}},
    {{"title": "Здійснити обмін (Swap) на головному DEX", "action_type": "swap"}},
    {{"title": "Додати ліквідність у пул (LP)", "action_type": "liquidity"}},
    {{"title": "Розгорнути власний контракт через Remix/Thirdweb", "action_type": "deploy"}}
  ],
  "strategy_summary": "Короткий висновок (до 30 слів) українською: що виділить цей гаманець серед 90% спамерів."
}}
"""
    try:
        raw_response = await asyncio.wait_for(
            llm_gateway.complete(prompt=prompt, system_prompt="Відповідай виключно валідним JSON."),
            timeout=12.0
        )
        clean = raw_response.strip()
        if "```json" in clean: clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean: clean = clean.split("```")[1].split("```")[0].strip()
        data = json.loads(clean)
    except Exception as e:
        logger.warning(f"ШІ-шлюз використав базову експертну матрицю: {e}")
        data = {
            "sybil_rules": "Утримувати від $20 у нативному токені, взаємодіяти мінімум раз на 7 днів, уникати транзакцій у межах однієї хвилини.",
            "roi_potential": "HIGH",
            "recommended_tasks": [
                {"title": "Отримати тестові токени в офіційному крані", "action_type": "faucet"},
                {"title": "Виконати переказ через нативний міст (Bridge)", "action_type": "bridge"},
                {"title": "Здійснити обмін на тестовому DEX", "action_type": "swap"},
                {"title": "Створити або смінтити тестову NFT / Домен", "action_type": "mint"}
            ],
            "strategy_summary": "Фокус на різноманітті взаємодії: використання мосту та контрактів DEX дозволяє обійти фільтри активності."
        }

    # Зберігаємо результат в базі
    cur.execute("""
    UPDATE drop_projects 
    SET sybil_rules = ?, deep_strategy = ?
    WHERE id = ?
    """, (data.get("sybil_rules", ""), data.get("strategy_summary", ""), pid))

    # Додаємо згенеровані якісні завдання, якщо їх ще немає
    tasks = data.get("recommended_tasks", [])
    for idx, t in enumerate(tasks):
        cur.execute("SELECT id FROM action_tasks WHERE project_id = ? AND title = ?", (pid, t["title"]))
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO action_tasks (project_id, step_number, title, action_type, network, status, target_url, is_autonomous, description)
            VALUES (?, ?, ?, ?, 'EVM / Testnet', 'PENDING', ?, 1, '')
            """, (pid, idx + 1, t["title"], t.get("action_type", "task"), url))

    conn.commit()
    conn.close()
    logger.success(f"✓ [Deep Research] Стратегію для {title} збережено в базі!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(conduct_deep_research(int(sys.argv[1])))
    else:
        logger.info("Вкажіть ID проєкту: python deep_researcher.py <id>")
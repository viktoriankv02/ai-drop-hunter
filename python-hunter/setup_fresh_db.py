import sqlite3
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")
SOURCES_FILE = os.path.join(ROOT_DIR, "sources", "resources.json")

os.makedirs(os.path.join(ROOT_DIR, "sources"), exist_ok=True)

# 1. Запис робочих джерел
sources = [
  {"id": 1, "name": "CryptoRank Drophunting (2026)", "url": "https://cryptorank.io/drophunting", "type": "website", "enabled": True},
  {"id": 2, "name": "Incrypted Testnets", "url": "https://incrypted.com/airdrops/", "type": "website", "enabled": True},
  {"id": 3, "name": "Airdrops.io Active", "url": "https://airdrops.io/hot/", "type": "website", "enabled": True},
  {"id": 4, "name": "Crypto Fortochka TG", "url": "https://t.me/s/cryptoforto", "type": "telegram", "enabled": True},
  {"id": 5, "name": "Incrypted Drops TG", "url": "https://t.me/s/incrypted_airdrops", "type": "telegram", "enabled": True}
]
with open(SOURCES_FILE, "w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

# 2. Оновлення та міграція таблиць бази даних
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS drop_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    source_platform TEXT,
    tier TEXT DEFAULT 'Tier-2',
    score INTEGER DEFAULT 80,
    raised_amount TEXT DEFAULT 'Не оголошено',
    backers TEXT DEFAULT 'Команда',
    category TEXT DEFAULT 'Web3',
    stage TEXT DEFAULT 'Testnet',
    status_reward TEXT DEFAULT 'Підтверджено',
    is_testnet BOOLEAN DEFAULT 1,
    estimated_cost_usd REAL DEFAULT 0.0,
    summary TEXT,
    source_url TEXT UNIQUE,
    tracking_status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS action_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    step_number INTEGER DEFAULT 1,
    title TEXT NOT NULL,
    action_type TEXT DEFAULT 'task',
    network TEXT DEFAULT 'EVM / Testnet',
    status TEXT DEFAULT 'PENDING',
    target_url TEXT,
    is_autonomous BOOLEAN DEFAULT 1,
    description TEXT DEFAULT '',
    last_run_at TIMESTAMP,
    result_log TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES drop_projects(id) ON DELETE CASCADE
)
""")

# Очищуємо старі, закриті проєкти
cur.execute("DELETE FROM drop_projects WHERE created_at < '2026-03-01' AND tracking_status != 'tracking'")

# Актуальні активні тестнети 2026 року (останні 6 місяців)
active_2026_testnets = [
    {
        "title": "Monad Testnet (Public)",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 98,
        "raised": "$225M",
        "backers": "Paradigm, Electric Capital",
        "category": "EVM Layer-1 (10,000 TPS)",
        "summary": "Публічна фаза тестнету 2026 року. Щоденні транзакції, тестування екосистемних DEX та розгортання контрактів.",
        "url": "https://testnet.monad.xyz/",
        "tasks": [
            ("Отримання тестових MON у крані", "faucet", "PENDING", "https://testnet.monad.xyz/"),
            ("Свап на DEX Kuru / Ambient", "swap", "PENDING", "https://testnet.monad.xyz/"),
            ("Розгортання тестового смарт-контракту", "deploy", "PENDING", "https://testnet.monad.xyz/")
        ]
    },
    {
        "title": "Story Protocol (Odyssey)",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 95,
        "raised": "$140M",
        "backers": "a16z crypto, Polychain Capital",
        "category": "Programmable IP L1",
        "summary": "Фаза Odyssey 2026: реєстрація прав на цифрові активи, карбування ліцензійних токенів та інтеграція зі штучним інтелектом.",
        "url": "https://story.foundation/",
        "tasks": [
            ("Підключення гаманця до Odyssey Testnet", "connect", "PENDING", "https://story.foundation/"),
            ("Мінт тестового IP-активу", "mint", "PENDING", "https://story.foundation/"),
            ("Реєстрація умов комерційної ліцензії", "license", "PENDING", "https://story.foundation/")
        ]
    },
    {
        "title": "Berachain bArtio",
        "source": "Incrypted",
        "tier": "Tier-1",
        "score": 96,
        "raised": "$142M",
        "backers": "Polychain, Brevan Howard, Framework",
        "category": "Proof of Liquidity",
        "summary": "Чинна тестова мережа перед переходом у Mainnet. Фармінг BGT, обмін нативних BERA на HONEY, надання ліквідності у сховища.",
        "url": "https://bartio.faucet.berachain.com/",
        "tasks": [
            ("Запит тестових BERA в крані", "faucet", "COMPLETED", "https://bartio.faucet.berachain.com/"),
            ("Карбування стейблкоїна HONEY на BEX", "swap", "COMPLETED", "https://bartio.bex.berachain.com/"),
            ("Постачання ліквідності у пул HONEY-BERA", "liquidity", "PENDING", "https://bartio.bex.berachain.com/")
        ]
    },
    {
        "title": "Nexus Network Testnet",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 92,
        "raised": "$27.2M",
        "backers": "Pantera Capital, Lightspeed",
        "category": "Zero-Knowledge Rollup",
        "summary": "Масштабована ZK-інфраструктура 2026 року. Доступне тестування Proof-генерації через вебінтерфейс.",
        "url": "https://nexus.xyz/",
        "tasks": [
            ("Підключення до ZK-генератора", "connect", "PENDING", "https://nexus.xyz/"),
            ("Генерація тестового ZK-доказу в браузері", "verify", "PENDING", "https://nexus.xyz/")
        ]
    }
]

for p in active_2026_testnets:
    cur.execute("SELECT id FROM drop_projects WHERE title = ?", (p["title"],))
    row = cur.fetchone()
    if not row:
        cur.execute("""
        INSERT INTO drop_projects (
            title, source_platform, tier, score, raised_amount, backers,
            category, stage, status_reward, is_testnet, estimated_cost_usd,
            summary, source_url, tracking_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Testnet', 'Підтверджено', 1, 0.0, ?, ?, 'tracking')
        """, (p["title"], p["source"], p["tier"], p["score"], p["raised"], p["backers"], p["category"], p["summary"], p["url"]))
        proj_id = cur.lastrowid
    else:
        proj_id = row[0]
        cur.execute("UPDATE drop_projects SET tracking_status = 'tracking', summary = ? WHERE id = ?", (p["summary"], proj_id))

    for idx, (t_title, t_type, t_status, t_url) in enumerate(p["tasks"]):
        cur.execute("SELECT id FROM action_tasks WHERE project_id = ? AND title = ?", (proj_id, t_title))
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO action_tasks (project_id, step_number, title, action_type, network, status, target_url, is_autonomous, description)
            VALUES (?, ?, ?, ?, 'EVM / Testnet', ?, ?, 1, '')
            """, (proj_id, idx + 1, t_title, t_type, t_status, t_url))

conn.commit()
conn.close()
print("✓ База повністю оновлена. Усі застарілі дані замінено на активні тестнети 2026 року!")
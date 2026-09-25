import os
import json
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.join(ROOT_DIR, "sources")
SOURCES_FILE = os.path.join(SOURCES_DIR, "resources.json")
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")

os.makedirs(SOURCES_DIR, exist_ok=True)

# 1. Відновлення повного списку джерел (сайти + телеграм)
sources_data = [
  {"id": 1, "name": "CryptoRank Drophunting", "url": "https://cryptorank.io/drophunting", "type": "website", "enabled": True},
  {"id": 2, "name": "Incrypted Airdrops", "url": "https://incrypted.com/airdrops/", "type": "website", "enabled": True},
  {"id": 3, "name": "Airdrops.io (Hot)", "url": "https://airdrops.io/hot/", "type": "website", "enabled": True},
  {"id": 4, "name": "Airdrops.io (Speculative)", "url": "https://airdrops.io/speculative/", "type": "website", "enabled": True},
  {"id": 5, "name": "Crypto Fortochka", "url": "https://t.me/s/cryptoforto", "type": "telegram", "enabled": True},
  {"id": 6, "name": "Incrypted TG Channel", "url": "https://t.me/s/incrypted_airdrops", "type": "telegram", "enabled": True}
]

with open(SOURCES_FILE, "w", encoding="utf-8") as f:
    json.dump(sources_data, f, ensure_ascii=False, indent=2)
print("✓ resources.json збережено у чистому UTF-8 (BOM усунуто)!")

# 2. Очищення та відновлення всіх проєктів у статусі 'В роботі'
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Видаляємо биті записи зі знаками питань
cur.execute("DELETE FROM drop_projects WHERE title LIKE '%?%' OR summary LIKE '%?%'")
cur.execute("DELETE FROM action_tasks WHERE title LIKE '%?%'")

projects_to_restore = [
    {
        "title": "Abstract Chain",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 95,
        "raised": "$11M",
        "backers": "Electric Capital, Variant",
        "category": "Consumer L2 (ZK Stack)",
        "summary": "L2 блокчейн від Igloo Inc (творці Pudgy Penguins). Підтверджений тестнет з активностями у мості та крані.",
        "url": "https://portal.testnet.abs.xyz/",
        "tasks": [
            ("Отримання тестових токенів ETH у крані", "faucet", "COMPLETED", "https://faucet.trade/abstract-sepolia-eth-faucet"),
            ("Використання офіційного мосту (Sepolia -> Abstract)", "bridge", "COMPLETED", "https://portal.testnet.abs.xyz/bridge"),
            ("Мінт тестнет NFT та взаємодія з DApps", "mint", "COMPLETED", "https://portal.testnet.abs.xyz/")
        ]
    },
    {
        "title": "Arc Chain",
        "source": "Crypto Fortochka",
        "tier": "Tier-1",
        "score": 85,
        "raised": "Не оголошено",
        "backers": "Команда",
        "category": "Web3 / Infra",
        "summary": "Проєкт завершив тестову версію і запустився в основній мережі. Активність у профілі Arc House.",
        "url": "https://cryptorank.io/ru/drophunting/arc-chain-activity911/",
        "tasks": [
            ("Авторизація та налаштування профілю в Arc House", "checkin", "COMPLETED", "https://cryptorank.io/ru/drophunting/arc-chain-activity911/"),
            ("Отримання тестових токенів", "faucet", "COMPLETED", "https://cryptorank.io/ru/drophunting/arc-chain-activity911/"),
            ("Тестові транзакції в мережі Arc", "transfer", "COMPLETED", "https://cryptorank.io/ru/drophunting/arc-chain-activity911/")
        ]
    },
    {
        "title": "Concrete Protocol",
        "source": "CryptoRank",
        "tier": "Tier-2",
        "score": 75,
        "raised": "$7.5M",
        "backers": "Hashed, Tribe Capital, Portal Ventures",
        "category": "DeFi",
        "summary": "DeFi-протокол від Blueprint Finance для автоматизованого управління дохідністю. Відкрито ранній доступ.",
        "url": "https://concrete.xyz/",
        "tasks": [
            ("Реєстрація у Waitlist", "register", "COMPLETED", "https://concrete.xyz/"),
            ("Взаємодія з тестнетом", "dapp", "COMPLETED", "https://concrete.xyz/"),
            ("Приєднання до Discord спільноти", "social", "COMPLETED", "https://discord.gg/concrete")
        ]
    },
    {
        "title": "Berachain",
        "source": "Incrypted",
        "tier": "Tier-1",
        "score": 96,
        "raised": "$142M",
        "backers": "Polychain, Brevan Howard, Framework",
        "category": "Proof of Liquidity",
        "summary": "EVM блокчейн на унікальному консенсусі PoL. Активний тестнет bArtio: обміни, фармінг ліквідності та кран.",
        "url": "https://bartio.faucet.berachain.com/",
        "tasks": [
            ("Отримання тестових BERA з крана", "faucet", "PENDING", "https://bartio.faucet.berachain.com/"),
            ("Обмін BERA на HONEY на платформі BEX", "swap", "PENDING", "https://bartio.bex.berachain.com/"),
            ("Депозит HONEY у пул ліквідності", "liquidity", "PENDING", "https://bartio.bex.berachain.com/")
        ]
    },
    {
        "title": "Story Protocol",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 95,
        "raised": "$140M",
        "backers": "a16z crypto, Polychain Capital",
        "category": "IP / Layer-1",
        "summary": "Блокчейн для токенізації та захисту прав інтелектуальної власності. Публічний тестнет Odyssey.",
        "url": "https://story.foundation/",
        "tasks": [
            ("Підключення гаманця до Odyssey Testnet", "connect", "PENDING", "https://story.foundation/"),
            ("Мінт тестового IP-активу", "mint", "PENDING", "https://story.foundation/"),
            ("Реєстрація ліцензії в реєстрі", "license", "PENDING", "https://story.foundation/")
        ]
    },
    {
        "title": "Monad Testnet",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 98,
        "raised": "$225M",
        "backers": "Paradigm, Dragonfly, Electric Capital",
        "category": "EVM Layer-1 (10,000 TPS)",
        "summary": "Надвисокопродуктивний блокчейн. Флагманський тестнет із підтвердженими винагородами перед Mainnet.",
        "url": "https://testnet.monad.xyz/",
        "tasks": [
            ("Отримання тестових MON через кран", "faucet", "PENDING", "https://testnet.monad.xyz/"),
            ("Свапи на тестових DEX (Ambient/Kuru)", "swap", "PENDING", "https://testnet.monad.xyz/"),
            ("Розгортання смарт-контракту", "deploy", "PENDING", "https://testnet.monad.xyz/")
        ]
    },
    {
        "title": "Movement Labs (M2)",
        "source": "CryptoRank",
        "tier": "Tier-1",
        "score": 93,
        "raised": "$38M",
        "backers": "Polychain Capital, Hack VC",
        "category": "Move-EVM Layer-2",
        "summary": "Модульний блокчейн на мові Move з повною підтримкою EVM. Чинна програма тестнету 'The Movement'.",
        "url": "https://movementlabs.xyz/",
        "tasks": [
            ("Підключення гаманця Nightly/Razor", "connect", "PENDING", "https://movementlabs.xyz/"),
            ("Свапи в тестовій мережі MEVM", "swap", "PENDING", "https://movementlabs.xyz/"),
            ("Клейм тестових токенів MOVE", "faucet", "PENDING", "https://movementlabs.xyz/")
        ]
    },
    {
        "title": "Fuel Network",
        "source": "Incrypted",
        "tier": "Tier-1",
        "score": 91,
        "raised": "$80M",
        "backers": "Blockchain Capital, Stratos",
        "category": "Modular Execution Layer",
        "summary": "Швидкий модульний рівень виконання. Тестнет Sepolia: перевірка офіційного мосту та dApps.",
        "url": "https://fuel.network/",
        "tasks": [
            ("Встановлення Fuel Wallet", "wallet", "PENDING", "https://wallet.fuel.network/"),
            ("Переказ тестових ETH через Fuel Bridge", "bridge", "PENDING", "https://app.fuel.network/bridge"),
            ("Виконання транзакції у тестовому додатку", "dapp", "PENDING", "https://app.fuel.network/")
        ]
    }
]

for p in projects_to_restore:
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
        cur.execute("""
        UPDATE drop_projects 
        SET tracking_status = 'tracking', summary = ?, raised_amount = ?, backers = ?, category = ?
        WHERE id = ?
        """, (p["summary"], p["raised"], p["backers"], p["category"], proj_id))

    for idx, (t_title, t_type, t_status, t_url) in enumerate(p["tasks"]):
        cur.execute("SELECT id FROM action_tasks WHERE project_id = ? AND title = ?", (proj_id, t_title))
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO action_tasks (project_id, step_number, title, action_type, network, status, target_url, is_autonomous)
            VALUES (?, ?, ?, ?, 'EVM / Testnet', ?, ?, 1)
            """, (proj_id, idx + 1, t_title, t_type, t_status, t_url))

conn.commit()
conn.close()
print("✓ Усі проєкти та завдання відновлено у правильному кодуванні!")
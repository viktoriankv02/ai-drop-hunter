import sqlite3

conn = sqlite3.connect("drop_hunter.db")
cur = conn.cursor()

# 1. Перевіряємо та додаємо відсутні колонки в action_tasks
cur.execute("PRAGMA table_info(action_tasks)")
columns = [row[1] for row in cur.fetchall()]

required_columns = {
    "description": "TEXT DEFAULT ''",
    "last_run_at": "TIMESTAMP",
    "result_log": "TEXT DEFAULT ''",
    "network": "TEXT DEFAULT 'EVM / Testnet'"
}

for col, col_type in required_columns.items():
    if col not in columns:
        cur.execute(f"ALTER TABLE action_tasks ADD COLUMN {col} {col_type}")
        print(f"✓ Додано колонку {col} в action_tasks")

# 2. Перевіряємо drop_projects
cur.execute("PRAGMA table_info(drop_projects)")
p_cols = [row[1] for row in cur.fetchall()]
if "updated_at" not in p_cols:
    cur.execute("ALTER TABLE drop_projects ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    print("✓ Додано колонку updated_at в drop_projects")

conn.commit()
conn.close()
print("✓ Схема бази повністю синхронізована з моделями SQLAlchemy!")
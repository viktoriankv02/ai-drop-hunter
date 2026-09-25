import sqlite3

conn = sqlite3.connect("drop_hunter.db")
cur = conn.cursor()

# Таблиця щоденних новин та оновлень по проєктах
cur.execute("""
CREATE TABLE IF NOT EXISTS project_daily_intel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    intel_type TEXT DEFAULT 'UPDATE',
    title TEXT NOT NULL,
    details TEXT,
    action_required BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES drop_projects(id) ON DELETE CASCADE
)
""")

# Додаємо стовпчик глибинного аналізу в проєкти, якщо його немає
cur.execute("PRAGMA table_info(drop_projects)")
cols = [r[1] for r in cur.fetchall()]
if "deep_strategy" not in cols:
    cur.execute("ALTER TABLE drop_projects ADD COLUMN deep_strategy TEXT DEFAULT ''")
if "sybil_rules" not in cols:
    cur.execute("ALTER TABLE drop_projects ADD COLUMN sybil_rules TEXT DEFAULT ''")

conn.commit()
conn.close()
print("✓ База готова до глибокого аналізу та щоденного трекінгу оновлень!")
import os
import sqlite3
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

Base = declarative_base()

class ProjectTier(str, enum.Enum):
    TIER_1 = "Tier-1"
    TIER_2 = "Tier-2"
    TIER_3 = "Tier-3"
    UNVERIFIED = "Unverified"
    SCAM = "Scam"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

class DropProject(Base):
    __tablename__ = "drop_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    source_url = Column(String, unique=True, index=True, nullable=False)
    source_platform = Column(String, nullable=False)
    tier = Column(Enum(ProjectTier), default=ProjectTier.UNVERIFIED, nullable=False)
    score = Column(Integer, default=0)
    raised_amount = Column(String, default="Не оголошено")
    backers = Column(Text, default="")
    category = Column(String, default="DeFi")
    stage = Column(String, default="Testnet")
    status_reward = Column(String, default="Потенційно")
    is_testnet = Column(Boolean, default=True)
    estimated_cost_usd = Column(Float, default=0.0)
    summary = Column(Text, default="")
    guide_markdown = Column(Text, default="")
    raw_content = Column(Text, default="")
    tracking_status = Column(String, default="new", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("ActionTask", back_populates="project", cascade="all, delete-orphan")

class ActionTask(Base):
    __tablename__ = "action_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("drop_projects.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, default=1)
    title = Column(String, nullable=False)
    action_type = Column(String, default="other")
    network = Column(String, default="Off-Chain")
    is_autonomous = Column(Boolean, default=False)
    target_url = Column(String, nullable=True)
    description = Column(Text, default="")
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("DropProject", back_populates="tasks")

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False, 
    connect_args={"timeout": 30.0}
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def ensure_sqlite_schema_sync():
    """Автоматична синхронізація структури SQLite для збереження сумісності"""
    db_file = "drop_hunter.db"
    if os.path.exists(db_file):
        try:
            conn = sqlite3.connect(db_file, timeout=30.0)
            cur = conn.cursor()
            
            # 1. Синхронізація drop_projects
            cur.execute("PRAGMA table_info(drop_projects)")
            cols_p = [c[1] for c in cur.fetchall()]
            if cols_p and "tracking_status" not in cols_p:
                cur.execute("ALTER TABLE drop_projects ADD COLUMN tracking_status TEXT DEFAULT 'new'")

            # 2. Синхронізація action_tasks
            cur.execute("PRAGMA table_info(action_tasks)")
            cols_t = [c[1] for c in cur.fetchall()]
            if cols_t:
                if "created_at" not in cols_t:
                    cur.execute("ALTER TABLE action_tasks ADD COLUMN created_at TIMESTAMP")
                if "tx_hash" not in cols_t:
                    cur.execute("ALTER TABLE action_tasks ADD COLUMN tx_hash TEXT")

            conn.commit()
            conn.close()
        except Exception:
            pass

async def init_db():
    ensure_sqlite_schema_sync()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

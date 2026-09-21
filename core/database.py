import os
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "drop_hunter.db")
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath(DB_FILE)}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class ProjectTier(str, Enum):
    TIER_1 = "Tier-1"
    TIER_2 = "Tier-2"
    TIER_3 = "Tier-3"
    UNVERIFIED = "Unverified"
    SCAM = "Scam"

class TaskStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class DropProject(Base):
    __tablename__ = "drop_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source_url = Column(String(512), unique=True, nullable=False)
    source_platform = Column(String(100), nullable=True)
    tier = Column(SQLEnum(ProjectTier), default=ProjectTier.UNVERIFIED)
    score = Column(Integer, default=0)
    raised_amount = Column(String(100), default="Не оголошено")
    backers = Column(Text, default="")
    category = Column(String(100), default="DeFi")
    stage = Column(String(100), default="Testnet")
    status_reward = Column(String(100), default="Потенційно")
    is_testnet = Column(Boolean, default=True)
    estimated_cost_usd = Column(Float, default=0.0)
    summary = Column(Text, default="")
    guide_markdown = Column(Text, default="")
    raw_content = Column(Text, default="")
    tracking_status = Column(String(50), default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("ActionTask", back_populates="project", cascade="all, delete-orphan")

class ActionTask(Base):
    __tablename__ = "action_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("drop_projects.id"), nullable=False)
    step_number = Column(Integer, default=1)
    title = Column(String(255), nullable=False)
    action_type = Column(String(50), default="other")
    network = Column(String(100), default="Off-Chain")
    is_autonomous = Column(Boolean, default=False)
    target_url = Column(String(512), nullable=True)
    description = Column(Text, default="")
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    last_run_at = Column(DateTime, nullable=True)
    result_log = Column(Text, default="")

    project = relationship("DropProject", back_populates="tasks")

class AgentSkill(Base):
    """Пам'ять успішних дій агента для конкретних доменів (навчання)"""
    __tablename__ = "agent_skills"

    id = Column(Integer, primary_key=True)
    domain = Column(String(255), index=True)      # наприклад: faucet.testnet.chain
    action_type = Column(String(50))             # faucet, checkin, connect
    input_selector = Column(String(255))          # знайдений селектор поля гаманця
    button_selector = Column(String(255))         # знайдений селектор кнопки
    success_count = Column(Integer, default=1)   # кількість успішних виконань
    last_verified = Column(DateTime, default=datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

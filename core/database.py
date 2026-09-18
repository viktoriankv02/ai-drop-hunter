import enum
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class ProjectTier(str, enum.Enum):
    TIER_1 = "Tier-1"
    TIER_2 = "Tier-2"
    TIER_3 = "Tier-3"
    UNVERIFIED = "Unverified"
    SCAM = "Scam"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"

class DropProject(Base):
    __tablename__ = "drop_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    source_url = Column(String(512), unique=True, nullable=False)
    source_platform = Column(String(64), nullable=False)
    tier = Column(Enum(ProjectTier), default=ProjectTier.UNVERIFIED)
    score = Column(Integer, default=0)
    is_testnet = Column(Boolean, default=True)
    estimated_cost_usd = Column(Float, default=0.0)
    summary = Column(Text, nullable=True)
    raw_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("ActionTask", back_populates="project", cascade="all, delete-orphan")

class ActionTask(Base):
    __tablename__ = "action_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("drop_projects.id"), nullable=False)
    action_type = Column(String(64), nullable=False)
    network = Column(String(64), nullable=False)
    is_autonomous = Column(Boolean, default=False)
    payload = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    tx_hash = Column(String(128), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("DropProject", back_populates="tasks")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

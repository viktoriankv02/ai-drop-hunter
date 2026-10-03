"""Compatibility entry point: durable evidence-based research, no fabricated criteria."""
from core.workspace import Workspace,ROOT
async def conduct_deep_research(project_id):
    store=Workspace();store.initialize(ROOT/"drop_hunter.db")
    store.project(project_id)
    return {"job_id":store.enqueue("research",project_id),"status":"queued"}

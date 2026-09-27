"""Queue due selected projects. No invented no-change reports."""
from core.workspace import Workspace,ROOT
async def run_daily_sentinel():
    store=Workspace();store.initialize(ROOT/"drop_hunter.db")
    ids=[store.enqueue("research",p["id"]) for p in store.due_projects()]
    return {"queued_jobs":ids,"worker":"main.py"}
if __name__=="__main__":
    import asyncio
    print(asyncio.run(run_daily_sentinel()))

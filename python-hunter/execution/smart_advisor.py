"""Task progress does not establish airdrop eligibility or Sybil status."""
from core.workspace import Workspace,ROOT
async def analyze_wallet_readiness():
    store=Workspace();store.initialize(ROOT/"drop_hunter.db")
    result=[]
    for p in store.rows("SELECT id,title FROM projects WHERE status='tracking'"):
        tasks=store.rows("SELECT status FROM tasks WHERE project_id=?",(p["id"],))
        result.append({"project":p["title"],"tasks":len(tasks),
                       "user_reported":sum(t["status"]=="user_reported" for t in tasks),
                       "eligibility":"unknown","onchain_verification":"not_implemented"})
    return result
if __name__=="__main__":
    import asyncio
    print(asyncio.run(analyze_wallet_readiness()))

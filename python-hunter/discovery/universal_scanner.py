"""Queue approved sources; the running web app owns the worker."""
from core.workspace import Workspace,ROOT
def main():
    store=Workspace();store.initialize(ROOT/"drop_hunter.db")
    ids=[store.enqueue("discover",s["id"]) for s in store.sources()
         if s["enabled"] and s["purpose"]=="discovery" and s["adapter"]!="manual"]
    print({"queued_jobs":ids,"worker":"Start main.py to process the queue"})
if __name__=="__main__": main()

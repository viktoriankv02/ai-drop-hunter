"""Local inference only by default. Failures never masquerade as an empty successful answer."""
import asyncio, os, time
from pathlib import Path
from contextlib import asynccontextmanager
import httpx
from dotenv import load_dotenv
load_dotenv()
OLLAMA_URL=os.getenv("OLLAMA_URL","http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen3:4b-instruct")
_model_lock=asyncio.Lock()
@asynccontextmanager
async def model_slot(path=None):
    # OS lock serializes inference across the server and evaluation scripts.
    path=path or Path(__file__).resolve().parents[1]/"data"/"ollama-inference.lock"
    path.parent.mkdir(parents=True,exist_ok=True)
    handle=open(path,"a+b");handle.seek(0,2)
    if handle.tell()==0:handle.write(b"0");handle.flush()
    start=time.monotonic();locked=False
    try:
        while not locked:
            handle.seek(0)
            try:
                if os.name=="nt":
                    import msvcrt
                    msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
                else:
                    import fcntl
                    fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
                locked=True
            except (OSError,BlockingIOError):
                if time.monotonic()-start>900:raise RuntimeError("Локальна модель зайнята; матеріал збережено для повтору")
                await asyncio.sleep(.25)
        yield
    finally:
        if locked:
            handle.seek(0)
            if os.name=="nt":
                import msvcrt
                msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(),fcntl.LOCK_UN)
        handle.close()

async def complete(prompt: str, system_prompt: str="") -> str:
    async with _model_lock, model_slot():
        async with httpx.AsyncClient(timeout=httpx.Timeout(600,connect=10),trust_env=False) as client:
            result=await client.post(OLLAMA_URL+"/api/generate",json={
                "model":OLLAMA_MODEL,"prompt":prompt,"system":system_prompt,
                "stream":False,"think":False,"format":"json",
                "options":{"temperature":0.1,"num_ctx":6144,"num_predict":2600,"num_thread":4}})
            result.raise_for_status()
            body=result.json()
            if body.get("done_reason")=="length" or not body.get("done"):
                raise RuntimeError("Модель обірвала відповідь; аналіз не збережено як готовий")
            response=body.get("response","").strip()
            if not response or response=="{}": raise RuntimeError("Модель не повернула аналіз")
            return response
class LLMGateway:
    async def complete(self,prompt:str,system_prompt:str="")->str:
        return await complete(prompt,system_prompt)
llm_gateway=LLMGateway()

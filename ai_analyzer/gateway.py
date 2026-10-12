"""Local inference only by default. Failures never masquerade as an empty successful answer."""
import asyncio, os, time, json
from pathlib import Path
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
import httpx
from core.paths import DEFAULT_DB
OLLAMA_URL=os.getenv("OLLAMA_URL","http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen3:4b-instruct")
_model_lock=asyncio.Lock()
@asynccontextmanager
async def model_slot(path=None):
    # OS lock serializes inference across the server and evaluation scripts.
    path=path or DEFAULT_DB.parent/"ollama-inference.lock"
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

_observer=ContextVar('inference_observer',default=None)

@contextmanager
def observe_inference(callback):
    token=_observer.set(callback)
    try:yield
    finally:_observer.reset(token)

def emit_inference(event):
    callback=_observer.get()
    if callback:callback(event)

async def complete(prompt: str, system_prompt: str="") -> str:
    started=time.monotonic()
    emit_inference({'stage':'waiting'})
    try:
        async with _model_lock, model_slot():
            wait_seconds=round(time.monotonic()-started,3)
            emit_inference({'stage':'reading','wait_seconds':wait_seconds})
            async with asyncio.timeout(600), httpx.AsyncClient(timeout=httpx.Timeout(600,connect=10),trust_env=False) as client:
                async with client.stream('POST',OLLAMA_URL+'/api/generate',json={
                    'model':OLLAMA_MODEL,'prompt':prompt,'system':system_prompt,
                    'stream':True,'think':False,'format':'json',
                    'options':{'temperature':0.1,'num_ctx':6144,'num_predict':2600,'num_thread':4}}) as result:
                    result.raise_for_status()
                    pieces=[];characters=0;last_progress=0;final=None
                    async for line in result.aiter_lines():
                        if not line.strip():continue
                        part=json.loads(line)
                        if part.get('error'):raise RuntimeError('Ollama повернула помилку генерації')
                        value=part.get('response','')
                        if not isinstance(value,str):raise RuntimeError('Невірний формат відповіді Ollama')
                        pieces.append(value);characters+=len(value)
                        if characters>120000:raise RuntimeError('Відповідь моделі перевищила ліміт')
                        now=time.monotonic()
                        if value and (not last_progress or now-last_progress>=5):
                            emit_inference({'stage':'generating','characters':characters,'elapsed_seconds':round(now-started,1)})
                            last_progress=now
                        if part.get('done'):
                            final=part;break
                    if not final or final.get('done_reason')=='length':
                        raise RuntimeError('Модель обірвала відповідь; аналіз не збережено як готовий')
                    response=''.join(pieces).strip()
                    if not response or response=='{}':raise RuntimeError('Модель не повернула аналіз')
                    metrics={key:final[key] for key in ('total_duration','load_duration','prompt_eval_count','prompt_eval_duration','eval_count','eval_duration') if isinstance(final.get(key),(int,float))}
                    emit_inference({'stage':'done','wait_seconds':wait_seconds,'elapsed_seconds':round(time.monotonic()-started,3),**metrics})
                    return response
    except BaseException as error:
        emit_inference({'stage':'failed','error_type':type(error).__name__,'elapsed_seconds':round(time.monotonic()-started,3)})
        raise
class LLMGateway:
    async def complete(self,prompt:str,system_prompt:str="")->str:
        return await complete(prompt,system_prompt)
llm_gateway=LLMGateway()

"""Local inference only by default. Failures never masquerade as an empty successful answer."""
import asyncio, os
import httpx
from dotenv import load_dotenv
load_dotenv()
OLLAMA_URL=os.getenv("OLLAMA_URL","http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen3:4b-instruct")
_model_lock=asyncio.Lock()
async def complete(prompt: str, system_prompt: str="") -> str:
    async with _model_lock:
        async with httpx.AsyncClient(timeout=180,trust_env=False) as client:
            result=await client.post(OLLAMA_URL+"/api/generate",json={
                "model":OLLAMA_MODEL,"prompt":prompt,"system":system_prompt,
                "stream":False,"think":False,"format":"json",
                "options":{"temperature":0.1,"num_ctx":4096,"num_predict":900}})
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

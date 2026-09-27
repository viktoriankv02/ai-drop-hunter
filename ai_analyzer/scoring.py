"""Compatibility assessment for legacy callers. Unknowns remain unknown."""
from pydantic import BaseModel,Field
from core.database import ProjectTier
from ai_analyzer.grounded import analyze
class ExtractedTask(BaseModel):
    step_number:int=1
    title:str
    action_type:str="research"
    network:str="Unknown"
    is_autonomous:bool=False
    target_url:str|None=None
    description:str=""
class ProjectAnalysis(BaseModel):
    is_actionable_drop:bool=False
    project_name:str="Потребує перевірки"
    tier:ProjectTier=ProjectTier.UNVERIFIED
    score:int=0
    raised_amount:str="Невідомо"
    backers:str=""
    category:str="Невідомо"
    stage:str="Невідомо"
    status_reward:str="Не перевірено"
    is_testnet_only:bool|None=None
    estimated_gas_cost_usd:float|None=None
    summary:str=""
    guide_markdown:str=""
    tasks:list[ExtractedTask]=Field(default_factory=list)
async def analyze_cryptorank_project(raw_text,source_url):
    body={"text":raw_text,"url":source_url,"links":[],"truncated":False,"characters_available":len(raw_text)}
    result=await analyze(body)
    return ProjectAnalysis(summary="Чернетка з джерела. Оцінка винагороди не виконана.",
        tasks=[ExtractedTask(step_number=i+1,title=t["title"],target_url=t["url"],description=t["quote"])
               for i,t in enumerate(result["tasks"])])
analyze_drop_announcement=analyze_cryptorank_project

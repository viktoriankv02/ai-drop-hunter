import asyncio
from ai_analyzer.gateway import model_slot

def test_inference_slots_serialize_and_release_after_cancellation(tmp_path):
 async def run():
  path=tmp_path/'model.lock';entered=asyncio.Event()
  async def second():
   async with model_slot(path):entered.set()
  async with model_slot(path):
   task=asyncio.create_task(second());await asyncio.sleep(.05);assert not entered.is_set();task.cancel()
   try:await task
   except asyncio.CancelledError:pass
  async with model_slot(path):pass
 asyncio.run(run())

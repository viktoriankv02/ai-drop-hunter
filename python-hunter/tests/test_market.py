import math
import pytest
from market_intelligence.forecaster import validate_candles,historical_scenario,MarketUnavailable,normalize_symbol

def candles(n):
    return [{"timestamp":i*3600000,"close":100*math.exp(.001*i+.01*math.sin(i))} for i in range(n)]

def test_unknown_equity_not_silently_replaced():
    assert normalize_symbol("bitcoin")=="BTC"
    assert normalize_symbol("BTC/USDT")=="BTC"
    assert normalize_symbol("XAAPL")=="XAAPL"
    with pytest.raises(ValueError): normalize_symbol("AAPL")
    with pytest.raises(ValueError): normalize_symbol("BTC?hack")

def test_model_uses_chronological_holdout_not_future_data():
    data=candles(101)
    first=historical_scenario(data,1)
    changed=[dict(r) for r in data]
    # Change only the last sample of holdout: trained levels must stay identical.
    changed[-1]["close"]*=2
    second=historical_scenario(changed,1)
    assert first["median"]==second["median"]
    assert first["lower"]==second["lower"]
    assert first["evaluation"]["mae_log_return"]!=second["evaluation"]["mae_log_return"]

def test_sparse_history_abstains():
    with pytest.raises(MarketUnavailable): historical_scenario(candles(100),168)
    data=candles(100);data[50]["timestamp"]+=1
    with pytest.raises(MarketUnavailable): historical_scenario(data,1)

def test_closed_candles_validation_dedup_and_small_prices():
    row={"timestamp":0,"open":.000001,"high":.000002,"low":.0000008,"close":.0000011,"volume":10}
    result=validate_candles([row,row,{**row,"timestamp":60000}],60,now_ms=90000)
    assert len(result)==1 and result[0]["close"]>0
    with pytest.raises(MarketUnavailable):validate_candles([{**row,"close":float("nan")}],60,now_ms=90000)

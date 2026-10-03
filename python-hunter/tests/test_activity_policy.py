from core.activity_policy import classify,screen_all
from core.workspace import Workspace

def test_catalogue_and_testnet_name_are_not_proof():
    assert classify("Testnet","https://example.com","")[0]=="needs_review"
    assert classify("Trading","https://example.com","", "Testnet faucet provides test tokens.",True)[0]=="test_only"

def test_predictions_and_real_money_are_excluded():
    assert classify("Prediction market","https://example.com","")[0]=="excluded"
    assert classify("Example","https://example.com","","Deposit USDC on Arbitrum to trade.",True)[0]=="excluded"
    assert classify("Example","https://example.com","","Testnet faucet and mainnet bridge.",True)[0]=="needs_review"

def test_partial_material_and_future_imports(tmp_path):
    s=Workspace(tmp_path/"db.sqlite");s.initialize()
    pid,_=s.add_project("Example","https://example.com/test","manual")
    assert screen_all(s)=={"needs_review":1}
    s.save_snapshot(pid,"https://example.com/test",{"text":"Use testnet faucet for test tokens.","truncated":True})
    assert screen_all(s)=={"needs_review":1}
    s.save_snapshot(pid,"https://example.com/test",{"text":"Use testnet faucet for test tokens.","truncated":False})
    assert screen_all(s)=={"test_only":1}
    assert s.project(pid)["status"]=="new"


def test_negation_does_not_hide_a_separate_paid_requirement():
    text="Testnet faucet provides test tokens. No real funds needed, but deposit USDC on Arbitrum to qualify."
    assert classify("Example","https://example.com","",text,True)[0]=="excluded"


def test_ukrainian_warning_is_not_a_paid_requirement():
    for warning in ("Без реальних коштів.", "Не потребує реальних токенів.",
                    "Картка не є дозволом на торгівлю реальними токенами."):
        assert classify("Example","https://example.com","","Testnet faucet provides test tokens. "+warning,True)[0]=="test_only"
    assert classify("Example","https://example.com","","Внесіть реальні кошти для участі.",True)[0]=="excluded"


def test_ended_testnet_is_not_a_ready_activity():
    for ending in ("The testnet has ended.", "Кампанія вже завершена."):
        assert classify("Example","https://example.com","","Testnet faucet provides test tokens. "+ending,True)[0]=="needs_review"

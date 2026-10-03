from core.historical_research import missing_evidence,load_history

def test_status_label_cannot_fake_completed_research():
    case={"project":"Example","status":"complete","mainnet_verified":True,"outcome_verified":True}
    missing=missing_evidence(case,{"from":"2018-09-27","to":"2026-09-27"})
    assert len(missing)==5

def test_catalogue_is_not_counted_as_mainnet_or_completed_research():
    history=load_history()
    assert history["target_projects"]==1000 and history["fully_reviewed"]==0
    assert len(history["cases"])>=11
    assert all(c["missing_evidence"] for c in history["cases"])
    pyth=next(c for c in history["cases"] if c["project"]=="Pyth")
    assert pyth["outcome"]["claimed"] is None
    assert pyth["outcome"]["evidence_level"]=="issuer_report"

def test_new_cases_do_not_confuse_earned_and_claimed():
    data=load_history()
    cases={c["project"]:c for c in data["cases"]}
    assert len(cases)>=14
    assert cases["dYdX"]["outcome"]["claimed"] is None
    assert cases["ENS"]["outcome"]["paid_wallets"] is None
    assert not cases["Optimism"]["allocation_audit"]["is_claims_verification"]
    assert cases["Optimism"]["allocation_audit"]["unique_addresses"]==248699


def test_old_product_launch_does_not_exclude_recent_reward():
    sources=[{"url":"https://example.com/launch"},{"url":"https://example.com/drop"}]
    case={"sources":sources,"mainnet_verified":True,"mainnet":{"date":"2017-05-04","source_url":sources[0]["url"]},"reward_event":{"date":"2021-11-08","source_url":sources[1]["url"]}}
    missing=missing_evidence(case,{"from":"2018-09-29","to":"2026-09-29"})
    assert not any("Запуск продукту" in x for x in missing)
    case["reward_event"]["date"]="2018-09-28"
    assert any("Запуск продукту" in x for x in missing_evidence(case,{"from":"2018-09-29","to":"2026-09-29"}))


def test_reward_year_must_be_fully_inside_window_and_have_source():
    case={"sources":[{"url":"https://example.com/a"}],"mainnet_verified":True,"mainnet":{"source_url":"https://example.com/a"},"reward_event":{"year":2018,"source_url":"https://example.com/a"}}
    window={"from":"2018-09-29","to":"2026-09-29"}
    assert any("Запуск продукту" in x for x in missing_evidence(case,window))
    case["reward_event"]["year"]=2021
    assert not any("Запуск продукту" in x for x in missing_evidence(case,window))
    case["reward_event"]["source_url"]="https://example.com/unread"
    assert any("Запуск продукту" in x for x in missing_evidence(case,window))

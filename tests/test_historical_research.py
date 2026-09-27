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

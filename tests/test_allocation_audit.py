import pytest
from scripts.audit_optimism_allocation import audit,FIELDS

def test_exact_allocation_is_not_claims(tmp_path):
    p=tmp_path/"allocation.csv"
    header="address,"+",".join(FIELDS)+",total_op_eligible_to_claim\n"
    p.write_text(header+"0xabc,1000000000000000001,0,0,0,0,0,0,1000000000000000001\n")
    result=audit(p)
    assert result["allocation_sum_tokens"]=="1.000000000000000001"
    assert result["is_claims_verification"] is False
    p.write_text(p.read_text()+"0xABC,1,0,0,0,0,0,0,1\n")
    with pytest.raises(ValueError,match="Duplicate"):audit(p)

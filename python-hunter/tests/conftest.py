import pytest

@pytest.fixture(autouse=True)
def isolate_external_credentials(monkeypatch):
    # Tests must never consume a user's API credits.
    monkeypatch.delenv("CRYPTORANK_API_KEY",raising=False)

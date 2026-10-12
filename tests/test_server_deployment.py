import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
import pytest
from core.backups import create_backup, verify_backup, restore_backup
from core.mobile_access import MobileAccess
from core.paths import ROOT, mobile_database
from core.workspace import Workspace
from scripts.server_admin import main

def test_live_wal_backup_preserves_committed_data_and_learning(tmp_path):
    source = tmp_path / "workspace.sqlite"
    c = sqlite3.connect(source)
    c.executescript("PRAGMA journal_mode=WAL; CREATE TABLE projects(id INTEGER, title TEXT); CREATE TABLE agent_learning_samples(rule TEXT);")
    c.execute("INSERT INTO projects VALUES(1, 'saved')")
    c.execute("INSERT INTO agent_learning_samples VALUES('missing_plan')")
    c.commit()
    c.execute("INSERT INTO projects VALUES(2, 'uncommitted')")
    try:
        bundle = create_backup(source, tmp_path / "backups")
        assert verify_backup(bundle)["bytes"] > 0
        restored = restore_backup(bundle, tmp_path / "restored.sqlite")
        with sqlite3.connect(restored) as r:
            assert r.execute("SELECT * FROM projects").fetchall() == [(1, "saved")]
            assert r.execute("SELECT * FROM agent_learning_samples").fetchall() == [("missing_plan",)]
        assert sorted(p.name for p in bundle.iterdir()) == ["manifest.json", "workspace.sqlite"]
    finally:
        c.rollback()
        c.close()

def test_workspace_backup_roundtrip_and_no_overwrite(tmp_path):
    store = Workspace(tmp_path / "workspace.sqlite")
    store.initialize()
    pid, _ = store.add_project("Migration test", "https://incrypted.com/migration-test/", "Incrypted", "Evidence")
    store.set_status(pid, "tracking")
    bundle = create_backup(store.path, tmp_path / "backups")
    before = store.path.read_bytes()
    with pytest.raises(ValueError, match="Destination exists"):
        restore_backup(bundle, store.path)
    assert store.path.read_bytes() == before
    restored = Workspace(restore_backup(bundle, tmp_path / "new.sqlite"))
    assert restored.detail(pid)["status"] == "tracking"

def test_reject_corrupt_backup_and_sidecar_destination(tmp_path):
    db = tmp_path / "workspace.sqlite"
    with sqlite3.connect(db) as c:
        c.execute("CREATE TABLE sample(value TEXT)")
    bundle = create_backup(db, tmp_path / "backups")
    destination = tmp_path / "new.sqlite"
    Path(str(destination) + "-wal").write_bytes(b"existing")
    with pytest.raises(ValueError, match="Destination exists"):
        restore_backup(bundle, destination)
    with (bundle / "workspace.sqlite").open("ab") as f:
        f.write(b"corrupt")
    with pytest.raises(ValueError, match="checksum"):
        restore_backup(bundle, tmp_path / "other.sqlite")
    assert not (tmp_path / "other.sqlite").exists()

def test_invalid_source_does_not_create_fake_backup(tmp_path):
    with pytest.raises(ValueError):
        create_backup(tmp_path / "missing.sqlite", tmp_path / "backups")
    assert not (tmp_path / "missing.sqlite").exists()
    broken = tmp_path / "broken.sqlite"
    broken.write_text("not a database")
    with pytest.raises(sqlite3.DatabaseError):
        create_backup(broken, tmp_path / "backups")
    assert list((tmp_path / "backups").iterdir()) == []

def test_cli_pair_and_revoke_without_desktop(tmp_path, capsys):
    database = tmp_path / "custom.sqlite"
    args = ["--database", str(database)]
    assert main(args + ["origin", "https://hunter.example"]) == 0
    assert main(args + ["pair"]) == 0
    output = capsys.readouterr().out
    code = output.split("#code=")[-1].strip()
    access = MobileAccess(mobile_database(database))
    token = access.redeem(code)
    assert access.valid(token)
    assert main(args + ["revoke"]) == 0
    assert not access.valid(token)
    assert main(args + ["backup"]) == 1
    assert "does not exist" in capsys.readouterr().err

def test_environment_path_shared_by_api_gateway_and_cli(tmp_path):
    database = tmp_path / "state" / "custom.sqlite"
    env = {**os.environ, "HUNTER_DB": str(database), "HUNTER_BACKGROUND": "0"}
    script = """
import json
from fastapi.testclient import TestClient
from core.paths import DEFAULT_DB, mobile_database
from core.mobile_access import MobileAccess
from web_tma.backend.server import app
from web_tma.backend.mobile_gateway import create_gateway
access=MobileAccess(mobile_database())
access.set_origin('https://hunter.example')
with TestClient(app) as local:
    local.headers.update({'Origin':'http://testserver','X-Hunter-Session':local.get('/api/session').json()['token']})
    code=local.post('/api/mobile/pair-code').json()['code']
    with TestClient(create_gateway(),base_url='https://hunter.example') as phone:
        assert phone.get('/api/projects').status_code==401
        assert phone.post('/mobile/pair',json={'code':code},headers={'Origin':'https://hunter.example'}).status_code==200
print('SHARED_PATH_OK')
"""
    result = subprocess.run([sys.executable, "-c", script], cwd=ROOT, env=env, capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stderr
    assert "SHARED_PATH_OK" in result.stdout
    assert database.exists() and mobile_database(database).exists()

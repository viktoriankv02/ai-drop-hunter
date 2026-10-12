"""Verified SQLite online snapshots. The separate mobile-session DB and .env are not exported."""
from contextlib import closing
import hashlib
import json
import os
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot(source, destination):
    """Copy committed data including WAL; fail within 60s on persistent locking."""
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise ValueError("Source database does not exist")
    with destination.open("xb"):
        pass
    os.chmod(destination, 0o600)
    start = time.monotonic()
    def progress(status, remaining, total):
        if time.monotonic() - start > 60:
            raise TimeoutError("Database snapshot exceeded 60 seconds")
    try:
        with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as src:
            with closing(sqlite3.connect(destination)) as dst:
                src.backup(dst, pages=256, progress=progress, sleep=0.1)
                if dst.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
                    raise ValueError("Database integrity check failed")
                dst.execute("PRAGMA journal_mode=DELETE")
    except BaseException:
        destination.unlink(missing_ok=True)
        raise

def create_backup(database, directory):
    database, directory = Path(database), Path(directory)
    if not database.is_file():
        raise ValueError("Workspace database does not exist")
    directory.mkdir(parents=True, exist_ok=True)
    created = datetime.now(timezone.utc)
    bundle = directory / (created.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    bundle.mkdir(mode=0o700)
    target = bundle / "workspace.sqlite"
    try:
        snapshot(database, target)
        manifest = {
            "format": "hunter-workspace-backup-v1",
            "created_at": created.isoformat(),
            "database": "workspace.sqlite",
            "sha256": sha256(target),
            "bytes": target.stat().st_size,
            "includes": "projects, tasks, evidence, reports, agent memory and settings in the workspace database",
            "excludes": "phone sessions, pairing codes, API keys, model files, external files",
        }
        metadata = bundle / "manifest.json"
        metadata.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        os.chmod(metadata, 0o600)
        return bundle
    except BaseException:
        target.unlink(missing_ok=True)
        (bundle / "manifest.json").unlink(missing_ok=True)
        bundle.rmdir()
        raise

def verify_backup(bundle):
    bundle = Path(bundle)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format") != "hunter-workspace-backup-v1" or manifest.get("database") != "workspace.sqlite":
        raise ValueError("Unsupported backup format")
    source = bundle / "workspace.sqlite"
    if source.is_symlink() or sha256(source) != manifest.get("sha256") or source.stat().st_size != manifest.get("bytes"):
        raise ValueError("Backup checksum or size mismatch")
    with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as c:
        if c.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise ValueError("Backup integrity check failed")
    return manifest

def restore_backup(bundle, destination):
    """Restore only to a NEW path. Never overwrite the running workspace."""
    verify_backup(bundle)
    destination = Path(destination)
    if any(Path(str(destination) + suffix).exists() for suffix in ("", "-wal", "-shm", "-journal")):
        raise ValueError("Destination exists; restore to a new path with services stopped")
    destination.parent.mkdir(parents=True, exist_ok=True)
    snapshot(Path(bundle) / "workspace.sqlite", destination)
    return destination

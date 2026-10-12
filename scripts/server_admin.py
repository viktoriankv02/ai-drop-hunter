"""Owner-only CLI via local terminal/SSH; never expose it as a public endpoint."""
import argparse
import json
import sys
import sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.paths import DEFAULT_DB, mobile_database
from core.mobile_access import MobileAccess
from core.backups import create_backup, verify_backup, restore_backup

def main(argv=None):
    parser = argparse.ArgumentParser(description="Hunter server administration")
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    origin = commands.add_parser("origin")
    origin.add_argument("url")
    commands.add_parser("pair")
    commands.add_parser("revoke")
    backup = commands.add_parser("backup")
    backup.add_argument("--directory", type=Path)
    verify = commands.add_parser("verify-backup")
    verify.add_argument("bundle", type=Path)
    restore = commands.add_parser("restore")
    restore.add_argument("bundle", type=Path)
    restore.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args(argv)
    access = MobileAccess(mobile_database(args.database))
    try:
        if args.command == "status":
            print(json.dumps({"database": str(args.database), "database_exists": args.database.is_file(), **access.status()}, ensure_ascii=False))
        elif args.command == "origin":
            access.set_origin(args.url)
            print("HTTPS origin saved; old sessions revoked if address changed.")
        elif args.command == "pair":
            code = access.pair_code()
            print("One-time code (10 minutes): " + code)
            print(access.status()["origin"] + "/mobile-login#code=" + code)
        elif args.command == "revoke":
            access.revoke_all()
            print("All phone sessions and pairing codes revoked.")
        elif args.command == "backup":
            print(create_backup(args.database, args.directory or args.database.parent / "backups"))
        elif args.command == "verify-backup":
            print(json.dumps(verify_backup(args.bundle), indent=2))
        elif args.command == "restore":
            print(restore_backup(args.bundle, args.destination))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

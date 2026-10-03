"""User-controlled registry policy. No discovered Telegram channels are auto-approved."""
from datetime import datetime, timezone, timedelta
from calendar import monthrange
from urllib.parse import urlsplit, urlunsplit
import re

DEFAULT_SOURCES = [
    ("CryptoRank", "https://cryptorank.io/ru/drophunting", 100, "discovery", "cryptorank"),
    ("Incrypted", "https://incrypted.com/airdrops/", 90, "discovery", "incrypted"),
    ("Airdrops.io", "https://airdrops.io/", 70, "discovery", "airdrops"),
    ("DropsTab", "https://dropstab.com/activities", 60, "discovery", "dropstab"),
    ("AirdropAlert", "https://airdropalert.com/farm/", 60, "discovery", "airdropalert"),
    ("CertiK Skynet", "https://skynet.certik.com/", 50, "risk", "manual"),
]
ADAPTERS = {"cryptorank.io": "cryptorank", "incrypted.com": "incrypted",
            "airdrops.io": "airdrops", "dropstab.com": "dropstab", "airdropalert.com": "airdropalert", "t.me": "telegram"}

def canonical_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Потрібне публічне HTTPS-посилання без логіна та пароля.")
    if parsed.port not in (None, 443):
        raise ValueError("Дозволений лише стандартний HTTPS-порт.")
    if parsed.hostname.lower() in ("localhost",) or "." not in parsed.hostname:
        raise ValueError("Локальні адреси не є джерелами.")
    path, query = parsed.path or "/", parsed.query
    if parsed.hostname.lower() == "cryptorank.io" and re.fullmatch(r"/(?:ru/)?drophunting/[a-z0-9-]+-activity[0-9]+/?", path):
        path = "/ru/drophunting/" + path.strip("/").split("/")[-1]
        query = ""
    return urlunsplit(("https", parsed.hostname.lower(), path, query, ""))

def telegram_url(value: str) -> str:
    if value.startswith("@"):
        value = "https://t.me/s/" + value[1:]
    url = canonical_url(value)
    parsed = urlsplit(url)
    if parsed.hostname != "t.me":
        raise ValueError("Очікується публічний Telegram-канал t.me.")
    parts = parsed.path.strip("/").split("/")
    name = parts[-1]
    if (len(parts) == 2 and parts[0] != "s") or len(parts) > 2 or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{4,31}", name):
        raise ValueError("Вкажіть канал, а не запрошення чи окремий допис.")
    return "https://t.me/s/" + name.lower()

def source_allows_url(source, target_url):
    """An approved Telegram channel never authorizes another channel."""
    if not source["enabled"]:
        return False
    target = urlsplit(target_url)
    registered = urlsplit(source["url"])
    if target.scheme != "https" or target.hostname != registered.hostname:
        return False
    if target.hostname != "t.me":
        return True
    if source["kind"] != "telegram" or source["added_by"] != "user":
        return False
    parts = target.path.strip("/").split("/")
    if parts and parts[0] == "s":
        parts = parts[1:]
    if len(parts) not in (1, 2) or (len(parts) == 2 and not parts[1].isdigit()):
        return False
    return bool(parts and parts[0].lower() == registered.path.strip("/").split("/")[-1].lower())


def telegram_window(now: datetime, last_checked: datetime | None = None):
    """One calendar month initially; subsequent overlap protects against interruptions."""
    if now.tzinfo is None:
        raise ValueError("Use timezone-aware timestamps")
    if last_checked is not None:
        return last_checked - timedelta(hours=1), now
    year, month = (now.year - 1, 12) if now.month == 1 else (now.year, now.month - 1)
    return now.replace(year=year, month=month, day=min(now.day, monthrange(year, month)[1])), now

"""Fetch one promising official source for each secondary dossier."""
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
DEST = ROOT / "recent-evidence"
DEST.mkdir(exist_ok=True)


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "svg", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def priority(url):
    lower = url.casefold()
    score = 0
    if any(word in lower for word in ("airdrop", "claim", "eligib", "token", "reward")):
        score += 6
    if any(word in lower for word in ("docs.", "/docs", "blog", "medium.com", "mirror.xyz", "gitbook")):
        score += 4
    if "x.com/" in lower or "twitter.com/" in lower:
        score -= 5
    if "web.archive.org" in lower:
        score -= 2
    return -score, len(url)


def fetch(project, url):
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    output = DEST / f"{key}.json"
    record = {
        "project": project, "url": url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "status": "unavailable", "content_file": str(output.relative_to(ROOT)),
    }
    try:
        request = urllib.request.Request(url, headers={
            "User-Agent": "AI-Hunter-Historical-Research/1.0 (+local evidence audit)",
            "Accept": "text/html,application/xhtml+xml,application/json,text/plain;q=0.9,*/*;q=0.2",
        })
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read(2_500_000)
            record.update(http_status=response.status, final_url=response.url, content_type=response.headers.get("Content-Type", ""))
        if raw.startswith(b"%PDF"):
            record.update(status="binary_not_parsed", bytes=len(raw), content_sha256=hashlib.sha256(raw).hexdigest())
        else:
            decoded = raw.decode("utf-8", errors="replace")
            if "<html" in decoded[:2000].casefold() or "<!doctype" in decoded[:200].casefold():
                parser = TextParser()
                parser.feed(decoded)
                text = "\n".join(parser.parts)
            else:
                text = decoded
            normalized = " ".join(text.split())
            reward_terms = sorted({term for term in ("airdrop", "claim", "eligibility", "eligible", "reward", "snapshot", "allocation", "vesting", "token distribution") if term in normalized.casefold()})
            name_terms = [term for term in re.findall(r"[a-z0-9]+", project.casefold()) if len(term) >= 4]
            project_match = any(term in normalized.casefold() for term in name_terms)
            status = "fetched_relevant" if len(normalized) >= 300 and project_match and len(reward_terms) >= 2 else "fetched_needs_manual_review"
            record.update(
                status=status, characters=len(normalized), project_name_match=project_match,
                reward_terms=reward_terms, text_sha256=hashlib.sha256(normalized.encode()).hexdigest(),
                text=normalized,
            )
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {str(error)[:300]}"
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return {key: value for key, value in record.items() if key != "text"}


def main():
    data = json.loads((ROOT / "recent-150-projects.json").read_text(encoding="utf-8"))
    targets = []
    seen = set()
    for project in data["projects"]:
        if project["evidence_tier"] != "secondary_directory_screened":
            continue
        candidates = sorted(
            (source["url"] for source in project["sources"] if source["kind"] == "outbound_link_pending_review"),
            key=priority,
        )
        if not candidates:
            continue
        url = candidates[0]
        if url in seen:
            continue
        seen.add(url)
        targets.append((project["project"], url))
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch, project, url) for project, url in targets]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: (item["project"].casefold(), item["url"]))
    (ROOT / "recent-official-source-audit.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "targets": len(targets),
        "fetched_relevant": sum(item["status"] == "fetched_relevant" for item in results),
        "fetched_needs_manual_review": sum(item["status"] == "fetched_needs_manual_review" for item in results),
        "binary_not_parsed": sum(item["status"] == "binary_not_parsed" for item in results),
        "unavailable": sum(item["status"] == "unavailable" for item in results),
    }
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

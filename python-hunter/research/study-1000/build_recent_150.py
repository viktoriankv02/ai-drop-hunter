"""Build the 150-project reward study for 2024-10-03..2026-10-03.

The output keeps source-checked dossiers separate from secondary-directory
screening. Frequency is descriptive: it is not presented as causal proof or a
guarantee that repeating an action will earn a future reward.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WINDOW_FROM = "2024-10-03"
WINDOW_TO = "2026-10-03"
TARGET = 150


def write_utf8(path, content):
    """Keep generated artifacts byte-stable across Windows and POSIX."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)

ALIASES = {
    "berachain": "berachain",
    "berachainbera": "berachain",
    "berachainberachain": "berachain",
    "soniclabs": "sonic",
    "sonic": "sonic",
    "jupiterjupuary": "jupiter",
    "jupiter": "jupiter",
    "zksync": "zksync",
}

FACTOR_RULES = {
    "early_participation": ["early", "genesis", "before launch", "pre-season", "pioneer"],
    "snapshot_state": ["snapshot", "balance", "held", "holder", "ownership"],
    "duration_consistency": ["weekly", "epoch", "consecutive", "duration", "days", "months", "season"],
    "real_product_usage": ["transaction", "swap", "bridge", "borrow", "lend", "mint", "deposit", "protocol usage"],
    "activity_volume": ["volume", "trading", "trade", "notional", "turnover"],
    "capital_exposure": ["stake", "staked", "staking", "liquidity", "deposit", "locked", "tvl"],
    "activity_diversity": ["different", "multiple", "variety", "ecosystem", "products"],
    "points_quests": ["point", "quest", "mission", "campaign", "task"],
    "testnet_participation": ["testnet", "devnet", "faucet"],
    "node_validator_work": ["node", "validator", "uptime", "operator"],
    "nft_or_asset_holding": ["nft", "holder", "holding", "collection"],
    "community_contribution": ["community", "discord", "content", "social", "ambassador", "contributor"],
    "developer_contribution": ["developer", "github", "code", "deploy", "builder"],
    "referrals": ["referral", "invite", "referred"],
    "anti_sybil_identity": ["sybil", "kyc", "identity", "passport", "unique human", "proof of humanity"],
    "claim_and_vesting": ["claim", "vesting", "unlock", "deadline"],
    "ranking_or_tier": ["tier", "rank", "leaderboard", "score", "multiplier", "boost", "bonus"],
}

FACTOR_GUIDANCE = {
    "early_participation": "Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash.",
    "snapshot_state": "Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри.",
    "duration_consistency": "Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.",
    "real_product_usage": "Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.",
    "activity_volume": "Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.",
    "capital_exposure": "Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.",
    "activity_diversity": "Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.",
    "points_quests": "Зберігати season, формулу points, mandatory/bonus дії та версію правил.",
    "testnet_participation": "Вести журнал транзакцій, feedback і знайдених помилок; тестнет сам по собі не гарантує токени.",
    "node_validator_work": "Контролювати uptime, версію клієнта, епохи, ключі та фактичну вартість сервера.",
    "nft_or_asset_holding": "Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння.",
    "community_contribution": "Оцінювати якість і підтверджуваність внеску; масовий spam підвищує Sybil-ризик.",
    "developer_contribution": "Зберігати PR, commit, deployment і прийнятий результат, а не лише факт активності.",
    "referrals": "Вважати referral додатковим множником, якщо правила не визначають його обов’язковим.",
    "anti_sybil_identity": "Не автоматизувати дублікати особистостей; перевіряти правила адрес, кластерів, KYC і географії.",
    "claim_and_vesting": "Стежити за початком/кінцем claim, vesting, unlock і поверненням невитребуваних токенів.",
    "ranking_or_tier": "Зберігати формулу score, межі tier і capped/uncapped частини; не припускати лінійну конвертацію.",
}


def identity_key(value):
    key = re.sub(r"[^a-z0-9]", "", value.casefold())
    return ALIASES.get(key, key)


def unique_clean(values):
    ignored = {
        "not known", "information", "details", "criteria", "loading content...",
        "official announcement", "official documentation", "eligibility criteria",
    }
    output = []
    for value in values:
        value = re.sub(r"\s+", " ", value).strip(" :")
        if not value or value.casefold() in ignored or len(value) < 3:
            continue
        if value not in output:
            output.append(value)
    return output


def value_after(lines, label):
    try:
        value = lines[lines.index(label) + 1].strip()
    except (ValueError, IndexError):
        return None
    return None if value.casefold() == "not known" else value


def section(lines, start, end_labels):
    try:
        begin = lines.index(start) + 1
    except ValueError:
        return []
    end = len(lines)
    for label in end_labels:
        try:
            end = min(end, lines.index(label, begin))
        except ValueError:
            pass
    return unique_clean(lines[begin:end])


def timeline_from(lines):
    values = section(lines, "Timeline", ["Token Distribution", "Eligibility Criteria", "Important Links"])
    result = []
    date_like = re.compile(r"(?:\d{4}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Not Known)", re.I)
    index = 0
    while index + 1 < len(values):
        if date_like.search(values[index + 1]):
            result.append({"event": values[index], "date": values[index + 1]})
            index += 2
        else:
            index += 1
    return result[:8]


def factor_tags(text):
    lower = text.casefold()
    return [name for name, words in FACTOR_RULES.items() if any(word in lower for word in words)]


def lesson_for(tags):
    ordered = sorted(tags, key=lambda tag: list(FACTOR_RULES).index(tag))
    selected = ordered[:3]
    if not selected:
        return "Розділяти категорії учасників і не перетворювати перелік історичних умов на обіцянку винагороди."
    return " ".join(FACTOR_GUIDANCE[tag] for tag in selected)


def parse_archive(row):
    saved = json.loads((ROOT / row["source_file"]).read_text(encoding="utf-8"))
    text = saved.get("text", "")
    assert hashlib.sha256(text.encode()).hexdigest() == row["source_text_sha256"]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    criteria = section(lines, "Eligibility Criteria", ["Important Links", "Additional Information", "Disclaimer"])
    description = value_after(lines, "Website") or "Опис продукту у джерелі не структуровано."
    allocation = value_after(lines, "Total Airdrop Amount")
    eligible = value_after(lines, "Number of Eligible Users")
    claimants = value_after(lines, "Number of Claimants")
    timeline = timeline_from(lines)
    links = [
        url for url in saved.get("external_links", [])
        if not any(host in url for host in (
            "coinmarketcap.com", "coingecko.com", "creativecommons.org",
            "github.com/i-shivamsoni", "airdroparchive.com",
        ))
    ]
    sources = [{
        "title": "Crypto Airdrop Archive", "url": row["source_url"],
        "kind": "secondary_directory", "access": "saved_copy",
    }]
    sources.extend({
        "title": "Посилання з каталогу — потребує перевірки", "url": url,
        "kind": "outbound_link_pending_review", "access": "not_rechecked",
    } for url in links[:6])
    combined = " ".join([description, *criteria])
    factors = factor_tags(combined)
    claim_start = next((item["date"] for item in timeline if "claiming started" in item["event"].casefold()), None)
    payout_status = "claim_start_reported_by_secondary_source" if claim_start else "reward_event_reported_by_secondary_source"
    if claimants:
        payout_status = "claimants_reported_by_secondary_source"
    unknowns = ["Запуск, правила та перекази не звірені з усіма першоджерелами."]
    if not claimants:
        unknowns.append("Кількість фактичних одержувачів невідома.")
    if not allocation:
        unknowns.append("Повний обсяг роздачі невідомий.")
    return {
        "project": row["name"],
        "identity_key": identity_key(row["name"]),
        "event_date": row["catalog_date"],
        "event_year": int(row["catalog_date"][:4]),
        "event_date_precision": "secondary_directory_catalog_date",
        "description": description,
        "rewarded_actions": criteria[:16] or ["У каталозі немає структурованого переліку критеріїв."],
        "allocation_reported": allocation,
        "eligible_reported": eligible,
        "claimants_reported": claimants,
        "timeline": timeline,
        "product_status": "reported_alive_by_secondary_directory",
        "payout_status": payout_status,
        "payout_summary": None,
        "evidence_tier": "secondary_directory_screened",
        "sources": sources,
        "factors": factors,
        "agent_lesson": lesson_for(factors),
        "unknowns": unknowns,
        "fine_tuning_eligible": False,
        "source_text_sha256": row["source_text_sha256"],
    }


def parse_curated(case, archive=None):
    sources = [{
        "title": f"Джерело {index}", "url": source["url"],
        "kind": source.get("kind", "source"), "access": source.get("access", "recorded"),
    } for index, source in enumerate(case.get("sources", []), 1)]
    criteria = [part.strip() for part in re.split(r"(?<=[.;])\s+", case.get("rules_summary", "")) if part.strip()]
    description = "Поіменне історичне досьє з матеріалами про умови та подію винагороди."
    allocation = str(case["reported_amount"]) if case.get("reported_amount") is not None else None
    eligible = None
    claimants = str(case["reported_recipients"]) if case.get("reported_recipients") is not None else None
    timeline = []
    event_date = case.get("event_date")
    precision = "exact_date" if event_date else "year"
    if archive:
        description = archive["description"]
        if len(archive["rewarded_actions"]) > len(criteria):
            criteria = archive["rewarded_actions"]
        allocation = allocation or archive["allocation_reported"]
        eligible = archive["eligible_reported"]
        claimants = claimants or archive["claimants_reported"]
        timeline = archive["timeline"]
        if not event_date:
            event_date = archive["event_date"]
            precision = archive["event_date_precision"]
        existing = {item["url"] for item in sources}
        sources.extend(item for item in archive["sources"] if item["url"] not in existing)
    combined = " ".join([case.get("rules_summary", ""), *criteria])
    # Legacy dossier tags use a different, very granular vocabulary. Reclassify
    # the source text into the shared factor taxonomy instead of mixing schemas.
    factors = factor_tags(combined)
    primary = any(
        source["kind"] in {"issuer", "issuer_or_governance"}
        and source["access"] in {"fetched", "direct_text_fetched", "web_read"}
        for source in sources
    )
    return {
        "project": case["project"],
        "identity_key": identity_key(case["project"]),
        "event_date": event_date,
        "event_year": case.get("reward_year"),
        "event_date_precision": precision,
        "description": description,
        "rewarded_actions": criteria[:16] or [case.get("rules_summary", "Умови потребують структурування.")],
        "allocation_reported": allocation,
        "eligible_reported": eligible,
        "claimants_reported": claimants,
        "timeline": timeline,
        "product_status": "source_checked_historical_product",
        "payout_status": case.get("payout_evidence_level", "source_checked_partial"),
        "payout_summary": case.get("payout_summary"),
        "evidence_tier": "primary_source_checked_partial" if primary else "curated_mixed_sources",
        "sources": sources,
        "factors": factors,
        "agent_lesson": case.get("agent_lesson") or lesson_for(factors),
        "unknowns": case.get("unknowns") or ["Повний аудит переказів не виконано."],
        "fine_tuning_eligible": False,
    }


def archive_score(item):
    return (
        4 * bool(item["allocation_reported"])
        + 3 * bool(item["eligible_reported"])
        + 3 * bool(item["claimants_reported"])
        + min(4, len(item["rewarded_actions"]) // 2)
        + 2 * (len(item["sources"]) > 1)
        + 2 * any("claiming started" in event["event"].casefold() for event in item["timeline"])
    )


def curated_in_scope(case, archive_by_key):
    event_date = case.get("event_date")
    if event_date:
        return WINDOW_FROM <= event_date <= WINDOW_TO
    if identity_key(case["project"]) in archive_by_key:
        return True
    return case.get("reward_year") == 2025


def build_factor_analysis(projects):
    factor_counts = Counter(factor for item in projects for factor in item["factors"])
    primary_counts = Counter(
        factor for item in projects
        if item["evidence_tier"] != "secondary_directory_screened"
        for factor in item["factors"]
    )
    rows = []
    for factor, count in factor_counts.most_common():
        rows.append({
            "factor": factor,
            "projects": count,
            "share_of_150": round(count / TARGET, 4),
            "source_checked_projects": primary_counts[factor],
            "secondary_screened_projects": count - primary_counts[factor],
            "interpretation": "Згадано в описі умов або критеріїв; частота не доводить причинний вплив на розмір виплати.",
            "strategy": FACTOR_GUIDANCE.get(factor, "Перевірити актуальні офіційні правила перед дією."),
        })
    return rows


def build_relationship_analysis(projects):
    """Rank factor co-occurrence; lift is descriptive, not causal."""
    counts = Counter(factor for item in projects for factor in set(item["factors"]))
    together = Counter()
    for item in projects:
        for left, right in combinations(sorted(set(item["factors"])), 2):
            together[(left, right)] += 1
    rows = []
    for (left, right), both in together.items():
        if both < 8:
            continue
        expected = counts[left] * counts[right] / TARGET
        lift = both / expected if expected else 0
        rows.append({
            "left": left,
            "right": right,
            "projects_together": both,
            "support": round(both / TARGET, 4),
            "lift": round(lift, 3),
            "conditional_left_given_right": round(both / counts[right], 4),
            "conditional_right_given_left": round(both / counts[left], 4),
            "interpretation": "Спільна поява в умовах; це не причинний вплив на payout.",
        })
    return sorted(rows, key=lambda row: (-row["lift"], -row["projects_together"], row["left"], row["right"]))[:15]


def apply_official_source_audit(projects):
    path = ROOT / "recent-official-source-audit.json"
    if not path.exists():
        return Counter()
    audit = json.loads(path.read_text(encoding="utf-8"))
    by_url = {item["url"]: item for item in audit}
    counts = Counter()
    for project in projects:
        statuses = []
        for source in project["sources"]:
            checked = by_url.get(source["url"])
            if not checked:
                continue
            source["access"] = checked["status"]
            source["content_file"] = checked.get("content_file")
            source["retrieved_at"] = checked.get("retrieved_at")
            statuses.append(checked["status"])
            counts[checked["status"]] += 1
        project["official_source_followup"] = statuses[0] if statuses else "not_attempted"
    return counts


def markdown_report(projects, evidence, factors, relationships, official_audit):
    lines = [
        "# Історичні роздачі: 150 проєктів за останні 2 роки", "",
        f"**Період подій:** {WINDOW_FROM}–{WINDOW_TO}. **Дата зрізу:** 03.10.2026.", "",
        "Рівно 150 унікальних емітентів; повторні сезони об’єднано. Поіменні досьє з прочитаними джерелами відділені від структурованого скринінгу вторинної директорії. Алокація, eligible, claimants і фактичні перекази — різні показники.", "",
        "## Покриття та межі доказів", "",
        f"- Першоджерела прочитано, досьє часткове: **{evidence['primary_source_checked_partial']}**.",
        f"- Змішані поіменні джерела: **{evidence['curated_mixed_sources']}**.",
        f"- Вторинна директорія, потрібна первинна перевірка: **{evidence['secondary_directory_screened']}**.",
        f"- Додатково завантажено офіційні сторінки з релевантними термінами: **{official_audit.get('fetched_relevant', 0)}**; вони ще очікують ручної перевірки тверджень.",
        "- Повністю відтворений аудит усіх переказів: **0**.",
        "- Fine-tuning дозволено: **0**; записи спершу мають пройти незалежну перевірку.", "",
        "## Взаємозв’язки та фактори", "",
        "Таблиця показує, як часто фактор прямо згаданий у зібраних умовах. Це описова частота, а не оцінка ймовірності нагороди й не доказ, що дія спричинила виплату.", "",
        "| Фактор | Проєктів | Частка | З перевірених досьє | Як застосувати |", "|---|---:|---:|---:|---|",
    ]
    for row in factors:
        lines.append(f"| `{row['factor']}` | {row['projects']} | {row['share_of_150']:.1%} | {row['source_checked_projects']} | {row['strategy']} |")
    lines += ["", "### Поєднання факторів", "",
        "Lift понад 1 означає, що пара зустрічалася разом частіше, ніж очікувалося з її окремих частот. Це допомагає будувати чекліст, але не доводить причинності або розміру винагороди.", "",
        "| Фактор A | Фактор B | Разом | Частка | Lift |", "|---|---|---:|---:|---:|"]
    for row in relationships:
        lines.append(f"| `{row['left']}` | `{row['right']}` | {row['projects_together']} | {row['support']:.1%} | {row['lift']:.2f} |")
    lines += ["", "## Стратегія відпрацювання", "",
        "1. Спочатку оцінити довіру: офіційний домен, команда, фінансування, стан mainnet/продукту, правила та ризики.",
        "2. Визначити основну корисну дію продукту. Взаємодія має бути реальною, повторюваною лише там, де правила враховують тривалість або епохи.",
        "3. Зберігати докази: дата, wallet, network, tx hash, route, amount, fee, balance before/after, quest/season і URL версії правил.",
        "4. Покривати додаткові фактори лише після основної дії: різноманітність функцій, governance, feedback, контент, referral або NFT.",
        "5. Встановити бюджет на gas, fees, capital lock і сервер. Зупиняти стратегію, якщо очікувана невизначена винагорода не виправдовує ризик.",
        "6. Не створювати Sybil-кластери, wash-volume, spam або фіктивні referrals. Такі дії часто ведуть до виключення.",
        "7. Після snapshot продовжувати відстеження: eligibility checker, claim, vesting, unlock, deadline і зміни правил.", "",
        "## 150 досьє", "",
    ]
    for index, item in enumerate(projects, 1):
        lines += [f"### {index}. {item['project']}", "",
            f"**Дата:** {item.get('event_date') or item.get('event_year') or 'невідомо'} ({item['event_date_precision']}). **Докази:** `{item['evidence_tier']}`.",
            f"**Проєкт:** {item['description']}",
            f"**Статуси:** {item['product_status']}; {item['payout_status']}.", "",
            "**Умови/дії:**", ""]
        lines.extend(f"- {value}" for value in item["rewarded_actions"])
        lines += ["", f"**Фактори:** {', '.join(item['factors']) or 'не класифіковано'}.",
            f"**Обсяг:** {item.get('allocation_reported') or 'невідомо'}. **Eligible:** {item.get('eligible_reported') or 'невідомо'}. **Claimants:** {item.get('claimants_reported') or 'невідомо'}.",
            f"**Урок:** {item['agent_lesson']}", "",
            "**Прогалини:** " + " ".join(item["unknowns"]), "",
            "**Джерела:** " + " · ".join(f"[{source['title']}]({source['url']})" for source in item["sources"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def html_report(projects, evidence, factors, relationships, official_audit):
    esc = html.escape
    labels = {
        "primary_source_checked_partial": "Першоджерела прочитано",
        "curated_mixed_sources": "Змішані джерела",
        "secondary_directory_screened": "Вторинний скринінг",
    }
    factor_rows = "".join(
        f"<tr><td><code>{esc(row['factor'])}</code></td><td>{row['projects']}</td><td>{row['share_of_150']:.1%}</td><td>{row['source_checked_projects']}</td><td>{esc(row['strategy'])}</td></tr>"
        for row in factors
    )
    relationship_rows = "".join(
        f"<tr><td><code>{esc(row['left'])}</code></td><td><code>{esc(row['right'])}</code></td><td>{row['projects_together']}</td><td>{row['support']:.1%}</td><td>{row['lift']:.2f}</td></tr>"
        for row in relationships
    )
    cards = []
    for index, item in enumerate(projects, 1):
        links = " · ".join(f'<a href="{esc(source["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{esc(source["title"])}</a>' for source in item["sources"])
        actions = "".join(f"<li>{esc(value)}</li>" for value in item["rewarded_actions"])
        tags = "".join(f"<span>{esc(tag)}</span>" for tag in item["factors"])
        timeline = "".join(f"<li><b>{esc(value['event'])}:</b> {esc(value['date'])}</li>" for value in item["timeline"])
        search = " ".join([item["project"], item["description"], *item["rewarded_actions"], *item["factors"]]).casefold()
        result = item.get("payout_summary") or f"Заявлений обсяг: {item.get('allocation_reported') or 'невідомо'}; eligible: {item.get('eligible_reported') or 'невідомо'}; claimants: {item.get('claimants_reported') or 'невідомо'}."
        tone = "secondary" if item["evidence_tier"] == "secondary_directory_screened" else "primary"
        cards.append(
            f'<article data-search="{esc(search, quote=True)}" data-level="{item["evidence_tier"]}"><div class="head"><span class="num">{index:03d}</span><div><h2>{esc(item["project"])}</h2><p>{esc(str(item.get("event_date") or item.get("event_year") or "дата невідома"))} · {esc(item["event_date_precision"])}</p></div></div>'
            f'<span class="badge {tone}">{esc(labels[item["evidence_tier"]])}</span><p class="muted">{esc(item["description"])}</p><div class="tags">{tags}</div><h3>Умови та дії</h3><ul>{actions}</ul><h3>Результат</h3><p>{esc(result)}</p><p><b>Продукт:</b> {esc(item["product_status"])}<br><b>Винагорода:</b> {esc(item["payout_status"])}</p>'
            + (f"<h3>Часова шкала</h3><ul>{timeline}</ul>" if timeline else "")
            + f'<div class="lesson"><b>Урок для агента</b><p>{esc(item["agent_lesson"])}</p></div><details><summary>Прогалини та джерела</summary><p>{esc(" ".join(item["unknowns"]))}</p><p>{links}</p></details></article>'
        )
    options = "".join(f'<option value="{key}">{esc(value)}</option>' for key, value in labels.items())
    return f'''<!doctype html><html lang="uk"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>150 історичних роздач — AI Hunter</title><style>
:root{{--ink:#172033;--muted:#64748b;--line:#d8e0eb;--bg:#f5f7fb;--card:#fff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,Segoe UI,system-ui,sans-serif}}main{{max-width:1240px;margin:auto;padding:40px 24px 80px}}header{{padding:36px;border-radius:24px;background:linear-gradient(135deg,#101a3b,#193d73 65%,#0e7490);color:#fff;box-shadow:0 20px 60px #1e3a8a22}}header h1{{font-size:clamp(34px,6vw,66px);line-height:1.02;margin:12px 0}}header p{{max-width:900px}}.eyebrow{{text-transform:uppercase;letter-spacing:.16em;font-size:12px;font-weight:700;color:#a5f3fc}}.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:24px 0}}.metric,.panel,article{{background:var(--card);border:1px solid var(--line);border-radius:18px}}.metric{{padding:20px}}.metric b{{display:block;font-size:32px}}.notice{{border-left:4px solid #f59e0b;background:#fffbeb;padding:15px 18px;border-radius:8px}}.panel{{padding:22px;margin:18px 0;overflow:auto}}table{{border-collapse:collapse;width:100%}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}.filters{{position:sticky;top:0;z-index:2;background:#f5f7fbee;backdrop-filter:blur(12px);padding:16px 0;display:flex;gap:12px}}input,select{{font:inherit;border:1px solid #94a3b8;border-radius:10px;padding:12px;background:#fff}}input{{flex:1;min-width:220px}}article{{padding:24px;margin:16px 0;box-shadow:0 8px 24px #0f172a08}}.head{{display:flex;gap:16px;align-items:start}}.num{{font:700 14px ui-monospace;color:#3157d5;background:#eef2ff;border-radius:8px;padding:6px 8px}}h2{{margin:0;font-size:28px}}h3{{font-size:14px;text-transform:uppercase;letter-spacing:.07em;margin-top:22px}}.muted,.head p{{color:var(--muted)}}.badge{{display:inline-block;border-radius:999px;padding:5px 11px;font-size:13px;font-weight:650}}.badge.primary{{background:#dcfce7;color:#166534}}.badge.secondary{{background:#fff7ed;color:#9a3412}}.tags{{display:flex;gap:7px;flex-wrap:wrap}}.tags span{{background:#edf5ff;color:#1e4a78;border-radius:6px;padding:3px 8px;font-size:12px}}.lesson{{background:#f0fdfa;border-left:4px solid #14b8a6;padding:14px 16px;border-radius:8px}}details{{border-top:1px solid var(--line);margin-top:18px;padding-top:14px}}summary{{cursor:pointer;font-weight:700}}a{{color:#174da3}}article[hidden]{{display:none}}@media(max-width:800px){{.metrics{{grid-template-columns:1fr 1fr}}.filters{{position:static;display:grid}}}}@media print{{.filters{{display:none}}body{{background:white}}article{{break-inside:avoid;box-shadow:none}}}}
</style><main><header><div class="eyebrow">AI Hunter · зріз 03.10.2026</div><h1>150 історичних роздач<br>за останні 2 роки</h1><p>Умови, результати, фактори винагородження й уроки для агентів. Період: {WINDOW_FROM}–{WINDOW_TO}. Один емітент рахується один раз.</p></header><div class="metrics"><div class="metric"><b>150</b>унікальних проєктів</div><div class="metric"><b>{evidence['primary_source_checked_partial']}</b>першоджерела прочитано</div><div class="metric"><b>{official_audit.get('fetched_relevant',0)}</b>релевантних офіційних сторінок у черзі</div><div class="metric"><b>{evidence['secondary_directory_screened']}</b>вторинний скринінг</div></div><p class="notice"><b>Межа висновків.</b> Частота фактора показує, як часто він згаданий в умовах, але не доводить причинність і не гарантує винагороду. Алокація, eligible, claimant та підтверджена виплата — різні стани.</p><section class="panel"><h2>Фактори, що впливали на eligibility або розмір</h2><table><thead><tr><th>Фактор</th><th>Проєктів</th><th>Частка</th><th>Перевірені досьє</th><th>Практична дія</th></tr></thead><tbody>{factor_rows}</tbody></table></section><section class="panel"><h2>Взаємозв’язки факторів</h2><p>Lift показує спільну появу в умовах, а не причинний вплив на payout.</p><table><thead><tr><th>Фактор A</th><th>Фактор B</th><th>Разом</th><th>Частка</th><th>Lift</th></tr></thead><tbody>{relationship_rows}</tbody></table></section><section class="panel"><h2>Базова стратегія</h2><ol><li>Перевірити офіційний домен, продукт/mainnet, правила й ризики.</li><li>Виконувати реальну основну функцію продукту; тривалість і регулярність додавати лише за наявності відповідної механіки.</li><li>Зберігати дату, wallet, network, tx hash, amount, fee, balance, quest/season і URL правил.</li><li>Після основної дії перевіряти modifiers: diversity, governance, feedback, content, referrals, NFT, tiers.</li><li>Мати межу витрат і не створювати Sybil-кластери, wash-volume чи spam.</li><li>Вести snapshot, checker, claim, vesting, unlock і deadline.</li></ol></section><div class="filters"><input id="q" aria-label="Пошук" placeholder="Назва, staking, testnet, NFT, фактор…"><select id="level" aria-label="Рівень доказів"><option value="">Усі рівні доказів</option>{options}</select></div><p id="count" aria-live="polite"></p>{''.join(cards)}<script>const q=document.querySelector('#q'),level=document.querySelector('#level'),cards=[...document.querySelectorAll('article')];function filter(){{const text=q.value.toLocaleLowerCase().trim();let n=0;for(const card of cards){{const visible=card.dataset.search.includes(text)&&(!level.value||card.dataset.level===level.value);card.hidden=!visible;if(visible)n++}}document.querySelector('#count').textContent=`Показано ${{n}} із ${{cards.length}} досьє`;}}q.addEventListener('input',filter);level.addEventListener('change',filter);filter();</script></main></html>'''


def build():
    previous = json.loads((ROOT / "historical-rewards.json").read_text(encoding="utf-8"))
    screening = json.loads((ROOT / "archive-screening.json").read_text(encoding="utf-8"))
    archive = [
        parse_archive(row) for row in screening["rows"]
        if row.get("catalog_date") and WINDOW_FROM <= row["catalog_date"] <= WINDOW_TO
        and row.get("catalog_status") == "Alive"
    ]
    archive_by_key = {}
    for item in sorted(archive, key=lambda value: (archive_score(value), value["event_date"]), reverse=True):
        archive_by_key.setdefault(item["identity_key"], item)

    projects = []
    seen = set()
    for case in previous["projects"]:
        if not curated_in_scope(case, archive_by_key):
            continue
        key = identity_key(case["project"])
        if key in seen:
            continue
        projects.append(parse_curated(case, archive_by_key.get(key)))
        seen.add(key)

    remaining = sorted(
        (item for key, item in archive_by_key.items() if key not in seen),
        key=lambda value: (-archive_score(value), value["event_date"], value["project"].casefold()),
    )
    for item in remaining:
        if len(projects) == TARGET:
            break
        projects.append(item)
        seen.add(item["identity_key"])
    if len(projects) != TARGET:
        raise RuntimeError(f"Expected {TARGET} projects, got {len(projects)}")
    projects.sort(key=lambda value: (value.get("event_date") or f"{value.get('event_year', 0)}-12-31", value["project"].casefold()), reverse=True)
    official_audit = apply_official_source_audit(projects)

    evidence = Counter(item["evidence_tier"] for item in projects)
    for key in ("primary_source_checked_partial", "curated_mixed_sources", "secondary_directory_screened"):
        evidence.setdefault(key, 0)
    factors = build_factor_analysis(projects)
    relationships = build_relationship_analysis(projects)
    dataset = {
        "window": {"from": WINDOW_FROM, "to": WINDOW_TO, "date_applies_to": "reward_or_claim_event"},
        "as_of": "2026-10-03", "target_unique_projects": TARGET,
        "methodology": "One issuer is counted once. Source-checked dossiers take precedence; high-information secondary screens fill the remaining sample with their lower evidence tier explicit.",
        "limitations": [
            "Secondary-directory dates and claims are not primary-source or onchain verification.",
            "Factor frequency is descriptive and does not establish causal effect on payout.",
            "No historical pattern guarantees a future reward.",
        ],
        "projects": projects,
    }
    write_utf8(ROOT / "recent-150-projects.json", json.dumps(dataset, ensure_ascii=False, indent=2))
    columns = ["project", "event_date", "event_year", "event_date_precision", "description", "rewarded_actions", "allocation_reported", "eligible_reported", "claimants_reported", "product_status", "payout_status", "evidence_tier", "factors", "agent_lesson", "unknowns", "sources"]
    with (ROOT / "recent-150-projects.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for item in projects:
            writer.writerow({key: json.dumps(item.get(key), ensure_ascii=False) if isinstance(item.get(key), (list, dict)) else item.get(key) for key in columns})

    strategy = {
        "as_of": "2026-10-03", "sample_size": TARGET,
        "evidence_tier_counts": dict(evidence), "official_source_audit": dict(official_audit), "factor_analysis": factors,
        "relationship_analysis": relationships,
        "agent_rules": [
            "Never promise or imply a guaranteed reward.",
            "Keep launch, TGE, snapshot, claim start, claim end and payout as separate events.",
            "Extract eligibility cohorts separately and preserve AND/OR logic, thresholds and units.",
            "Separate allocation, eligible wallets, claimants and verified transfers.",
            "Record fees, locked capital, infrastructure cost and asset-price exposure.",
            "Use historical cases as questions to investigate, never as current-project evidence.",
            "Do not train on secondary-only records until independent review is complete.",
        ],
    }
    write_utf8(ROOT / "recent-150-strategy.json", json.dumps(strategy, ensure_ascii=False, indent=2))
    markdown = markdown_report(projects, evidence, factors, relationships, official_audit)
    page = html_report(projects, evidence, factors, relationships, official_audit)
    write_utf8(ROOT / "REPORT.uk.md", markdown)
    write_utf8(ROOT / "REPORT.html", page)

    validation = {
        "status": "passed", "projects": len(projects),
        "unique_projects": len({item["identity_key"] for item in projects}),
        "window": [WINDOW_FROM, WINDOW_TO], "evidence_tiers": dict(evidence),
        "official_source_audit": dict(official_audit),
        "projects_with_sources": sum(bool(item["sources"]) for item in projects),
        "projects_with_actions": sum(bool(item["rewarded_actions"]) for item in projects),
        "fine_tuning_eligible": sum(bool(item["fine_tuning_eligible"]) for item in projects),
        "html_cards": page.count("<article "), "factors": len(factors),
        "factor_relationships": len(relationships),
    }
    assert validation["projects"] == validation["unique_projects"] == TARGET
    assert validation["projects_with_sources"] == validation["projects_with_actions"] == TARGET
    assert validation["fine_tuning_eligible"] == 0
    assert validation["html_cards"] == TARGET
    write_utf8(ROOT / "recent-150-validation.json", json.dumps(validation, ensure_ascii=False, indent=2))
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    build()

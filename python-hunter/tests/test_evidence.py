import asyncio
from datetime import datetime,timezone
import pytest
from core.source_policy import telegram_window,canonical_url,telegram_url
from discovery.evidence import catalog, material, telegram_messages, read_html, SourceUnavailable
from ai_analyzer.grounded import validate_analysis

def test_calendar_month_and_initial_history_gap():
    now=datetime(2026,3,31,tzinfo=timezone.utc)
    start,_=telegram_window(now)
    assert start.day==28 and start.month==2
    html='<div class="tgme_widget_message" data-post="testchannel/1"><time datetime="2026-03-30T12:00:00Z"></time><div class="tgme_widget_message_text">New task</div></div>'
    result=telegram_messages(html,now)
    assert len(result["messages"])==1 and not result["history_complete"]
    assert result["messages"][0]["url"]=="https://t.me/testchannel/1"
    assert not telegram_messages(html,datetime(2026,5,31,tzinfo=timezone.utc))["messages"]

def test_no_fake_candidates_on_empty_or_navigation():
    assert catalog("<h1>No projects</h1>","https://cryptorank.io/ru/drophunting","cryptorank")==[]
    html='<a href="/ru/drophunting/example-activity1">Example</a><a href="https://evil.example/ru/drophunting/fake-activity1">Fake</a>'
    assert len(catalog(html,"https://cryptorank.io/ru/drophunting","cryptorank"))==1

def test_untrusted_model_evidence_and_urls_are_rejected():
    text="Read the official documentation before joining this campaign."
    data={"tasks":[{"title":"Good","quote":text,"url":"https://example.com"},
                   {"title":"Fake","quote":"The reward is guaranteed today","url":"https://evil.com"},
                   {"title":"Bad link","quote":text,"url":"javascript:alert(1)"}]}
    result=validate_analysis(data,text,"https://example.com",[])
    assert [t["title"] for t in result["tasks"]]==["Good"]
    assert result["tasks"][0]["requires_user_review"]
    assert validate_analysis({},text,"https://example.com",[])["tasks"]==[]

def test_material_keeps_links_and_removes_scripts():
    html="<article><h1>Guide</h1><script>stolen()</script><p>"+("Useful instructions. "*10)+"</p><a href='/join'>Join</a></article>"
    body=material(html,"https://example.com/guide")
    assert "stolen" not in body["text"]
    assert body["links"][0]["url"]=="https://example.com/join"

def test_policy_rejects_credentials_local_and_invites():
    for value in ("http://example.com","https://user:pass@example.com","https://localhost"):
        with pytest.raises(ValueError): canonical_url(value)
    with pytest.raises(ValueError): telegram_url("https://t.me/+privateInvite")
    with pytest.raises(ValueError): telegram_url("https://t.me/channel/123")

def test_reader_rejects_unapproved_redirect_target_before_network():
    with pytest.raises(SourceUnavailable):
        asyncio.run(read_html("https://evil.example/path",{"cryptorank.io"}))


def test_dropstab_excludes_regular_market_coins():
    html='<a href="/coins/bitcoin">BTC</a><a href="/coins/real/activities"><span class="font-semibold text-sm">Real</span> Active</a>'
    values=catalog(html,"https://dropstab.com/activities","dropstab")
    assert len(values)==1 and values[0]["title"]=="Real"

def test_incrypted_active_rows_use_single_id():
    html='<tr data-single-id="42"><td class="status-active"><span class="airdrop-item-title">Example</span></td></tr>'
    assert catalog(html,"https://incrypted.com/airdrops/","incrypted")==[{"title":"Example","url":"https://incrypted.com/airdrops/?single=42"}]

def test_airdropalert_imports_only_active_campaign_cards():
    html="""<nav><a href="/airdrops/">Airdrops</a></nav>
    <div class="card-anchor active-label" data-href="https://airdropalert.com/airdrops/example-airdrop/"><h4 class="title">Example</h4></div>
    <div class="card-anchor ended-label" data-href="https://airdropalert.com/airdrops/ended/"><h4 class="title">Ended</h4></div>
    <div class="card-anchor active-label" data-href="https://unapproved.example/airdrops/other/"><h4 class="title">External</h4></div>
    <div class="card-anchor active-label" data-href="/blogs/news/"><h4 class="title">Article</h4></div>"""
    assert catalog(html,"https://airdropalert.com/farm/","airdropalert")==[
        {"title":"Example","url":"https://airdropalert.com/airdrops/example-airdrop/"}]

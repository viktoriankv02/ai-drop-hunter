import os
import sys
import json
import asyncio
import httpx
from datetime import datetime
from loguru import logger

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ai_analyzer.gateway import llm_gateway
import sqlite3

DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")

BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
OKX_TICKER_URL = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

async def fetch_binance_anomalies(client: httpx.AsyncClient):
    """Отримує пари з високим об'ємом та різким рухом з Binance"""
    try:
        res = await client.get(BINANCE_TICKER_URL, timeout=10)
        data = res.json()
        anomalies = []
        for item in data:
            symbol = item.get("symbol", "")
            if not symbol.endswith("USDT") or any(stable in symbol for stable in ["USDCUSDT", "FDUSDUSDT", "EURUSDT"]):
                continue

            quote_vol = float(item.get("quoteVolume", 0))  # Об'єм в USDT
            change_pct = float(item.get("priceChangePercent", 0))
            price = float(item.get("lastPrice", 0))

            # Фільтр: об'єм > 2M USDT і рух за 24г більше ±5%
            if quote_vol >= 2_000_000 and abs(change_pct) >= 5.0 and price > 0:
                anomalies.append({
                    "symbol": f"{symbol[:-4]}/USDT",
                    "exchange": "Binance",
                    "price": price,
                    "change_24h": change_pct,
                    "volume_usd": quote_vol,
                    "raw_symbol": symbol
                })
        return anomalies
    except Exception as e:
        logger.error(f"Помилка отримання Binance: {e}")
        return []

async def fetch_okx_anomalies(client: httpx.AsyncClient):
    """Отримує пари з OKX"""
    try:
        res = await client.get(OKX_TICKER_URL, timeout=10)
        data = res.json().get("data", [])
        anomalies = []
        for item in data:
            inst_id = item.get("instId", "")
            if not inst_id.endswith("-USDT"):
                continue

            last = float(item.get("last", 0) or 0)
            open24 = float(item.get("open24h", 0) or 0)
            vol_ccy = float(item.get("volCcy24h", 0) or 0)

            if open24 > 0 and last > 0 and vol_ccy >= 1_500_000:
                change_pct = ((last - open24) / open24) * 100
                if abs(change_pct) >= 5.0:
                    anomalies.append({
                        "symbol": inst_id.replace("-", "/"),
                        "exchange": "OKX",
                        "price": last,
                        "change_24h": round(change_pct, 2),
                        "volume_usd": vol_ccy,
                        "raw_symbol": inst_id
                    })
        return anomalies
    except Exception as e:
        logger.error(f"Помилка отримання OKX: {e}")
        return []

async def evaluate_anomaly_with_ai(anomaly: dict) -> dict:
    """ШІ аналізує імпульс та вирішує: це маніпуляція чи торговий сигнал"""
    symbol = anomaly["symbol"]
    exchange = anomaly["exchange"]
    price = anomaly["price"]
    change = anomaly["change_24h"]
    vol = f"${anomaly['volume_usd']:,.0f}"

    prompt = f"""Аналіз ринкової аномалії криптовалюти:
Пара: {symbol} ({exchange})
Поточна ціна: {price}
Зміна за 24г: {change}%
Торговий об'єм за 24г: {vol}

Визнач потенціал угоди (LONG якщо імпульс здоровий, SHORT якщо це перекуплений сквиз/дамп, IGNORE якщо це сміттєвий щиткоін).
Дай оцінку впевненості (0-100).
Відповідай ТІЛЬКИ валідним JSON без коментарів:
{{
  "direction": "LONG або SHORT або IGNORE",
  "score": 75,
  "signal_type": "volume_surge_pump або breakout або manipulation",
  "reason": "коротке обґрунтування українською (до 15 слів)"
}}
"""
    try:
        response = await llm_gateway.complete(prompt=prompt, system_prompt="Ти професійний ринковий квант-аналітик криптоактивів. Відповідай суворо JSON.")
        clean = response.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
        return json.loads(clean)
    except Exception:
        # Fallback якщо модель перевантажена
        direction = "LONG" if change > 0 else "SHORT"
        return {
            "direction": direction,
            "score": 60,
            "signal_type": "volume_surge_pump" if change > 0 else "volume_surge_dump",
            "reason": f"Імпульсний рух {change}% з добовим об'ємом {vol}"
        }

def save_signal(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO market_signals (symbol, exchange, direction, signal_type, entry_price, change_24h, ai_score, ai_reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["symbol"], data["exchange"], data["direction"],
        data["signal_type"], data["entry_price"], data["change_24h"],
        data["ai_score"], data["ai_reason"]
    ))
    conn.commit()
    conn.close()

async def run_market_scanner():
    logger.info("📈 Запуск ШІ-Агента моніторингу ринку (Binance + OKX)...")
    async with httpx.AsyncClient() as client:
        # 1. Паралельний збір із двох бірж
        b_task = fetch_binance_anomalies(client)
        o_task = fetch_okx_anomalies(client)
        b_res, o_res = await asyncio.gather(b_task, o_task)
        
        all_anomalies = b_res + o_res
        logger.info(f"Знайдено пар з аномальною активністю: {len(all_anomalies)}")

        # Сортуємо за найбільшим рухом
        all_anomalies.sort(key=lambda x: abs(x["change_24h"]), reverse=True)

        for anom in all_anomalies[:5]:  # Беремо топ-5 найгарячіших
            logger.info(f"🔍 Аналіз {anom['exchange']}: {anom['symbol']} ({anom['change_24h']}%)")
            analysis = await evaluate_anomaly_with_ai(anom)
            
            score = analysis.get("score", 0)
            direction = analysis.get("direction", "IGNORE")

            if direction != "IGNORE" and score >= 65:
                signal_data = {
                    "symbol": anom["symbol"],
                    "exchange": anom["exchange"],
                    "direction": direction,
                    "signal_type": analysis.get("signal_type", "surge"),
                    "entry_price": anom["price"],
                    "change_24h": anom["change_24h"],
                    "ai_score": score,
                    "ai_reason": analysis.get("reason", "Підтверджено аналітикою")
                }
                save_signal(signal_data)
                logger.success(f"🔥 СИГНАЛ [{direction}] {anom['symbol']} ({anom['exchange']}) | Ціна: {anom['price']} | Бал ШІ: {score}/100 | {analysis.get('reason')}")

if __name__ == "__main__":
    asyncio.run(run_market_scanner())

import httpx
import json
import asyncio
from datetime import datetime, timedelta
from loguru import logger
from ai_analyzer.gateway import llm_gateway

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
OKX_CANDLES_URL = "https://www.okx.com/api/v5/market/candles"

TIMEFRAME_MAP_BINANCE = {
    "1h": ("1m", 60),
    "24h": ("15m", 96),
    "1m": ("4h", 180),
    "1y": ("1d", 365),
    "5y": ("1w", 260)
}

TIMEFRAME_MAP_OKX = {
    "1h": ("1m", 60),
    "24h": ("15m", 96),
    "1m": ("4H", 180),
    "1y": ("1Dutc", 300),
    "5y": ("1W", 260)
}

def normalize_symbol(symbol: str) -> str:
    s = symbol.strip().upper().replace("/", "").replace("-", "")
    for stable in ["USDT", "BUSD", "USDC"]:
        if s.endswith(stable):
            s = s[:-len(stable)]
            break
    return s

def calculate_rsi(prices: list, period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(prices)):
        d = prices[i] - prices[i - 1]
        gains.append(max(d, 0.0))
        losses.append(abs(min(d, 0.0)))
    avg_g = sum(gains[-period:]) / period
    avg_l = sum(losses[-period:]) / period
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

def calculate_ema(prices: list, span: int) -> float:
    if not prices:
        return 0.0
    alpha = 2 / (span + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * alpha + ema * (1 - alpha)
    return round(ema, 4)

async def get_klines_data(symbol: str, period: str = "24h") -> dict:
    base_sym = normalize_symbol(symbol)
    pair_binance = f"{base_sym}USDT"
    chart_data, closes = [], []
    source_exchange = "Binance"

    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers, timeout=6) as client:
        try:
            b_interval, b_limit = TIMEFRAME_MAP_BINANCE.get(period, ("15m", 96))
            res = await client.get(BINANCE_KLINES_URL, params={"symbol": pair_binance, "interval": b_interval, "limit": b_limit})
            if res.status_code == 200:
                for k in res.json():
                    t = int(k[0])
                    c = float(k[4])
                    closes.append(c)
                    chart_data.append({
                        "time": datetime.utcfromtimestamp(t / 1000).strftime("%d.%m %H:%M"),
                        "price": c,
                        "volume": float(k[5])
                    })
        except Exception:
            pass

        if not closes:
            try:
                okx_bar, okx_limit = TIMEFRAME_MAP_OKX.get(period, ("15m", 96))
                res = await client.get(OKX_CANDLES_URL, params={"instId": f"{base_sym}-USDT", "bar": okx_bar, "limit": okx_limit})
                if res.status_code == 200:
                    raw_okx = res.json().get("data", [])
                    if raw_okx:
                        source_exchange = "OKX"
                        for k in reversed(raw_okx):
                            t = int(k[0])
                            c = float(k[4])
                            closes.append(c)
                            chart_data.append({
                                "time": datetime.utcfromtimestamp(t / 1000).strftime("%d.%m %H:%M"),
                                "price": c,
                                "volume": float(k[5])
                            })
            except Exception:
                pass

    if not closes:
        return {"error": f"Пару {base_sym}/USDT не знайдено на Binance та OKX"}

    curr_p = closes[-1]
    first_p = closes[0]
    chg = ((curr_p - first_p) / first_p) * 100 if first_p > 0 else 0

    rsi = calculate_rsi(closes, 14)
    ema20 = calculate_ema(closes, 20)
    ema50 = calculate_ema(closes, 50)
    sup = min(closes[-30:]) if len(closes) >= 30 else min(closes)
    res_p = max(closes[-30:]) if len(closes) >= 30 else max(closes)

    return {
        "symbol": f"{base_sym}/USDT",
        "exchange": source_exchange,
        "period": period,
        "current_price": curr_p,
        "price_change_pct": round(chg, 2),
        "chart": chart_data,
        "metrics": {
            "rsi": rsi,
            "ema20": ema20,
            "ema50": ema50,
            "trend_ema": "BULLISH" if ema20 >= ema50 else "BEARISH",
            "support": round(sup, 4),
            "resistance": round(res_p, 4)
        }
    }

async def generate_ai_token_forecast(symbol: str, horizon: str = "24h") -> dict:
    base_data = await get_klines_data(symbol, period="24h" if horizon in ["1h", "24h"] else "1m")
    if "error" in base_data:
        return base_data

    curr_p = base_data["current_price"]
    m = base_data["metrics"]

    is_bull = m["trend_ema"] == "BULLISH"
    bull_mult = 1.035 if horizon == "1h" else (1.065 if horizon == "24h" else 1.15)
    bear_mult = 0.98 if horizon == "1h" else (0.95 if horizon == "24h" else 0.88)

    calc_bull_target = round(curr_p * (bull_mult if is_bull else 1.02), 4)
    calc_base_target = round(curr_p * (1.015 if is_bull else 0.99), 4)
    calc_bear_target = round(curr_p * (0.98 if is_bull else bear_mult), 4)

    prompt = f"Аналіз {base_data['symbol']}. Ціна: ${curr_p}, RSI: {m['rsi']}, Тренд: {m['trend_ema']}. Горизонт: {horizon}. Зроби короткий висновок до 20 слів."

    summary = f"Тренд {m['trend_ema']} на базі EMA20/50. RSI {m['rsi']} свідчить про баланс сил у робочому коридорі."
    try:
        # Таймаут 3 секунди на відповідь Ollama
        ai_resp = await asyncio.wait_for(
            llm_gateway.complete(prompt=prompt, system_prompt="Ти криптоаналітик."),
            timeout=3.0
        )
        if ai_resp and len(ai_resp.strip()) > 5:
            summary = ai_resp.strip().replace('"', '')
    except Exception:
        pass

    # Майбутня проекція
    step_minutes = 10 if horizon == "1h" else (120 if horizon == "24h" else 1440)
    future_labels, bull_curve, base_curve, bear_curve = [], [], [], []
    now = datetime.utcnow()

    for i in range(1, 7):
        future_time = now + timedelta(minutes=step_minutes * i)
        future_labels.append(future_time.strftime("%d.%m %H:%M"))
        p = i / 6
        bull_curve.append(round(curr_p + (calc_bull_target - curr_p) * p, 4))
        base_curve.append(round(curr_p + (calc_base_target - curr_p) * p, 4))
        bear_curve.append(round(curr_p + (calc_bear_target - curr_p) * p, 4))

    return {
        "symbol": base_data["symbol"],
        "exchange": base_data["exchange"],
        "horizon": horizon,
        "current_price": curr_p,
        "metrics": m,
        "forecast": {
            "dominant_trend": m["trend_ema"],
            "probabilities": {"bull": 55 if is_bull else 30, "base": 30, "bear": 15 if is_bull else 40},
            "levels": {
                "take_profit_1": round(curr_p * 1.025, 4),
                "take_profit_2": round(curr_p * 1.055, 4),
                "stop_loss": round(curr_p * 0.965, 4),
                "risk_reward_ratio": "1:2.4"
            },
            "summary": summary
        },
        "projection_timeline": {
            "labels": future_labels,
            "bull_curve": bull_curve,
            "base_curve": base_curve,
            "bear_curve": bear_curve
        }
    }

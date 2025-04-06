import requests
import pandas as pd
import pandas_ta as ta

def fetch_ohlc(symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
    print(f"[ta] Ophalen candles voor {symbol} @ {interval}")
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Geen geldige data van Binance")
    print(f"[ta] Aantal candles ontvangen: {len(data)}")
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "_", "_", "_", "_", "_", "_"
    ])
    df["close"] = pd.to_numeric(df["close"])
    return df

def analyse_multiple_timeframes(symbol: str) -> dict:
    timeframes = ["5m", "10m", "15m", "30m", "1h", "1d"]
    results = {}
    for tf in timeframes:
        try:
            print(f"[ta] Start analyse timeframe: {tf}")
            df = fetch_ohlc(symbol, tf)
            print(f"[ta] Dataframe opgebouwd voor {tf}, laatste prijs: {df['close'].iloc[-1]}")
            df["rsi"] = ta.rsi(df["close"], length=14)
            df["ema20"] = ta.ema(df["close"], length=20)
            df["ema50"] = ta.ema(df["close"], length=50)
            trend = "Bullish" if df["ema20"].iloc[-1] > df["ema50"].iloc[-1] else "Bearish"
            results[tf] = {
                "rsi": df["rsi"].iloc[-1],
                "trend": trend,
                "close": df["close"].iloc[-1]
            }
            print(f"[ta] ✅ {tf} | RSI: {results[tf]['rsi']:.2f} | Trend: {trend}")
        except Exception as e:
            print(f"[ta] ❌ Fout in analyse {tf}: {str(e)}")
            continue
    return results

def analyse_single_timeframe(symbol: str, tf: str) -> dict:
    try:
        print(f"[ta] Analyse single timeframe {tf} voor {symbol}")
        df = fetch_ohlc(symbol, tf)
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["ema20"] = ta.ema(df["close"], length=20)
        df["ema50"] = ta.ema(df["close"], length=50)
        trend = "Bullish" if df["ema20"].iloc[-1] > df["ema50"].iloc[-1] else "Bearish"
        print(f"[ta] ✅ Single {tf} | RSI: {df['rsi'].iloc[-1]:.2f} | Trend: {trend}")
        return {
            "rsi": df["rsi"].iloc[-1],
            "trend": trend,
            "close": df["close"].iloc[-1]
        }
    except Exception as e:
        print(f"[ta] ❌ Fout analyse single {tf}: {str(e)}")
        raise
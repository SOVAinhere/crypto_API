from fastapi import FastAPI, HTTPException
from datetime import datetime
import requests
from database import engine, SessionLocal
from models import Base, Price

app = FastAPI()
Base.metadata.create_all(bind=engine)

COINS = {
    "BTC": "bitcoin",
    "XMR": "monero"
}


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/prices/latest")
def get_latest_price(symbol: str):
    symbol = symbol.upper()
    if symbol not in COINS:
        raise HTTPException(status_code=404, detail="Symbol not found")

    coin_id = COINS[symbol]

    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": coin_id,
            "vs_currencies": "usd",
        }
    )

    data = response.json()
    price_value = data[coin_id]["usd"]

    db = SessionLocal()

    price = Price(
        symbol=symbol,
        price=price_value,
        source="coingecko"
    )

    db.add(price)
    db.commit()
    db.close()

    return {
        "symbol": symbol,
        "price": price_value,
        "source": "coingecko",
        "timestamp": datetime.utcnow()
    }

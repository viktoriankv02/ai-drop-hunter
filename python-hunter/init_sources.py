import os
import json

SOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources")
SOURCES_FILE = os.path.join(SOURCES_DIR, "resources.json")
os.makedirs(SOURCES_DIR, exist_ok=True)

# Повний відновлений перелік 26 джерел
all_26_sources = [
  {"id": 1, "name": "CryptoRank Drophunting", "url": "https://cryptorank.io/drophunting", "type": "website", "enabled": True},
  {"id": 2, "name": "CryptoRank Funding Rounds", "url": "https://cryptorank.io/funding-rounds", "type": "website", "enabled": True},
  {"id": 3, "name": "Incrypted Airdrops", "url": "https://incrypted.com/airdrops/", "type": "website", "enabled": True},
  {"id": 4, "name": "Airdrops.io (Hot)", "url": "https://airdrops.io/hot/", "type": "website", "enabled": True},
  {"id": 5, "name": "Airdrops.io (Latest)", "url": "https://airdrops.io/", "type": "website", "enabled": True},
  {"id": 6, "name": "Airdrops.io (Speculative)", "url": "https://airdrops.io/speculative/", "type": "website", "enabled": True},
  {"id": 7, "name": "Dropstab Airdrops", "url": "https://dropstab.com/insights/airdrops", "type": "website", "enabled": True},
  {"id": 8, "name": "DappRadar Airdrops", "url": "https://dappradar.com/hub/airdrops", "type": "website", "enabled": True},
  {"id": 9, "name": "DefiLlama Airdrops", "url": "https://defillama.com/airdrops", "type": "website", "enabled": True},
  {"id": 10, "name": "AlphaDrops Portal", "url": "https://alphadrops.net/", "type": "website", "enabled": True},
  {"id": 11, "name": "Crypto Fortochka", "url": "https://t.me/s/cryptoforto", "type": "telegram", "enabled": True},
  {"id": 12, "name": "Incrypted Airdrops TG", "url": "https://t.me/s/incrypted_airdrops", "type": "telegram", "enabled": True},
  {"id": 13, "name": "DoubleTop Airdrops", "url": "https://t.me/s/doubletop", "type": "telegram", "enabled": True},
  {"id": 14, "name": "Crypto Davy", "url": "https://t.me/s/cryptodavy_ru", "type": "telegram", "enabled": True},
  {"id": 15, "name": "Bankless Drops Feed", "url": "https://t.me/s/bankless_drop", "type": "telegram", "enabled": True},
  {"id": 16, "name": "Hotties Drops", "url": "https://t.me/s/hottiesdrops", "type": "telegram", "enabled": True},
  {"id": 17, "name": "Cyber Airdrops", "url": "https://t.me/s/cyber_airdrops", "type": "telegram", "enabled": True},
  {"id": 18, "name": "Drops Daily Updates", "url": "https://t.me/s/drops_daily", "type": "telegram", "enabled": True},
  {"id": 19, "name": "Web3 Testnets Hub", "url": "https://t.me/s/web3_testnet", "type": "telegram", "enabled": True},
  {"id": 20, "name": "Node & Drop Channel", "url": "https://t.me/s/node_drop", "type": "telegram", "enabled": True},
  {"id": 21, "name": "0xAirdrops News", "url": "https://t.me/s/oxairdrops", "type": "telegram", "enabled": True},
  {"id": 22, "name": "Prophunt Drops", "url": "https://t.me/s/prophunt", "type": "telegram", "enabled": True},
  {"id": 23, "name": "Crypto Lambo Hunters", "url": "https://t.me/s/crypto_lambo_hunt", "type": "telegram", "enabled": True},
  {"id": 24, "name": "Galxe Quests Tracker", "url": "https://t.me/s/galxe_tracker", "type": "telegram", "enabled": True},
  {"id": 25, "name": "Layer3 Alpha Feed", "url": "https://t.me/s/layer3_alpha", "type": "telegram", "enabled": True},
  {"id": 26, "name": "RetroDrop Hunter Feed", "url": "https://t.me/s/retrodrop_hunter", "type": "telegram", "enabled": True}
]

with open(SOURCES_FILE, "w", encoding="utf-8") as f:
    json.dump(all_26_sources, f, ensure_ascii=False, indent=2)

print(f"✓ Успішно записано {len(all_26_sources)} джерел у sources/resources.json (чистий UTF-8)!")
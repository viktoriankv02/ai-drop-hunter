import os
import json
import asyncio
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# М'який імпорт web3
try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    logger.warning("⚠️ Бібліотеку web3 не знайдено. On-chain транзакції вимкнено (доступна лише browser-автоматизація).")

TESTNET_RPCS = {
    "ethereum_sepolia": "https://rpc.sepolia.org",
    "arbitrum_sepolia": "https://sepolia-rollup.arbitrum.io/rpc",
    "base_sepolia": "https://sepolia.base.org",
    "optimism_sepolia": "https://sepolia.optimism.io"
}

TEST_PRIVATE_KEY = os.getenv("TEST_PRIVATE_KEY", "")

class Web3Signer:
    def __init__(self):
        self.account = None
        if WEB3_AVAILABLE and TEST_PRIVATE_KEY and TEST_PRIVATE_KEY.startswith("0x") and len(TEST_PRIVATE_KEY) == 66:
            try:
                self.account = Account.from_key(TEST_PRIVATE_KEY)
                logger.info(f"🔑 [Web3Signer] Завантажено тестовий гаманець: {self.account.address}")
            except Exception as e:
                logger.error(f"Не вдалося ініціалізувати гаманець: {e}")
        else:
            if not TEST_PRIVATE_KEY:
                logger.info("ℹ️ [Web3Signer] TEST_PRIVATE_KEY не задано в .env (використовується публічна адреса за замовчуванням).")

    def get_web3_instance(self, network_name: str = "ethereum_sepolia"):
        if not WEB3_AVAILABLE:
            return None
        rpc_url = TESTNET_RPCS.get(network_name.lower(), TESTNET_RPCS["ethereum_sepolia"])
        return Web3(Web3.HTTPProvider(rpc_url))

    async def sign_message(self, message: str) -> str:
        if not self.account or not WEB3_AVAILABLE:
            return ""
        signed = self.account.sign_message(Account.encode_defunct(text=message))
        return signed.signature.hex()

web3_signer = Web3Signer()

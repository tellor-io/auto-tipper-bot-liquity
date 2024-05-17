import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# update these values
network = os.getenv("NETWORK") # ganache, goerli, mainnet, mumbai, polygon
query_id = os.getenv("QUERY_ID")
query_data = os.getenv("QUERY_DATA")
interval = int(os.getenv("INTERVAL")) # in seconds
redstone_is_frozen_timeout = int(os.getenv("REDSTONE_IS_FROZEN_TIMEOUT"))
redstone_max_price_deviation = float(os.getenv("REDSTONE_MAX_PRICE_DEVIATION_FROM_PREVIOUS_ROUND"))
redstone_datafeed_id = os.getenv("REDSTONE_DATAFEED_ID")
price_change_threshold = float(os.getenv("PRICE_CHANGE_THRESHOLD")) # collateral token price change threshold
collateral_token_price_url = os.getenv("COLLATERAL_TOKEN_PRICE_URL_COINGECKO")
if network == "mainnet":
    provider_url = os.getenv("PROVIDER_URL_MAINNET")
    oracle_address = "0x8cFc184c877154a8F9ffE0fe75649dbe5e2DBEbf"
    oracle_token_address = "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0"
    autopay_address = "0x3b50dEc3CA3d34d5346228D86D29CF679EAA0Ccb"
    private_key = os.getenv("MAINNET_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "goerli":
    provider_url = os.getenv("PROVIDER_URL_GOERLI")
    oracle_address = "0xD9157453E2668B2fc45b7A803D3FEF3642430cC0"
    oracle_token_address = "0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2"
    autopay_address = "0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0"
    private_key = os.getenv("GOERLI_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "sepolia":
    provider_url = os.getenv("PROVIDER_URL_SEPOLIA")
    oracle_address = "0xB19584Be015c04cf6CFBF6370Fe94a58b7A38830"
    oracle_token_address = "0x80fc34a2f9FfE86F41580F47368289C402DEc660"
    autopay_address = "0xB59a8085b4C360a3694396CA8E09441052656cF6"
    private_key = os.getenv("SEPOLIA_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "goerli_playground":
    provider_url = os.getenv("PROVIDER_URL_GOERLI")
    oracle_address = "0x3251838bd813fdf6a97D32781e011cce8D225d59"
    oracle_token_address = "0x3251838bd813fdf6a97D32781e011cce8D225d59"
    autopay_address = "0x9F6091CD579304a27Cf8Ab4927b1e0c242F61B4D"
    private_key = os.getenv("GOERLI_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "polygon":
    provider_url = os.getenv("PROVIDER_URL_POLYGON")
    oracle_address = "0x8cFc184c877154a8F9ffE0fe75649dbe5e2DBEbf"
    oracle_token_address = "0xE3322702BEdaaEd36CdDAb233360B939775ae5f1"
    autopay_address = "0x11cA06aa780ce89dbBF5D8F5fA8bf6965Be942c9"
    private_key = os.getenv("POLYGON_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    base_token_price_url_selector = "matic-network"
    gas_price_url = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "mumbai":
    provider_url = os.getenv("PROVIDER_URL_MUMBAI")
    oracle_address = "0xB0ff935b775a70504b810cf97c39987058e18550"
    oracle_token_address = "0x3251838bd813fdf6a97D32781e011cce8D225d59"
    autopay_address = "0xBfe8B0b5dBB521bdD1CF8E09432B41eD5328619a"
    private_key = os.getenv("MUMBAI_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    base_token_price_url_selector = "matic-network"
    gas_price_url = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "optimism":
    provider_url = os.getenv("PROVIDER_URL_OPTIMISM")
    oracle_address = "0x8cFc184c877154a8F9ffE0fe75649dbe5e2DBEbf"
    oracle_token_address = "0xaf8cA653Fa2772d58f4368B0a71980e9E3cEB888"
    autopay_address = "0x3b50dEc3CA3d34d5346228D86D29CF679EAA0Ccb"
    private_key = os.getenv("OPTIMISM_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api-optimistic.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken" # not used
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "optimism-goerli":
    provider_url = os.getenv("PROVIDER_URL_OPTIMISM_GOERLI")
    oracle_address = "0xD9157453E2668B2fc45b7A803D3FEF3642430cC0"
    oracle_token_address = "0xd71F72C18767083e4e3FE84F9c62b8038C1Ef4f6"
    autopay_address = "0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0"
    private_key = os.getenv("OPTIMISM_GOERLI_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api-optimistic.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken" # not used
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "zkevm":
    provider_url = os.getenv("PROVIDER_URL_ZKEVM")
    oracle_address = "0x34Fae97547E990ef0E05e05286c51E4645bf1A85"
    oracle_token_address = "0x03346b2F4BC23fd7f4935f74E70c7a7FebC45313"
    autopay_address = "0x6684E5DdbEe1b97E10847468cB5f4e38f3aB83FE"
    private_key = os.getenv("ZKEVM_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.zkevm.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken" # not used
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
elif network == "ganache":
    provider_url = os.getenv("PROVIDER_URL_GANACHE")
    oracle_address = "0x8d38Fdc9d2d75476b473bA5c50Cc4bd92E0b2301"
    oracle_token_address = "0x8d38Fdc9d2d75476b473bA5c50Cc4bd92E0b2301"
    autopay_address = "0xeC3FEf7f14049A4Aa42C0106A9c1D70ae5425BB6"
    private_key = os.getenv("GANACHE_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    redstone_feed_address = os.getenv("REDSTONE_FEED_ADDRESS")
else:
    print("invalid network")


# can change these values or leave them as is
start_time = datetime.datetime(2022, 12, 1, 0, 0, 0) # start time for the first interval
initial_profit_margin_usd = 2.0 # usd
tip_multiplier = 1.10 # multiplier for each tip retry
max_retip_count = 10 # max number of times to retry a tip
retip_delay = 45 # seconds
total_gas_cost=700000 # cost of submitValue + claimTip
api_max_tries = 10 # max number of times to retry api calls
token_approval_amount = 1000e18 # amount of oracle token to approve for autopay contract




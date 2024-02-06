import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# can change these values or leave them as is
start_time = datetime.datetime(2022, 12, 1, 0, 0, 0) # start time for the first interval
initial_profit_margin_usd = 1.0 # usd
tip_multiplier = 1.10 # multiplier for each tip retry
max_retip_count = 10 # max number of times to retry a tip
retip_delay = 45 # seconds
total_gas_cost=700000 # cost of submitValue + claimTip
api_max_tries = 10 # max number of times to retry api calls
token_approval_amount = 1000e18 # amount of oracle token to approve for autopay contract
# leave these as-is
network = os.getenv("NETWORK") # ganache, goerli, mainnet, mumbai, polygon
query_id = os.getenv("QUERY_ID")
query_data = os.getenv("QUERY_DATA")
interval = int(os.getenv("INTERVAL")) # in seconds
price_change_threshold = float(os.getenv("PRICE_CHANGE_THRESHOLD")) # collateral token price change threshold
collateral_token_price_url = os.getenv("COLLATERAL_TOKEN_PRICE_URL_COINGECKO")
api3_feed_address = os.getenv("API3_FEED_ADDRESS")
api3_max_price_deviation = float(os.getenv("API3_MAX_PRICE_DEVIATION_FROM_PREVIOUS_ROUND"))
api3_is_frozen_timeout = int(os.getenv("API3_IS_FROZEN_TIMEOUT"))

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
elif network == "polygon":
    provider_url = os.getenv("PROVIDER_URL_POLYGON")
    oracle_address = "0x8cFc184c877154a8F9ffE0fe75649dbe5e2DBEbf"
    oracle_token_address = "0xE3322702BEdaaEd36CdDAb233360B939775ae5f1"
    autopay_address = "0x11cA06aa780ce89dbBF5D8F5fA8bf6965Be942c9c"
    private_key = os.getenv("POLYGON_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    base_token_price_url_selector = "matic-network"
    gas_price_url = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
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
elif network == "mantle":
    provider_url = os.getenv("PROVIDER_URL_MANTLE")
    oracle_address = "0x46038969D7DC0b17BC72137D07b4eDe43859DA45"
    oracle_token_address = "0x35D48A789904E9b15705977192e5d95e2aF7f1D3"
    autopay_address = "0x6C77f2c171C8cEe08F7A5645c34BB14A29b8532f"
    private_key = os.getenv("MANTLE_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=mantle&vs_currencies=usd"
    base_token_price_url_selector = "mantle"
    gas_price_url = "NA"
elif network == "mantle-goerli":
    provider_url = os.getenv("PROVIDER_URL_MANTLE_GOERLI")
    oracle_address = "0xf9C672525284C76b9a7e83BE94849Af47624a2dd"
    oracle_token_address = "0x46038969D7DC0b17BC72137D07b4eDe43859DA45"
    autopay_address = "0x10c9042C4BBD61E98bB2b3dfb90d127Be4328Aab"
    private_key = os.getenv("MANTLE_GOERL_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=mantle&vs_currencies=usd"
    base_token_price_url_selector = "mantle"
    gas_price_url = "NA"
elif network == "ganache":
    provider_url = os.getenv("PROVIDER_URL_GANACHE")
    oracle_address = "0xB568253aD5D232bF8BbF56AFCf505D03D1D42aFf"
    oracle_token_address = "0xB568253aD5D232bF8BbF56AFCf505D03D1D42aFf"
    autopay_address = "0x499A0eDDD9B34737E7A809AAb0fa22dc965Eb0E1"
    private_key = os.getenv("GANACHE_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
else:
    print("invalid network")





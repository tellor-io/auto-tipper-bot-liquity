import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# update these values
network = "ganache" # ganache, goerli, mainnet, mumbai, polygon
query_id = "0x40aa71e5205fdc7bdb7d65f7ae41daca3820c5d3a8f62357a99eda3aa27244a3" # eth/usd
query_data = "0x00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000953706f745072696365000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000056d6174696300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000037573640000000000000000000000000000000000000000000000000000000000"
interval = 60 * 1 # seconds

if network == "mainnet":
    provider_url = os.getenv("PROVIDER_URL_MAINNET")
    oracle_address = "0xB3B662644F8d3138df63D2F43068ea621e2981f9"
    oracle_token_address = "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0"
    autopay_address = "0x1F033Cb8A2Df08a147BC512723fd0da3FEc5cCA7"
    private_key = os.getenv("MAINNET_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
elif network == "goerli":
    provider_url = os.getenv("PROVIDER_URL_GOERLI")
    oracle_address = "0xB3B662644F8d3138df63D2F43068ea621e2981f9"
    oracle_token_address = "0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2"
    autopay_address = "0x1F033Cb8A2Df08a147BC512723fd0da3FEc5cCA7"
    private_key = os.getenv("GOERLI_PK")
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
    oracle_address = "0x8f55D884CAD66B79e1a131f6bCB0e66f4fD84d5B"
    oracle_token_address = "0xE3322702BEdaaEd36CdDAb233360B939775ae5f1"
    autopay_address = "0x1775704809521D4D7ee65B6aFb93816af73476ec"
    private_key = os.getenv("POLYGON_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    base_token_price_url_selector = "matic-network"
    gas_price_url = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
elif network == "mumbai":
    provider_url = os.getenv("PROVIDER_URL_MUMBAI")
    oracle_address = "0x8f55D884CAD66B79e1a131f6bCB0e66f4fD84d5B"
    oracle_token_address = "0xCE4e32fE9D894f8185271Aa990D2dB425DF3E6bE"
    autopay_address = "0x1775704809521D4D7ee65B6aFb93816af73476ec"
    private_key = os.getenv("MUMBAI_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    base_token_price_url_selector = "matic-network"
    gas_price_url = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
elif network == "ganache":
    provider_url = os.getenv("PROVIDER_URL_GANACHE")
    oracle_address = "0xD4aaC57fd0696F5fFF38C622FcA94D7bB722A9fC"
    oracle_token_address = "0xD4aaC57fd0696F5fFF38C622FcA94D7bB722A9fC"
    autopay_address = "0xCBC648c91E75E6d5ac7B8ff51aEb62085A0f1F4A"
    private_key = os.getenv("GANACHE_PK")
    oracle_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd"
    oracle_token_price_url_selector = "tellor"
    base_token_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    base_token_price_url_selector = "ethereum"
    gas_price_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
else:
    print("invalid network")


# can change these values or leave them as is
start_time = datetime.datetime(2022, 12, 1, 0, 0, 0) # start time for the first interval
initial_profit_margin_usd = 2.0 # usd
tip_multiplier = 1.10 # multiplier for each tip retry
max_retip_count = 10 # max number of times to retry a tip
retip_delay = 45 # seconds
total_gas_cost=2000000 # cost of submitValue + claimTip
api_max_tries = 10 # max number of times to retry api calls
token_approval_amount = 1000e18 # amount of oracle token to approve for autopay contract




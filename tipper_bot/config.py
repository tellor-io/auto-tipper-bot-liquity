import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# update these values
network = "goerli" # ganache, goerli, mainnet, mumbai, polygon
query_id = "0x83a7f3d48786ac2667503a61e8c415438ed2922eb86a2906e4ee66d9a2ce4992" # eth/usd
query_data = "0x00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000953706f745072696365000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000003657468000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000037573640000000000000000000000000000000000000000000000000000000000"
interval = 60 * 10 # seconds

if network == "ganache":
    provider_url = os.getenv("PROVIDER_URL_GANACHE")
    oracle_address = "0xD4aaC57fd0696F5fFF38C622FcA94D7bB722A9fC"
    oracle_token_address = "0xD4aaC57fd0696F5fFF38C622FcA94D7bB722A9fC"
    autopay_address = "0xCBC648c91E75E6d5ac7B8ff51aEb62085A0f1F4A"
    private_key = os.getenv("GANACHE_PK")
elif network == "goerli":
    provider_url = os.getenv("PROVIDER_URL_GOERLI")
    oracle_address = "0xB3B662644F8d3138df63D2F43068ea621e2981f9"
    oracle_token_address = "0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2"
    autopay_address = "0x1F033Cb8A2Df08a147BC512723fd0da3FEc5cCA7"
    private_key = os.getenv("GOERLI_PK")
elif network == "goerli_playground":
    provider_url = os.getenv("PROVIDER_URL_GOERLI")
    oracle_address = "0x3251838bd813fdf6a97D32781e011cce8D225d59"
    oracle_token_address = "0x3251838bd813fdf6a97D32781e011cce8D225d59"
    autopay_address = "0x9F6091CD579304a27Cf8Ab4927b1e0c242F61B4D"
    private_key = os.getenv("GOERLI_PK")
else:
    print("invalid network")


# can change these values or leave them as is
start_time = datetime.datetime(2022, 12, 1, 0, 0, 0) # start time for the first interval
initial_profit_margin_usd = 2.0 # usd
tip_multiplier = 1.10 # multiplier for each tip retry
max_retip_count = 10 # max number of times to retry a tip
retip_delay = 30 # seconds
total_gas_cost=2000000 # cost of submitValue + claimTip
api_max_tries = 10 # max number of times to retry api calls
token_approval_amount = 1000e18 # amount of oracle token to approve for autopay contract




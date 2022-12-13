import requests
import json
import time
from web3 import Web3
import config
import time
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# load config values
start_time = config.start_time
interval = config.interval
query_id = config.query_id
query_data = config.query_data
tip_multiplier = config.tip_multiplier
initial_profit_margin_usd = config.initial_profit_margin_usd
max_retip_count = config.max_retip_count

trb_price = 0.0
last_report_time = 0


# setup provider
provider_url = os.getenv("PROVIDER_URL")
web3 = Web3(Web3.HTTPProvider(provider_url))
# set private key
web3.eth.account.enable_unaudited_hdwallet_features()
acct = web3.eth.account.privateKeyToAccount(os.getenv("PRIVATE_KEY"))
web3.eth.defaultAccount = acct.address
print("Connected to Ethereum node: ", web3.isConnected())
print("Current block number: ", web3.eth.blockNumber)

# import playgound abi
with open("abis/TellorPlayground.json") as f:
    abi = json.load(f)

oracle_contract = web3.eth.contract(address=config.oracle_address, abi=abi)
oracle_token_contract = web3.eth.contract(address=config.oracle_token_address, abi=abi)

# import autopay abi
with open("abis/AutoPay.json") as f:
    abi = json.load(f)

autopay_contract = web3.eth.contract(address=config.autopay_address, abi=abi)

def get_gas_cost_in_trb():
    # get prices for base token and oracle token
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        response = response.json()
        base_token_price = response["ethereum"]["usd"]
        print("base token price: ", base_token_price)

        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tellor&vs_currencies=usd")
        response = response.json()
        oracle_token_price = response["tellor"]["usd"]
        trb_price = oracle_token_price
        print("oracle token price: ", oracle_token_price)

        # get gas price
        response = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
        response = response.json()
        gas_price = response["fast"] / 10
        print("gas price: ", gas_price)

        # convert gas cost to oracle token: gas_price * gas_cost * base_token_price / oracle_price
        gas_cost_oracle_token = gas_price * config.total_gas_cost * base_token_price / oracle_token_price / 1000000000
        return (gas_cost_oracle_token, trb_price)
    except:
        print("error getting gas cost in TRB")
        return (0.0, 0.0)

# function for determining number of seconds until next interval
def get_seconds_until_next_interval():
    current_time = datetime.datetime.now()
    next_interval = start_time + datetime.timedelta(seconds=interval)
    # get next interval after current time
    while next_interval < current_time:
        next_interval = next_interval + datetime.timedelta(seconds=interval)
    # get number of seconds until next interval
    seconds_until_next_interval = (next_interval - current_time).total_seconds()
    print("seconds until next interval: ", seconds_until_next_interval)
    return int(seconds_until_next_interval)

# function for getting required tip
def get_required_tip(try_count):
    (gas_cost_trb, trb_price) = get_gas_cost_in_trb()

    # handle api errors with limited retries
    api_max_tries = 10
    api_try_count = 0
    while trb_price == 0.0 and api_try_count < api_max_tries:
        print("trb price is 0, trying again in 10 seconds")
        time.sleep(2 * api_try_count)
        (gas_cost_trb, trb_price) = get_gas_cost_in_trb()
        api_try_count += 1


    print("gas cost in trb: ", gas_cost_trb)
    print("initial profit margin usd: ", initial_profit_margin_usd)
    print("trb price: ", trb_price)
    print("tip multiplier: ", tip_multiplier)
    print("try count: ", try_count)

    # calculate required tip
    required_tip = (gas_cost_trb + initial_profit_margin_usd / trb_price) * tip_multiplier ** try_count
    return required_tip

def update_last_report_time():
    current_time = datetime.datetime.now()
    print("current time: ", current_time.timestamp())
    data_before = oracle_contract.functions.getDataBefore(query_id, int(current_time.timestamp())).call()
    global last_report_time
    last_report_time = int(data_before[2])
    print("last report time: ", last_report_time)

def initiate_tipping_sequence(retip_count):
    # gas_cost_trb = get_gas_cost_in_trb()
    # print("gas cost in trb: ", gas_cost_trb)

    # calculate required tip
    required_tip = get_required_tip(retip_count)
    print("required tip: ", required_tip)

    if required_tip == 0.0:
        print("error getting required tip")
        return

    # get current tip
    current_tip = autopay_contract.functions.getCurrentTip(query_id).call()
    print("current tip: ", current_tip / 1e18)

    # check if current tip is less than required tip
    amount_to_tip = 0
    if current_tip < (required_tip * 1e18):
        # calculate tip amount
        amount_to_tip = (required_tip * 1e18) - current_tip
        print("tip amount: ", amount_to_tip / 1e18)

        # call tip function
        tx_hash = autopay_contract.functions.tip(query_id, int(amount_to_tip), query_data).transact()
        print("Transaction hash: ", tx_hash)

        # wait for transaction to be mined
        web3.eth.waitForTransactionReceipt(tx_hash)

    # wait 20 seconds
    print("sleeping...")
    time.sleep(20)

    # get current time
    current_time = datetime.datetime.now()

    # call getDataBefore function
    data_before = oracle_contract.functions.getDataBefore(query_id, int(current_time.timestamp())).call()
    last_report_time_updated = int(data_before[2])
    print("last report time updated: ", last_report_time_updated)
    print("last report time: ", last_report_time)

    # check if data is available
    if last_report_time_updated <= int(last_report_time):
        print("no new data reported")
        # check if try count is less than max try count
        if retip_count < max_retip_count:
            # initiate tipping sequence again
            print("try count ", retip_count, " is less than max try count ", max_retip_count)
            initiate_tipping_sequence(retip_count + 1)
    else:
        print("new data reported")


            

while True:

    update_last_report_time()
    seconds_until_next_interval = get_seconds_until_next_interval()

    if seconds_until_next_interval < 60: # and int(last_report_time) < int(start_time.timestamp()):
        # initiate tipping sequence
        print("initiating tipping sequence")
        initiate_tipping_sequence(retip_count = 0)
    else:
        # sleep until next interval
        time.sleep(seconds_until_next_interval / 2 + 1)




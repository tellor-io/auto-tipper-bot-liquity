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

last_report_time = 0


# setup provider
provider_url = config.provider_url
web3 = Web3(Web3.HTTPProvider(provider_url))
# set private key
web3.eth.account.enable_unaudited_hdwallet_features()
acct = web3.eth.account.privateKeyToAccount(config.private_key)
web3.eth.defaultAccount = acct.address
print("Connected to Ethereum node: ", web3.isConnected())
print("Using address: ", web3.eth.defaultAccount)
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

print("oracle contract: ", oracle_contract.address)
print("oracle token contract: ", oracle_token_contract.address)
print("autopay contract: ", autopay_contract.address)

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
        response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken")
        response = response.json()
        gas_price = float(response["result"]["FastGasPrice"])
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
    api_max_tries = config.api_max_tries
    api_try_count = 1
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

def tip(amount_to_tip):
    print("tipping: ", amount_to_tip)
    # build transaction 
    tx = autopay_contract.functions.tip(query_id, int(amount_to_tip), query_data).buildTransaction()

    # get gas estimate
    gas_estimate = web3.eth.estimateGas(tx)
    print("gas estimate: ", gas_estimate)

    # update transaction with gas estimate
    tx.update({'gas': gas_estimate})

    # update nonce
    tx.update({'nonce': web3.eth.getTransactionCount(acct.address)})

    # sign transaction
    signed_tx = web3.eth.account.signTransaction(tx, private_key=config.private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print("tx hash: ", tx_hash.hex())
    # wait for transaction to be mined
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


def initiate_tipping_sequence(retip_count):
    # calculate required tip
    required_tip = get_required_tip(retip_count)
    print("required tip: ", required_tip)

    if required_tip == 0.0:
        print("error getting required tip")
        return

    # get current tip
    current_tip = autopay_contract.functions.getCurrentTip(query_id).call()
    print("current tip: ", current_tip / 1e18)

    # call getDataBefore function, check for new report since tipping sequence started
    current_time = datetime.datetime.now()
    data_before = oracle_contract.functions.getDataBefore(query_id, int(current_time.timestamp())).call()
    last_report_time_updated = int(data_before[2])
    print("last report time updated: ", last_report_time_updated)
    print("last report time: ", last_report_time)

    # check if current tip is less than required tip and last report time has not changed
    amount_to_tip = 0
    if current_tip < (required_tip * 1e18) and last_report_time_updated == last_report_time:
        # calculate tip amount
        amount_to_tip = (required_tip * 1e18) - current_tip
        print("tip amount: ", amount_to_tip / 1e18)

        # # call tip function
        # tx_hash = autopay_contract.functions.tip(query_id, int(amount_to_tip), query_data).transact()
        # print("Transaction hash: ", tx_hash)

        # # wait for transaction to be mined
        # web3.eth.wait_for_transaction_receipt(tx_hash)

        # call tip function
        tip(amount_to_tip)

    # wait 20 seconds
    print("sleeping...")
    time.sleep(config.retip_delay)


    # call getDataBefore function
    current_time = datetime.datetime.now()
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

def approve_token():
    print("approving token")
    tx = oracle_token_contract.functions.approve(autopay_contract.address, int(config.token_approval_amount)).build_transaction()
    # get gas estimate
    gas_estimate = web3.eth.estimate_gas(tx)
    print("gas estimate: ", gas_estimate)
    # update transaction with appropriate gas amount
    tx.update({ 'gas' : gas_estimate })
    tx.update({ 'nonce' : web3.eth.get_transaction_count(acct.address) })
    signed_tx = web3.eth.account.sign_transaction(tx, config.private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Transaction hash: ", tx_hash)
    # wait for transaction to be mined
    web3.eth.wait_for_transaction_receipt(tx_hash)

while True:
    update_last_report_time()
    seconds_until_next_interval = get_seconds_until_next_interval()
    current_timestamp = datetime.datetime.now().timestamp()


    if seconds_until_next_interval < 60 and int(last_report_time) < int(current_timestamp) - int(config.interval / 10):
        # initiate tipping sequence
        print("\ninitiating tipping sequence")
        initiate_tipping_sequence(retip_count = 0)
    else:
        # check token allowance
        token_allowance = oracle_token_contract.functions.allowance(acct.address, autopay_contract.address).call()
        print("token allowance: ", token_allowance)
        if token_allowance < config.token_approval_amount / 10:
            # approve token allowance
            approve_token()
        # sleep until next interval
        time.sleep(seconds_until_next_interval / 2 + 1)




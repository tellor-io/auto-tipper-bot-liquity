import requests
import json
import time
from web3 import Web3
from tipper_bot import config
import time
import datetime
import os
from dotenv import load_dotenv
import logging
from urllib.parse import urlparse, parse_qs

load_dotenv()

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='logs/tipper.log', filemode='a')

# Create a logger object
logger = logging.getLogger("tipper_bot")
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create a file handler to save logs to a file
file_handler = logging.FileHandler("logs/tipper.log", mode="a")
file_handler.setLevel(logging.INFO)  # Set the minimum log level for the file handler

# Create a console handler to print logs to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the minimum log level for the console handler

# Create a formatter to define the log message format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Set the formatter for both handlers

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
# add the handler to the root logger
logging.getLogger('').addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# load config values
tip_multiplier = config.tip_multiplier
initial_profit_margin_usd = config.initial_profit_margin_usd
max_retip_count = config.max_retip_count
price_change_threshold = config.price_change_threshold

# setup provider
provider_url = config.provider_url
web3 = Web3(Web3.HTTPProvider(provider_url))
# set private key
web3.eth.account.enable_unaudited_hdwallet_features()
acct = web3.eth.account.privateKeyToAccount(config.private_key)
web3.eth.defaultAccount = acct.address
logging.info("Connected to Ethereum node: %s", web3.isConnected())
logging.info("Using network: %s", config.network)
logging.info("Using address: %s", web3.eth.defaultAccount)
logging.info("Current block number: %s", web3.eth.blockNumber)

# import playgound abi
with open("abis/TellorPlayground.json") as f:
    abi = json.load(f)

oracle_contract = web3.eth.contract(address=config.oracle_address, abi=abi)
oracle_token_contract = web3.eth.contract(
    address=config.oracle_token_address, abi=abi)

# import autopay abi
with open("abis/Autopay.json") as f:
    abi = json.load(f)

autopay_contract = web3.eth.contract(address=config.autopay_address, abi=abi)

with open("abis/DapiProxy.json") as f:
    abi = json.load(f)

api3_feed_contract = web3.eth.contract(address=config.api3_feed_address, abi=abi)

logging.info("oracle contract: %s", oracle_contract.address)
logging.info("oracle token contract: %s", oracle_token_contract.address)
logging.info("autopay contract: %s", autopay_contract.address)
logging.info("api3 feed contract: %s", api3_feed_contract.address)


def get_gas_cost_in_oracle_token():
    # get prices for base token and oracle token
    try:
        response_base_token = requests.get(
            config.base_token_price_url)
        response_json_base_token = response_base_token.json()
        base_token_price = response_json_base_token[config.base_token_price_url_selector]["usd"]
        logging.info("base token price: %s", base_token_price)

        response_oracle_token = requests.get(
            config.oracle_token_price_url)
        response_json_oracle_token = response_oracle_token.json()
        oracle_token_price = response_json_oracle_token[config.oracle_token_price_url_selector]["usd"]
        trb_price = oracle_token_price
        logging.info("oracle token price: %s", oracle_token_price)

        if config.network == 'mantle' or config.network == 'mantle-goerli':
            gas_price = 0.05
            gas_cost_usd = config.total_gas_cost * gas_price * base_token_price / 1000000000
        elif config.network == 'optimism' or config.network == 'optimism-goerli':
            # optimism uses custom gas cost calculation logic, just hardcode for now
            gas_cost_usd = 0.5
        else:
            # get gas price
            response_gas_price = requests.get(
                config.gas_price_url)
            response_json_gas_price = response_gas_price.json()
            gas_price = float(response_json_gas_price["result"]["FastGasPrice"])
            logging.info("gas price: %s", gas_price)

            gas_cost_usd = config.total_gas_cost * gas_price * base_token_price / 1000000000

        logging.info("gas cost in usd: %s", gas_cost_usd)
        # convert gas cost to oracle token: gas_price * gas_cost * base_token_price / oracle_price
        gas_cost_oracle_token = gas_cost_usd / oracle_token_price
        return (gas_cost_oracle_token, trb_price)
    except:
        logging.error("error getting gas cost in TRB")
        return (0.0, 0.0)

# function for determining number of seconds until next interval
def get_seconds_until_next_interval(interval, start_time):
    current_time = datetime.datetime.now()
    next_interval = start_time + datetime.timedelta(seconds=interval)
    # get next interval after current time
    while next_interval < current_time:
        next_interval = next_interval + datetime.timedelta(seconds=interval)
    # get number of seconds until next interval
    seconds_until_next_interval = (
        next_interval - current_time).total_seconds()
    logging.info("seconds until next interval: %s", seconds_until_next_interval)
    return int(seconds_until_next_interval)

# function for getting required tip
def get_required_tip(try_count):
    (gas_cost_trb, trb_price) = get_gas_cost_in_oracle_token()

    # handle api errors with limited retries
    api_max_tries = config.api_max_tries
    api_try_count = 0
    while trb_price == 0.0 and api_try_count < api_max_tries:
        sleep_time = 5 * 2 ** api_try_count
        logging.warning("trb price is 0, trying again in %s seconds", sleep_time)
        time.sleep(sleep_time)
        (gas_cost_trb, trb_price) = get_gas_cost_in_oracle_token()
        api_try_count += 1

    logging.info("gas cost in trb: %s", gas_cost_trb)
    logging.info("initial profit margin usd: %s", initial_profit_margin_usd)
    logging.info("trb price: %s", trb_price)
    logging.info("tip multiplier: %s", config.tip_multiplier)
    logging.info("try count: %s", try_count)

    if trb_price == 0.0:
        return 0.0

    # calculate required tip
    required_tip = (gas_cost_trb + initial_profit_margin_usd /
                    trb_price) * tip_multiplier ** try_count
    return required_tip

# function for getting last report time for given query id
def get_last_report_time(query_id):
    current_time = datetime.datetime.now()
    try:
        data_before = oracle_contract.functions.getDataBefore(
            query_id, int(current_time.timestamp())).call()
        timestamp_retrieved = int(data_before[2])
        logging.info("last report time: %s", timestamp_retrieved)
        return timestamp_retrieved
    except:
        logging.warning("error getting data before")
        return 0


def tip(amount_to_tip, query_id, query_data):
    logging.info("tipping: %s", amount_to_tip)
    # build transaction

    try:
        tx = autopay_contract.functions.tip(query_id, int(
            amount_to_tip), query_data).buildTransaction()
        logging.info("tx: %s", tx)
        # get gas estimate
        gas_estimate = web3.eth.estimateGas(tx)
        logging.info("gas estimate: %s", gas_estimate)

        # update transaction with gas estimate
        tx.update({'gas': gas_estimate})

        # update nonce
        tx.update({'nonce': web3.eth.getTransactionCount(acct.address)})
    except:
        logging.warning("error building transaction")
        logging.info("building legacy transaction")
        tx = autopay_contract.functions.tip(query_id, int(
            amount_to_tip), query_data).buildTransaction({
                'gasPrice': web3.eth.gas_price,
                'nonce': web3.eth.getTransactionCount(acct.address),
                # 'gas': gas_estimate,
        })
        

    # sign transaction
    signed_tx = web3.eth.account.signTransaction(
        tx, private_key=config.private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    logging.info("tx hash: %s", tx_hash.hex())
    # wait for transaction to be mined
    web3.eth.waitForTransactionReceipt(tx_hash)


def initiate_tipping_sequence(retip_count, query_id, query_data, last_report_time, balances):
    # calculate required tip
    required_tip = get_required_tip(retip_count)
    logging.info("required tip: %s", required_tip)

    if required_tip == 0.0:
        logging.error("error getting required tip, exiting")
        return

    # get current tip
    current_tip = autopay_contract.functions.getCurrentTip(query_id).call()
    logging.info("current tip: %s", current_tip / 1e18)

    # call getDataBefore function, check for new report since tipping sequence started
    current_time = datetime.datetime.now()
    data_before = oracle_contract.functions.getDataBefore(
        query_id, int(current_time.timestamp())).call()
    last_report_time_updated = int(data_before[2])
    logging.info("last report time updated:  %s", last_report_time_updated)
    logging.info("last report time previous: %s", last_report_time)

    # check if current tip is less than required tip or last report time has not changed
    amount_to_tip = 0
    if current_tip < (required_tip * 1e18) or last_report_time_updated == last_report_time:
        # calculate tip amount
        amount_to_tip = (required_tip * 1e18) - current_tip
        if amount_to_tip < 0:
            amount_to_tip = 0
        logging.info("amount to tip: %s", amount_to_tip / 1e18)

        # check if oracle token balance is zero
        if(balances[0] == 0):
            logging.error("zero %s oracle token balance, exiting", config.oracle_token_price_url_selector)
            return
        # check if oracle token balance is less than amount to tip
        if(balances[0] < amount_to_tip):
            logging.warning("not enough %s oracle token balance to tip", config.oracle_token_price_url_selector)
            logging.warning("using all %s oracle token balance to tip", config.oracle_token_price_url_selector)
            amount_to_tip = balances[0]
            logging.info("new amount to tip: %s", amount_to_tip / 1e18)
        
        if(amount_to_tip > 0):
            tip(amount_to_tip, query_id, query_data)

        # wait 20 seconds
        logging.info("sleeping %s seconds...", config.retip_delay)
        time.sleep(config.retip_delay)

        # call getDataBefore function
        current_time = datetime.datetime.now()
        data_before = oracle_contract.functions.getDataBefore(
            query_id, int(current_time.timestamp())).call()
        last_report_time_updated = int(data_before[2])
        logging.info("last report time updated:  %s", last_report_time_updated)
        logging.info("last report time previous: %s", last_report_time)

        # check if data is available
        if last_report_time_updated <= int(last_report_time):
            logging.info("no new data reported")
            # check if try count is less than max try count
            if retip_count < max_retip_count:
                balances = approve_token_and_check_balance()
                # initiate tipping sequence again
                logging.info("try count %s is less than max try count %s", retip_count, max_retip_count)
                logging.info("initiating tipping sequence again")
                initiate_tipping_sequence(retip_count + 1, query_id, query_data, last_report_time, balances)
        else:
            logging.info("new data reported")

def approve_token_and_check_balance():
    # check balances
    oracle_token_balance = oracle_token_contract.functions.balanceOf(
        acct.address).call()
    logging.info("%s token balance: %s", config.oracle_token_price_url_selector, oracle_token_balance / 1e18)
    base_token_balance = web3.eth.get_balance(acct.address)
    logging.info("%s token balance: %s", config.base_token_price_url_selector, base_token_balance / 1e18)

    min_base_token_balance = get_min_base_token_balance()
    if base_token_balance < min_base_token_balance:
        logging.error("base token balance is less than minimum required balance")
        logging.error("min required balance: %s", min_base_token_balance)
        check_allowance = False
    else:
        # check token allowance
        token_allowance = oracle_token_contract.functions.allowance(
            acct.address, autopay_contract.address).call()
        logging.info("token allowance: %s", token_allowance / 1e18)
        if token_allowance < config.token_approval_amount / 10:
            # approve token allowance
            logging.info("approving token amount: %s", config.token_approval_amount)
            try:
                tx = oracle_token_contract.functions.approve(autopay_contract.address, int(
                    config.token_approval_amount)).build_transaction()
                # get gas estimate
                gas_estimate = web3.eth.estimate_gas(tx)
                logging.info("gas estimate: %s", gas_estimate)
                # update transaction with appropriate gas amount
                tx.update({'gas': gas_estimate})
                tx.update({'nonce': web3.eth.get_transaction_count(acct.address)})
            except:
                logging.warning("error building transaction")
                logging.info("building legacy transaction")
                tx = oracle_token_contract.functions.approve(autopay_contract.address, int(
                    config.token_approval_amount)).buildTransaction({
                        'gasPrice': web3.eth.gas_price,
                        'nonce': web3.eth.getTransactionCount(acct.address),
                        # 'gas': gas_estimate,
                })
            signed_tx = web3.eth.account.sign_transaction(tx, config.private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logging.info("transaction hash: %s", tx_hash.hex())
            # wait for transaction to be mined
            web3.eth.wait_for_transaction_receipt(tx_hash)
    return [oracle_token_balance, base_token_balance]

def get_api3_latest_data(latest_data, previous_data):
    try:
        latest_data_tmp = api3_feed_contract.functions.read().call()
        if latest_data == 0:
            # first time calling this function
            return latest_data_tmp, latest_data_tmp
        elif latest_data_tmp[1] == latest_data[1]:
            # no new data
            return latest_data, previous_data
        else:
            return latest_data_tmp, latest_data
    except:
        logging.warning("error getting api3 latest data")
        return 0, 0

def extract_selectors(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token_selector = query_params.get('ids', [None])[0]
    currency_selector = query_params.get('vs_currencies', [None])[0]
    return token_selector, currency_selector
    
def collateral_price_change_above_threshold(last_saved_collateral_price):
    # get collateral price from coingecko
    try:
        response = requests.get(
            config.collateral_token_price_url)
        response_json = response.json()
        collateral_token_price_selector, currency_selector = extract_selectors(config.collateral_token_price_url)
        collateral_token_price = response_json[collateral_token_price_selector][currency_selector]
        logging.info("collateral token price: %s", collateral_token_price)
        # check if price change is above threshold
        if last_saved_collateral_price == 0:
            last_saved_collateral_price = collateral_token_price
            return False, last_saved_collateral_price
        price_change = abs(collateral_token_price - last_saved_collateral_price) / last_saved_collateral_price
        logging.info("price change: %s", price_change)
        if price_change >= config.price_change_threshold:
            logging.info("price change above threshold")
            return True, last_saved_collateral_price
        else:
            return False, last_saved_collateral_price
    except:
        logging.warning("error getting collateral token price")
        return False

def api3_price_change_above_max(latest_data, previous_data):
    if latest_data == 0 or previous_data == 0:
        return False
    current_price = latest_data[0]
    previous_price = previous_data[0]

    min_price = min(current_price, previous_price)
    max_price = max(current_price, previous_price)

    percent_deviation = (max_price - min_price) / max_price
    if percent_deviation > config.api3_max_price_deviation:
        logging.info("api3 price change above max")
        return True
    else:
        return False
        
def api3_is_frozen(api3_latest_data):
    current_timestamp = datetime.datetime.now().timestamp()
    latest_timestamp = api3_latest_data[1]
    if current_timestamp - latest_timestamp > config.api3_is_frozen_timeout:
        logging.info("api3 is almost frozen. latest timestamp: %s", latest_timestamp)
        return True
    else:
        return False

def api3_is_broken(api3_latest_data):
    current_timestamp = datetime.datetime.now().timestamp()
    updated_at = api3_latest_data[1]
    answer = api3_latest_data[0]
    if int(updated_at) == 0 or int(updated_at) > current_timestamp:
        logging.info("api3 is broken. updated at: %s", updated_at)
        return True
    if int(answer) == 0:
        logging.info("api3 is broken. answer: %s", answer)
        return True
    # api3 is not broken
    return False

def get_min_base_token_balance():
    gas_cost = config.total_gas_cost
    gas_price = web3.eth.gas_price
    min_base_token_balance = gas_cost * gas_price * 4
    return min_base_token_balance

def main():
    query_id = config.query_id
    query_data = config.query_data
    interval = config.interval
    start_time = config.start_time
    collateral_token_price = 0
    api3_latest_data = 0
    api3_previous_data = 0

    balances = approve_token_and_check_balance()
    while True:
        last_report_time = get_last_report_time(query_id=query_id)
        seconds_until_next_interval = get_seconds_until_next_interval(interval=interval, start_time=start_time)
        current_timestamp = datetime.datetime.now().timestamp()
        seconds_since_last_tellor_report = current_timestamp - int(last_report_time)
        api3_latest_data, api3_previous_data = get_api3_latest_data(api3_latest_data, api3_previous_data)
        # bools must all be true to report
        sufficient_funds_bool = True
        report_for_backup_oracle = False
        seconds_since_last_tellor_report_is_sufficient = False
        collateral_price_change_above_threshold_bool = False
        if price_change_threshold > 0:
            collateral_price_change_above_threshold_bool, collateral_token_price = collateral_price_change_above_threshold(collateral_token_price)
        if balances[0] == 0:
            logging.error("zero %s oracle token balance", config.oracle_token_price_url_selector)
            sufficient_funds_bool = False
        min_base_token_balance = get_min_base_token_balance()
        if balances[1] < min_base_token_balance:
            logging.error("%s base token balance is less than minimum required balance", config.base_token_price_url_selector)
            sufficient_funds_bool = False
        if api3_latest_data != 0:
            if api3_is_frozen(api3_latest_data):
                report_for_backup_oracle = True
            elif api3_is_broken(api3_latest_data):
                report_for_backup_oracle = True
            elif api3_price_change_above_max(api3_latest_data, api3_previous_data):
                report_for_backup_oracle = True

        if seconds_since_last_tellor_report >= config.api3_is_frozen_timeout:
            seconds_since_last_tellor_report_is_sufficient = True
        if (sufficient_funds_bool and report_for_backup_oracle) and (seconds_since_last_tellor_report_is_sufficient or collateral_price_change_above_threshold_bool):
            # initiate tipping sequence
            logging.info("initiating tipping sequence")
            initiate_tipping_sequence(retip_count=0, query_id=query_id, query_data=query_data, last_report_time=last_report_time, balances=balances)
        else:
            balances = approve_token_and_check_balance()
            # sleep until next interval
            logging.info("sleeping until next interval")
            time.sleep(seconds_until_next_interval + 1)
    return None

if __name__ == "__main__":
    main()

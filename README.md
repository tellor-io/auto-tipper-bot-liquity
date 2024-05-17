# Liquity Auto Tipper Bot - Redstone Primary

This is a bot for automatically detecting when the Tellor backup oracle will be triggered in a Liquity-like system with Redstone as a primary oracle, and adding a tip for Tellor data in that case. Currently supported networks include Ethereum mainnet, Polygon, Optimism, Bob, Goerli, Mumbai, and Optimism-Goerli.

### Clone repo and cd
```sh
git clone -b redstone --single-branch https://github.com/tellor-io/auto-tipper-bot-liquity.git
```
```sh
cd auto-tipper-bot-liquity
```
```sh
mv .env.example .env
```

### Setup

```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
```

```sh
pip install -e .
```

### Usage
Add your private key and rpc url to `.env` file. Update the `QUERY_ID`, `QUERY_DATA`, and `REDSTONE_FEED_ADDRESS`, `REDSTONE_DATAFEED_ID`, and `NETWORK` to your desired values. Set the `INTERVAL` based on how often you want the bot to check conditions for adding a tip. In addition, set the `REDSTONE_IS_FROZEN_TIMEOUT` and `REDSTONE_MAX_PRICE_DEVIATION_FROM_PREVIOUS_ROUND` parameters to match the Liquity-like `PriceFeed` contract.

In the case where tellor is triggered as the oracle, if you also want your bot to tip based on a collateral price change threshold, set the `PRICE_CHANGE_THRESHOLD` to a value greater than 0. A value of `0.05` represents a price change of 5%, for example. Set `COLLATERAL_TOKEN_PRICE_URL_COINGECKO` to the url of the price feed for your collateral token. With this feature enabled, the bot will tip if any of the "Redstone is down" conditions are met, and the collateral token price changes by more than this threshold. Note that, in the event any of the "Redstone is down" conditions are met, the bot will also continue to tip in an interval of `REDSTONE_IS_FROZEN_TIMEOUT`. To disable this feature, set `PRICE_CHANGE_THRESHOLD` to `0`.

**To begin tipping**
```sh
tipper
```

### How It Works
The bot watches for Redstone broken, Redstone frozen, and Redstone data outside threshold conditions. If any of these conditions are met, the bot will automatically determine a tip amount as a function of the current gas cost, oracle token price (TRB), and base token price (ETH, MATIC, etc.). It calculates the cost of paying for gas in terms of the oracle token and adds a buffer of $2. It then waits 45 seconds for a data report. If a report is submitted, the bot then waits for the next tipping interval, again checking for backup oracle conditions to be met. If no report was submitted, the bot recalculates the gas cost in terms of the oracle token, adds the $2 buffer, and multiplies this value by 1.10. It keeps doing this until a report is submitted or up to a max of 10 times.

### Why Use This
The Tellor oracle works by incentivizing data reporters to submit your requested data. Reporters have to cover gas costs plus earn some profit. This bot is a handy tool for any liquity-like protocol which wants to pay for Tellor data only when needed.

## Maintainers <a name="maintainers"> </a>
This repository is maintained by the [Tellor team](https://github.com/orgs/tellor-io/people)


## How to Contribute<a name="how2contribute"> </a>  

Check out our issues log here on Github or feel free to reach out anytime [info@tellor.io](mailto:info@tellor.io)

## Copyright

Tellor Inc. 2023
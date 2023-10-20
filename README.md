# Auto Tipper Bot

This is a bot for automatically detecting when the Tellor backup oracle will be triggered in a Liquity-like system and adding a tip for Tellor data in that case. Currently supported networks include Ethereum mainnet, Polygon, Optimism, Goerli, Mumbai, and Optimism-Goerli.

### Clone repo and cd
```sh
git clone https://github.com/tellor-io/auto-tipper-bot-liquity.git
```
```sh
cd auto-tipper-bot
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
Add your private key and rpc url to `.env` file. Update the `QUERY_ID`, `QUERY_DATA`, and `CHAINLINK_AGGREGATOR_ADDRESS`, and `NETWORK` to your desired values.

**To begin tipping**
```sh
tipper
```

### How It Works
The bot watches for Chainlink broken, Chainlink frozen, and Chainlink data outside threshold conditions. If any of these conditions are met, the bot will automatically determine a tip amount as a function of the current gas cost, oracle token price (TRB), and base token price (ETH, MATIC). It calculates the cost of paying for gas in terms of the oracle token and adds a buffer of $2. It then waits 45 seconds for a data report. If a report is submitted, the bot then waits for the next tipping interval, again checking for backup oracle conditions to be met. If no report was submitted, the bot recalculates the gas cost in terms of the oracle token, adds the $2 buffer, and multiplies this value by 1.10. It keeps doing this until a report is submitted or up to a max of 10 times.

### Why Use This
The Tellor oracle works by incentivizing data reporters to submit your requested data. Reporters have to cover gas costs plus earn some profit. This bot is a handy tool for any liquity-like protocol which wants to pay for Tellor data only when needed.

## Maintainers <a name="maintainers"> </a>
This repository is maintained by the [Tellor team](https://github.com/orgs/tellor-io/people)


## How to Contribute<a name="how2contribute"> </a>  

Check out our issues log here on Github or feel free to reach out anytime [info@tellor.io](mailto:info@tellor.io)

## Copyright

Tellor Inc. 2023
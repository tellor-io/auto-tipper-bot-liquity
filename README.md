# Auto Tipper Bot

This is a bot for automatically tipping a query id at a fixed interval. It is a work in progress and is not yet ready for use. It can currently tip a query id on Goerli at a fixed interval, wait for a data report, and increase the tip a max number of times until a report is submitted.

### Clone repo and cd
```sh
git clone git@github.com:tellor-io/auto-tipper-bot.git
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
Add your private key and Goerli rpc url to `.env` file. Update the `query_id`, `query_data`, and `interval` in the `tipper_bot/config.py` file. 

**To begin tipping**
```sh
tipper
```

## Maintainers <a name="maintainers"> </a>
This repository is maintained by the [Tellor team](https://github.com/orgs/tellor-io/people)


## How to Contribute<a name="how2contribute"> </a>  

Check out our issues log here on Github or feel free to reach out anytime [info@tellor.io](mailto:info@tellor.io)

## Copyright

Tellor Inc. 2022
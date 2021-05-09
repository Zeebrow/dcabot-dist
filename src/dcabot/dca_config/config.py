import sys
import os
import logging
import configparser

logger = logging.getLogger(__name__)
TRUE_STRINGS = ['Y', 'YES', 'TRUE' '1']
FALSE_STRINGS = ['N', 'NO', 'FALSE', '0']
DEFAULT_CONFIG_FILEPATH = "/home/mike/bin/dcabot-minimal/etc/dcabot.conf"

try:
    os.stat(DEFAULT_CONFIG_FILEPATH)
except FileNotFoundError:
    logger.critical(f"Could not find configuration file at {DEFAULT_CONFIG_FILEPATH}. Exiting!")
    exit(1)

# Configuration
config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_FILEPATH)

def check_files_exist(config_file=DEFAULT_CONFIG_FILEPATH):
    # check conf files and handle errors
    if (not os.path.exists(config_file)):
        logger.error(f"Could not find configuration file {config_file}. Exiting!") # (should ask to generate a new one
        return False
    return True

def get_tracked_currencies():
    tracked_currencies = []
    buy_amt = []
    for section in config.sections():
        if '-usd' in section:
            t = section.upper(),config[section]['daily_buy']
            tracked_currencies.append(t)
    return tracked_currencies

def generate_new_configfile():
    pass

def validate_config(config_file):
    # Check for vars, catch typos (You want to buy HOW MUCH?!)
    pass

def default_trigger(daily_buy_total: float, current_balance: float):
    logger.warn("Unable to get low balance alert level from configuration!")
    logger.warn(f"Defaulting to 2x daily buy total (${2*daily_buy_total:.2f})")
    if 2*daily_buy_total > current_balance:
        return True
    else:
        return False

def trigger_low_bal_alert(low_bal_level: str, current_balance: float, daily_buy_total: float):
    try:
        low_bal_level = float(low_bal_level)
        if low_bal_level < current_balance:
            return True
        else:
            return False
    except ValueError:
        try:
            multiplier = int(low_bal_level[:-1])
            if multiplier*daily_buy_total > current_balance:
                return True
            else:
                return False
        except ValueError:
            return default_trigger(daily_buy_total, current_balance)
    else:
        return default_trigger(daily_buy_total, current_balance)


## General
usd_low_balance_alert = float(config['general']['usd_low_balance_alert'])
threshold_daily_buy = float(config['general']['threshold_daily_buy'])
dcabot_home = config['general']['home_dir']
## BTC-USD
btcusd_daily_buy = float(config['btc-usd']['daily_buy'])

## ETH-USD
ethusd_daily_buy = float(config['eth-usd']['daily_buy'])

## BCH-USD
bchusd_daily_buy = float(config['bch-usd']['daily_buy'])

## Email
email_to = config['email']['email_to']
email_from = config['email']['email_from']
smtp_host = config['email']['smtp_host']
smtp_port = config['email']['smtp_port']

__send_emails = config['email']['send_email_notifications']
if __send_emails.lower() in ['ture', 'yes', '1']:
    send_email_notifications = True
else:
    send_email_notifications = False



logger.debug(f"threshold_daily_buy :{threshold_daily_buy}")
logger.debug(f"dcabot_home :{dcabot_home}")
logger.debug(f"btcusd_daily_buy :{btcusd_daily_buy}")
logger.debug(f"ethusd_daily_buy :{ethusd_daily_buy}")
logger.debug(f"email_to :{email_to}")
logger.debug(f"email_from :{email_from}")
logger.debug(f"send_email_notifications: {send_email_notifications}")
logger.debug(f"usd_low_balance_alert: {usd_low_balance_alert}")

if __name__ == '__main__':
    print()
    print("________DCAbot_Config________")
    if (len(sys.argv) == 1):
        print(f"No conf file specified. Reading default ({DEFAULT_CONFIG_FILEPATH}).")
        config_file = DEFAULT_CONFIG_FILEPATH
    elif (len(sys.argv) > 2):
        print(f"Ignoring extra arguments: {sys.argv[2:]} (argument should be a non-default path to dcabot.conf)")
    else:
        config_file = sys.argv[1]
        print(f"Using {config_file}")
    conf = configparser.ConfigParser()
    conf.read(config_file)
    print("Sections:")
    print(config.sections())
    print()
    print("General settings:")
    for key in config['general']:
        print("{}: {}".format(key, config['general'][key]))
    print()
    print('btc-usd currency pair settings:')
    for key in config['btc-usd']:
        print("{}: {}".format(key, config['btc-usd'][key]))
    print()
    print('eth-usd currency pair settings:')
    for key in config['eth-usd']:
        print("{}: {}".format(key, config['btc-usd'][key]))
    print()
    print("Email settings:")
    for key in config['email']:
        print("{}: {}".format(key, config['email'][key]))
    print()
    print("Logging settings:")
    for key in config['logging']:
        print("{}: {}".format(key, config['logging'][key]))

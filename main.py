#  Copyright (c) 2020. RoguedBear
import argparse
import logging
import requests
import checker
import re
import csv
import json
from datetime import time, datetime, timedelta
from threading import Timer
from time import sleep


# noinspection PyShadowingNames
def alert_onTelegram(message: str):
    """
    This function will send an alert to telegram notifying about the change
    :param message: The message
    :return: None
    """
    try:
        with open('telegram_tokens.json') as tokens:
            data = json.load(tokens)
            CHAT_ID, TOKEN = str(data['chat_id']), str(data['bot_token'])
    except FileNotFoundError:
        CHAT_ID = ''
        TOKEN = ''

    requests.get("https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown"
                                                                                              "&text=" + message)


# noinspection PyShadowingNames
def time_parser(time: str) -> int:
    """
    Converts compound duration time to seconds
    :param time: str of compound time
    :return: int, seconds
    """
    time_search = re.compile(r"(?:(\d+)h)? ?(?:(\d+)m)? ?(?:(\d+)s)?")
    hour, minute, second = time_search.fullmatch(time).groups(default='0')
    return int(hour) * 3600 + int(minute) * 60 + int(second)


def send_uptimealert():
    """
    Sends uptime alert every 24hours
    :return:
    """
    alert_onTelegram("#UptimeStatus, The program is working 🤖👍")


# ==================================================================================
# ------------------------Command line parsers------------------------
parser = argparse.ArgumentParser(description="This program checks from the supplied list of webpages, that if anyone "
                                             "of those have changed and notifies about it.")
parser.add_argument('-w', '--wait', help="The duration for which the program should wait before checking the page "
                                         "again. Defaults to 2 hours. Use compound duration say 2h", metavar='XhYmZ')
parser.add_argument('-c', '--config', help="use the specified file instead of default config.csv", metavar='filename')
parser.add_argument('-d', '--debug', help="Increase logging level of program to debug. AKA increases verbosity of "
                                          "program", action='store_true')
parser.add_argument('-t', '--time', help="time to send a daily alert notifying that the program is working. Enter "
                                         "time in HH:MM 24 hour format.\nOtherwise uses program's default time of "
                                         "14:00 IST", metavar='HH:MM')
args = parser.parse_args()
# ---------------------------------END--------------------------------
# --debug
if args.debug:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(format='%(asctime)s - %(levelname)-8s: "%(name)-20s": %(funcName)16s() - %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S', level=level)
logger = logging.getLogger("PHASE:Startup")

logger.debug("Running logging in DEBUG mode.")

# --config
config_file = 'config.csv'
if args.config:
    logger.info(f"Using custom file: {args.config}")
    config_file = args.config
else:
    logger.info("Using default configuration file")

# --wait
SLEEP_TIME = 7200  # 2 hours
if args.wait:
    SLEEP_TIME = time_parser(args.wait)

logger.info(f"SLEEP_TIME set to {SLEEP_TIME} seconds ({SLEEP_TIME / 3600:.2f} hrs)")

# --time
ALERT_TIME = time(hour=14)

if args.time:
    ALERT_TIME = datetime.strptime(args.time, '%H:%M').time()
logger.info(f"Program will alert the user about program uptime on: {ALERT_TIME.strftime('%I:%M %p')}")

# Sending alert:
alert_onTelegram("Program started. 🤖")
# ==================================================================================

# Reading from csv file.
# For now the csv file has 2 main columns: name (of the website), url
"""Pseudocode:
    * have a master list
    * while reading from csv, create and instantiate the Webpage class object
    * If the file does not exist, create one and exit
"""
# TODO: if the file does not exist, prompt the user to create one from within the program
logger = logging.getLogger("PHASE:Pre-LOOP")
MASTER_WebpageList = []
logger.info("Loading URLs from config file... (Expect some delay)")
try:
    with open(config_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            logger.info(f"Reading \"{row[0]}\".")

            new_class_instance = checker.Webpage(row[0].strip(), row[1].strip())
            try:
                new_class_instance.find_DeltaChange(int(row[2]))
            except (ValueError, IndexError):
                new_class_instance.find_DeltaChange()
            MASTER_WebpageList.append(new_class_instance)
    logger.info(f"Loading complete! Added: {len(MASTER_WebpageList)} elements")
except FileNotFoundError:
    logger.critical("Configuration file does not exists! Creating a default one")
    file = open('config.csv', 'w')
    file.close()

# =======================================

# The loop
logger = logging.getLogger("PHASE:Loop")
sleep(0.5)
for i in range(5, -1, -1):
    print(f"Starting main loop in {i}...", end='\r')
    sleep(1)
    print("                          ", end='\r')
logger.info("Started Main loop...")
target_time = timedelta(hours=ALERT_TIME.hour, minutes=ALERT_TIME.minute)
"""Pseudocode:
    * iterate through MASTER list
    * use the detect
    * if change_detected is True, then notify on telegram
    * check if time is within 20 minutes of ALERT_TIME, then send a message that the program is working
"""
while True:
    # iterating through master list
    for webpage in MASTER_WebpageList:
        # use the detect
        change_detected, output = webpage.detect(1)

        # If change is detected
        if change_detected:
            message = f"""A change on *{webpage.get_name()}* has been detected.\n\nHere is the change:\n`{output}`"""
            alert_onTelegram(message)

    # Checking every 2hours if the alert_time is near.
    current_time = datetime.now()
    current_time = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
    duration = target_time - current_time
    if duration.seconds <= SLEEP_TIME:  # Means the alert time is well within 2hr range
        logger.debug(
            f"Starting UptimeThread with wait duration of: {duration.seconds / 3600:.02f} hours or {duration.seconds / 60:.02f} minutes")
        Timer(duration.seconds, send_uptimealert).start()

    sleep(SLEEP_TIME)

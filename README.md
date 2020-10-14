# Website Change Detector 🌐 
 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
 
> A self-hosted program, which detects when a website's contents are updated (a website has changed) and notifies you about it.

## How to Use:

 1. Save the websites you want to check in the csv file `config.csv` as:
    ```
     1 | <<webpage 1 name>>, <<webpage 1 url to check>>
     2 | <<webpage 2 name>>, <<webpage 2 url to check>>
    ``` 
    Note that you do not need to write any "csv headings". just directly follow this format.
 
 2. Run [main.py](main.py) (`python3 main.py`). \
   By default program will with default settings. You can configure some of them, by passing them as command line arguments. \
   Snip of `python3 main.py -h` or `python3 main.py --help`:
    ```
    usage: main.py [-h] [-w XhYmZ] [-c filename] [-d] [-t HH:MM]
    
    This program checks from the supplied list of webpages, that if anyone of
    those have changed and notifies about it.
    
    optional arguments:
      -h, --help            show this help message and exit
      -w XhYmZ, --wait XhYmZ
                            The duration for which the program should wait before
                            checking the page again. Defaults to 2 hours. Use
                            compound duration say 2h
      -c filename, --config filename
                            use the specified file instead of default config.csv
      -d, --debug           Increase logging level of program to debug. AKA
                            increases verbosity of program
      -t HH:MM, --time HH:MM
                            time to send a daily alert notifying that the program
                            is working. Enter time in HH:MM 24 hour format.
                            Otherwise uses program's default time of 14:00 IST
    ```
   3. Changes will be notified by Telegram ![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/16px-Telegram_logo.svg.png). \
   You need to create your own bot, and enter your own bot `TOKEN` and your `CHAT_ID` on line 20 and 21 in [main.py](main.py) in the function `alert_onTelegram()`
## ToDo:

 - [ ] Ability to add more websites to the list without stopping the program.
 - [ ] Check for constant changes ( aka ∆change ) daily. <br>
       some websites have messed up code changing daily, which needs to be "_intelligently_" identified if the change is some daily-occurring change (such as day/date) or an actual change.
 - [ ] Generate the before and after screenshots (much like how Visualping does).

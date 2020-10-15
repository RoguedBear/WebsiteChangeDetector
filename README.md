# Website Change Detector 🌐 
 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
 
> A self-hosted program, which detects when a website's contents are updated (a website has changed) and notifies you about it.

Not many services exist (that I can find of) which notify you about changes in websites that you might want to track. 
Some do, but they're either paid or limited in how many websites you can track. \
All this could be overcome for free, if you have some programming background **and time**.

I created this Change Detector, to batch check the websites which are on my monitoring list which I can run on my own server, or on the cloud and works according to how I want.
I am aiming for this project to have the same features as offered by other paid services by using the power of Open-Source Community. And Time.


GPL License will guarantee that derivatives of this project remain open-sourced 
## How to Use:

 1. Save the websites you want to check in the csv file `config.csv` as: \
  (4 columns used as of latest commit)
    ```
     1 | <<webpage 1 name>>, <<webpage 1 url to check>>, <<OPTIONAL timeout for finding delta change>>, <<OPTIONAL: True/False whether to verify SSL or not; default value in program is True>>
     2 | <<webpage 2 name>>, <<webpage 2 url to check>>, <<OPTIONAL timeout for finding delta change>>, <<OPTIONAL: True/False whether to verify SSL or not; default value in program is True>>
    ``` 
    - Note that you do not need to write any "csv headings". just directly follow this format.
    - If you get SSLError, then you must write `false` in the 4th column for the respective webpage.
 
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
   You need to create your own bot, and enter your own bot `TOKEN` and your `CHAT_ID` either on line 26 and 27 in [main.py](main.py) in the function `alert_onTelegram()` or create a file same as [telegram_tokens.json](telegram_tokens.json) and enter your `CHAT_ID` and `TOKEN` in either `str` or `int` there.
## How it works:
_To be written..._ (For the time being, currently the program calls bash's `diff` command to check for changes)
## ToDo:

 - [x] Have a better Logging format.
 - [ ] Skipping the webpage when any critical error/exception is encountered instead of stopping the execution of program.
 - [ ] Ability to add more websites to the list without stopping the program.
 - [ ] ~~Check for constant changes ( aka ∆change ) daily. <br>
       some websites have messed up code changing daily, which needs to be "_intelligently_" identified if the change is some daily-occurring change (such as day/date) or an actual change.~~ \
       much better way would be to reply back to the bot about the False Positive, and the bot will then add it to list_ofDeltaChange
 - [ ] Generate the before and after screenshots (much like how Visualping does).
 - [ ] Give a better name to the project?

---
#### Feel free to find and open issues or contribute in this project if you can!

---

#  Copyright (c) 2020. RoguedBear
import logging
import os
import re
from time import sleep
from typing import Tuple
import datetime
import requests


class Webpage:
    """
    The webpage class object which will have all the methods related to checking changes
    name: str, name of website
    url: str

    -----------
    Methods:
     #Getters:
      - get_name()       : returns the name of the website
      - get_url()        : returns the url of the website
      - get_webpage()    : downloads the webpage from the internet and returns as string
      - get_filename()   : returns the appropriate filename
      - get_deltaChange(): returns the list containing deltachange

    #Setter:
      - set_deltaChange() : stores the list of changes

    #Other Functions:
      - save_html(): saves the html code to a unique file
      - load_html(): loads the html code to a string in a variable
      - detect()   : the method used in main, which'll select the appropriate way to detect changes.

    #Detectors:
      - find_DeltaChange(): Finds the constant change that'll be present between a webpage's 2 html file
      - method1_diff()    : Method 1 for detecting change in website. Uses bash's `diff` command.
    """

    def __init__(self, name, url, verifySSL=True):
        self.sleep_time = 0.5
        self.name = name
        self.url = format_url(url)
        self.verifySSL = verifySSL
        self.filename = {'old': f'{self.name}_old.html', 'new': f'{self.name}_new.html'}
        self.deltaChange = []
        self.logger = logging.getLogger(name)
        self.logger.debug(f"Created Class Webpage: {name}")

    # =========================================
    ## Getters
    def get_name(self) -> str:
        """
        Returns the webpage's name
        output: string
        """
        return self.name

    def get_url(self) -> str:
        """
        Returns the webpage's url
        output: string url
        """
        return self.url

    def get_webpage(self) -> str:
        """
        Downloads the webpage from the internet and returns the html string.
        Also saves the webpage in code variable.
        output: str
        """
        while True:
            try:  # if electricity goes out, and internet is not available for the time
                html_page = requests.get(self.get_url(), verify=self.verifySSL).text
            except ConnectionError:
                self.logger.critical("ConnectionError! Internet or Electricity has probably gone out for a while. "
                                     "Retrying in 1minute...")
                sleep(60)
                continue

            if len(html_page) == 0:
                self.logger.warning(f" received webpage for \"{self.get_name()}\" of size 0! Retrying... ")
            else:
                self.logger.debug(f"successfully downloaded {self.get_name()}'s webpage.")
                break
        # Not required for method 1
        # self.code = html_page
        # noinspection PyUnboundLocalVariable
        return html_page

    def get_filename(self, filetype) -> str:
        """
        Returns the predefined filename of the Webpage
        > Save/load is supposed to flexibly save/load files from any suffix name. Therefore no need to assert

        :param filetype: old/new filename
        :return:
        """
        try:
            assert filetype in ['old', 'new'], "filetype variable is not 'old' or 'new'!\nfiletype: " + str(filetype)
            return self.filename[filetype]
        # TODO: do something about this:
        except AssertionError:
            return filetype

    def get_deltaChange(self) -> list:
        """
        Returns the list of changes stored
        :return: list
        """
        return self.deltaChange

    """ Not required for Method 1
    def get_code(self):
        '''
        Return the html code of the webpage
        :return: str 
        '''
    """

    # ==========================================
    ## Setters
    def set_deltaChange(self, list_of_changes: list):
        """
        Takes in the set of changes, and stores them
        :param list_of_changes: list
        :return: None
        """
        self.deltaChange = list_of_changes

    # ==========================================
    ## Other Functions

    def save_html(self, save_as: str, code: str = None) -> None:
        """
        Save's the html code with the file name <name>_old.html
        > Save/load is supposed to flexibly save/load files from any suffix name. Therefore no need to assert
        :param code: str, html code
        :param save_as: str, [old or new  values only] the extension with which to save file
        :return: None
        """
        if code is None:
            code = self.get_webpage()
        file_name = self.get_filename(save_as)
        file = open(file_name, 'w')
        file.write(code)
        file.close()
        sleep(self.sleep_time)
        self.logger.debug(f"Saved html file as: {file_name}")

    def load_html(self, old_new) -> str:
        """
        Loads the html code from the file
        :param old_new: [old/new] html code
        :return: str, html code
        """
        try:
            file_name = self.get_filename(old_new)
            file = open(file_name, 'r')
            data = file.readlines()
            file.close()
            sleep(self.sleep_time)
            self.logger.debug(f"Successfully opened {file_name}")
            return ''.join(data)
        except FileNotFoundError:
            self.logger.warning("File for " + self.get_name() + " does not exists!")
            return ''

    # ==========================================
    ## Detectors

    def find_DeltaChange(self, WAIT_TIME=5, debug=False) -> None:
        """
        Identifies the constant change that'll exist between 2 downloaded versions of the website
        :param debug:
        :param WAIT_TIME: defaults to 5s. the time to wait before downloading the next page
        :return:  None. internally stores the changes

        # Pseudocode:
        * download (and save) the first file
        * download (and save) the second file after WAIT_TIME seconds
        * use the diff command and store the output
        * parse the output
        * find the text that matches in both the files.
        * store as delta_change
        """
        # Since this function is meant to be run at the start, this function will download and manage the copies in
        # _old and _new html files

        # Downloading the webpages
        if debug is False:
            self.save_html('old')
            sleep(WAIT_TIME)
            self.save_html('new')

        # Getting the diff command output
        diff_output = os.popen(f"diff {self.get_filename('old')} {self.get_filename('new')}").read()
        diff_output = diff_output.replace(r'\/', '/')

        # Filtering the output
        filtered_diff_output = filter_DiffOutput(diff_output)

        # Finding the same elements
        same_elements = []
        for code_tuples in filtered_diff_output:
            same_elements.append(find_SameElements(code_tuples[0], code_tuples[1]))
        self.set_deltaChange(same_elements)

        if not same_elements:
            self.logger.debug(f"'{self.get_name()}': No deltaChange found")
        else:
            self.logger.debug(f"'{self.get_name()}': DeltaChange found ({len(same_elements)})")

    def method1_diff(self) -> Tuple[bool, str]:
        """
        This function uses bash's `diff` command to detect change in a website's HTML.
        Will return True/False value and optionally diff command's output
        :return: tuple(bool, str)

        # Pseudocode:
        * Check if the files exist, raise error and/or skip otherwise
        * Generate the -I arguments
        * send the diff command
        * if the diff's output is '' then nothing changed
        * otherwise, return the output as well
        """

        # Generating -I args
        # TODO: save this command line argument as instance variable and use that to save potentially some CPU usage.
        deltachange = self.get_deltaChange()
        args = '-I \'' + "' -I '".join(deltachange) + "'" if deltachange else ''
        command = rf"""diff -EZBb {args} {self.get_filename('old')} {self.get_filename('new')}"""

        self.logger.debug(f"sending command:\n{command}\n")
        # Sending the command

        output = os.popen(command).read()
        #breakpoint()
        # Checking the output of diff
        # TODO: using beautiful soup, strip the tags and send the strings as output to be sent as alert
        if output != '':
            self.logger.info("Change has been DETECTED!")
            return True, output
        else:
            self.logger.debug("No change was found")
            return False, ''

    def detect(self, method: int, debug=False) -> Tuple[bool, str]:
        """
        This method will be used by main.
        :param debug: if debug, then store the old html file when change is detected
        :param method: the method to use to detect changes.
        (PS: planned some more ways to detect changes using BeautifulSoup and maybe difflib)
        :return: Tuple(bool, str)
        """
        try:
            assert method in [1]
        except AssertionError:
            self.logger.critical("method argument not in range! Cannot detect changes for this webpage until "
                                 f"then.\nGiven 'method' argument: {method}")

        # Downloading the new file
        new_code = self.get_webpage()
        self.save_html('new', new_code)

        # USing one of the detection methods
        if method == 1:
            change_detected, output = self.method1_diff()

        # If debug then save the file with current date.
        # noinspection PyUnboundLocalVariable
        if change_detected and debug:
            now = datetime.datetime.now()
            webpage_old = self.load_html('old')
            self.save_html(f"{self.get_name()}{datetime.datetime.strftime(now, '_%d-%m-%y_%H:%M')}"
                           "_old.html", webpage_old)
            webpage_new = self.load_html('new')
            self.save_html(f"{self.get_name()}{datetime.datetime.strftime(now, '_%d-%m-%y_%H:%M')}"
                           "_new.html", webpage_new)
            # noinspection PyUnboundLocalVariable
            self.logger.debug(f"\n\n{output}")

        # After the checks are complete, move the _new.html file to as _old.html
        old_code = self.load_html('new')
        self.save_html('old', old_code)

        # Finally return the output
        # noinspection PyUnboundLocalVariable
        return change_detected, output


def format_url(url):
    """
    formats the url with https
    :param url: str
    :return: str
    """
    if url == '':
        raise Exception('EmptyURLProvided - Check the configuration file')
    if url[0:8] != 'https://' and url[0:7] != 'http://':
        url = 'https://' + url
    return url


def filter_DiffOutput(output):
    """
    Filters the output received from bash's diff command
    Aiming to get mos of the text.
    :param output: the output received from diff command
    :return: list, a list of both code files. eg: [(code1, code2), (code1, code2)]
    """
    line_regex = re.compile(r'^\d+c\d+|\n\d+c\d+')  # Regex to match 634c634 stuff to split the output
    strip_punc = ' <>\n\t!@#$%^&*()\\[]{};:\'""?/`~=+-_'
    changes = line_regex.split(output)[1:]  # since 0th element is ''
    changes = [tuple(i.split('\n---\n')) for i in changes]
    changes = [(i.strip(strip_punc), j.strip(strip_punc)) for i, j in changes]
    return changes
    # return [i.strip(strip_punc) for i in output[output.find('\n'):].split('\n---\n')]


def find_SameElements(code1, code2) -> str:
    """
    Finds the same elements between two diff comparisons
    :param code1: str, The first code
    :param code2: str, The second code
    :return: str, the common html
    """
    same = ''
    for i, j in zip(code1, code2):
        if i == j and i.isnumeric() is False and i not in ['\\', '/']:
            same += i
        else:
            break
    return same


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s: %(funcName)16s() : "%(name)16.15s" - %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.DEBUG)

    test = Webpage('Ubi', 'free.ubisoft.com')
    print(test.load_html('old'))

    # testing find_DeltaChange
    test2 = Webpage('local', '127.0.0.1')
    test2.find_DeltaChange(debug=True)
    print(test2.get_deltaChange())

    test3 = Webpage('1', '127.0.0.1')
    print(test3.get_url())
    test3.find_DeltaChange(debug=True)
    print(test3.get_deltaChange())
    
    # Testing method1_diff
    print('--------------')
    test_method1 = Webpage('1', 'localhost')
    test_method1.find_DeltaChange(debug=True)
    print(test_method1.method1_diff())

    test2_method1 = Webpage('local', 'localhost')
    print("url:" + test2_method1.get_url())
    test2_method1.find_DeltaChange(debug=True)
    print(test2_method1.method1_diff())
    test2_method1.detect(3)

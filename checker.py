#  Copyright (c) 2020. RoguedBear
import requests
import logging
import re
from time import sleep

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(funcName)10s() - %(message)s', datefmt='%d/%m/%y %H:%M:%S',
                    level=logging.INFO)


class Webpage:
    """
    The webpage class object which will have all the methods related to checking changes
    name: str, name of website
    url: str

    -----------
    Methods:
     #Getters:
      - get_name()   : returns the name of the website
      - get_url()    : returns the url of the website
      - get_webpage(): downloads the webpage from the internet and returns as string

     #Other Functions:
      - save_html(): saves the html code to a unique file
      - load_html(): loads the html code to a string in a variable
    """

    def __init__(self, name, url):
        self.name = name
        self.url = format_url(url)
        logging.debug(f"Created Class Webpage: {name}")

    # =========================================
    ## Getters
    def get_name(self):
        """
        Returns the webpage's name
        output: string
        """
        return self.name

    def get_url(self):
        """
        Returns the webpage's url
        output: string url
        """
        return self.url

    def get_webpage(self):
        """
        Downloads the webpage from the internet and returns the html string.
        Also saves the webpage in code variable.
        output: str
        """
        html_page = requests.get(self.get_url()).text
        # Not required for method 1
        # self.code = html_page
        return html_page

    """ Not required for Method 1
    def get_code(self):
        '''
        Return the html code of the webpage
        :return: str 
        '''
    """

    # ==========================================
    ## Other Functions

    def save_html(self, save_as, code=None) -> None:
        """
        Save's the html code with the file name <name>_old.html
        :param code: str, html code
        :param save_as: str, [old or new  values only] the extension with which to save file
        :return: None
        """
        assert save_as in ['old', 'new'], f"type is incorrectly specified!\nExpected: old/new  Got: {save_as}"
        if code is None:
            code = self.get_webpage()
        file_name = f"{self.get_name()}_{save_as}.html"
        file = open(file_name, 'w')
        file.write(code)
        file.close()
        logging.debug(f"Saved html file as: {file_name} for class {self.get_name()}")

    def load_html(self, old_new):
        """
        Loads the html code from the file
        :param old_new: [old/new] html code
        :return: str, html code
        """
        try:
            file_name = f"{self.get_name()}_{old_new}.html"
            file = open(file_name, 'r')
            logging.debug(f"Successfully opened {file_name}")
            return ''.join(file.readlines())
        except FileNotFoundError:
            logging.warning("File for " + self.get_name() + " does not exists!")
            return ''

    # ==========================================
    ## Detectors

    def find_DeltaChange(self, WAIT_TIME=5):
        """
        Identifies the constant change that'll exist between 2 downloaded versions of the website
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
        self.save_html('old')
        sleep(WAIT_TIME)
        self.save_html('new')


def format_url(url):
    """
    formats the url with https
    :param url: str
    :return: str
    """
    if url[0:8] != 'https://' or url[0:7] != 'http://':
        url = 'https://' + url
    return url


def filter_DiffOutput(output):
    """
    Filters the output received from bash's diff command
    Aiming to get mos of the text.
    :param output: the output received from diff command
    :return: list, a list of both code files. eg: [(code1, code2), (code1, code2)]
    """
    line_regex = re.compile(r'^\d+c\d+|\n\d+c\d+') # Regex to match 634c634 stuff to split the output
    strip_punc = ' <>\n\t!@#$%^&*()\\[]{};:\'""?/`~=+-_'
    changes = line_regex.split(output)[1:] # since 0th element is ''
    changes = [tuple(i.split('\n---\n')) for i in changes]
    changes = [(i.strip(strip_punc), j.strip(strip_punc)) for i,j in changes]
    return changes
    #return [i.strip(strip_punc) for i in output[output.find('\n'):].split('\n---\n')]


def find_SameElements(code1, code2):
    """
    Finds the same elements between two diff comparisons
    :param code1: str, The first code
    :param code2: str, The second code
    :return: str, the common html
    """
    pass


if __name__ == '__main__':
    test = Webpage('Ubi', 'free.ubisoft.com')
    print(test.load_html('old'))

#  Copyright (c) 2020. RoguedBear
import requests


class Webpage:
    """
    The webpage class object which will have all the methods related to checking changes
    name: str, name of website
    url: str, in the format: 'https://...'
    """

    def __init__(self, name, url):
        self.name = name
        self.url = format_url(url)

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
        Downloads the webpage from the internet and returns the html string
        output: str
        """
        return requests.get(self.get_url()).text


def format_url(url):
    """
    formats the url with https
    :param url: str
    :return: str
    """
    if url[0:8] != 'https://' or url[0:7] != 'http://':
        url = 'https://' + url
    return url

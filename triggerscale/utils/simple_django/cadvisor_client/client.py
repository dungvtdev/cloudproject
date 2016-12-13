# from string import Formatter as fmt
import requests, json
from requests.exceptions import *


class Client(object):
    def __init__(self, guest=None):
        """
        :param guest: Guest object cho biet may ao dc theo doi
        """
        self.guest = guest

    def verify_guest(self):
        url = self.get_machine_info_url()
        try:
            requests.get(url)
            return True
        except ConnectionError as e:
            return False


    def get_machine_info_url(self):
        return self.guest.get_base_url() + "/machine"


    def machineInfo(self):
        url = self.get_machine_info_url()
        response = requests.get(url)
        return response



class Guest(object):
    url = ""
    version = "v1.3"

    def __init__(self, url="localhost", version="1.3"):
        self.url = url
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        self.version = version
        if not self.version.startswith('v'):
            self.version = 'v'+self.version

    def get_base_url(self):
        return "http://"+self.url+"/api/"+self.version


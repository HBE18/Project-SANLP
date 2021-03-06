from .API import API
from .Haberturk import Haberturk
from .Sabah import Sabah
from .Twitter import Twitter
from .Sozcu import Sozcu
from .YouTube import YouTube
from .Milliyet import Milliyet
from .Hurriyet import Hurriyet
from .Posta import Posta
from json import load
from os import getcwd

class Connector:
    __currentApi = None
    __currentApiName = ""
    socialMediaList = [
        "Twitter",
        "YouTube"
    ]
    newsList = [
        "Hurriyet", #broken
        "Sabah", #broken
        "Haberturk", #broken
        "Sozcu", #it seems working
        "Milliyet", #broken
        "Posta" #it seems NOT working
    ]

    def __init__(self):
        cwd = getcwd()
        if cwd.endswith("DataMining"):
            fp = open("keys.json", "r")
        else:
            fp = open("./DataMining/keys.json", "r")
        keys = load(fp)
        fp.close()
        self.allApis = {
            "Social Media": {
                "Twitter": Twitter(keys["Twitter"]["Bearer Token"]),
                "YouTube": YouTube()
            },

            "News": {
                "Hurriyet": Hurriyet(),
                "Sabah": Sabah(),
                "Haberturk": Haberturk(),
                "Sozcu": Sozcu(),
                "Milliyet": Milliyet(),
                "Posta": Posta()
            }
        }

    def _getApiName(self) -> str:
        return self.__currentApiName

    def _getCurrentApi(self) -> object:
        return self.__currentApi

    def connectToApi(self,apiName="") -> None:
        """
        The function takes apiName as a string parameter and connects the API (given in the parameters).

        ``apiName`` is the string which is includes API's name.

        Example Usage:

        >>> connectToApi("Twitter")
        """
        if apiName == "":
            self.__currentApi = API("Default")
        elif apiName in self.socialMediaList:
            self.__currentApi = self.allApis["Social Media"][apiName]
        elif apiName in self.newsList:
            self.__currentApi = self.allApis["News"][apiName]
        else:
            raise (Exception("Wrong apiName sended to the connectToApi() function"))

        self.__currentApiName = apiName
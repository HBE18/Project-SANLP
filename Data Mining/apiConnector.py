from API import API
from Twitter import Twitter
from YouTube import YouTube
from Facebook import Facebook
from Linkedin import Linkedin
from json import load
from os import getcwd

__currentApi = None

def _getCurrentApi() -> object:
    return __currentApi


def connectToApi(apiName = "") -> None:
    """
    The function takes apiName as a string parameter and connects the API (given in the parameters).

    ``apiName`` is the string which is includes API's name.

    Example Usage:

    >>> connectToApi("Twitter")
    """
    
    global __currentApi
    cwd = getcwd()
    if cwd.endswith("Data Mining"):
        fp = open("keys.json","r")
    else:
        fp = open("./Data Mining/keys.json","r")
    keys = load(fp)
    fp.close()
    if apiName == "":
        __currentApi = API("Default")
    elif apiName == "Twitter":
        __currentApi = Twitter(keys[apiName]["Bearer Token"])
    elif apiName == "YouTube":
        __currentApi = YouTube()
    elif apiName == "Facebook":
        __currentApi = Facebook()
    elif apiName == "Linkedin":
        __currentApi = Linkedin()
    else:
        raise(Exception("Wrong apiName sended to the connectToApi() function"))
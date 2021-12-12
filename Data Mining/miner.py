from json import load
from requests import get
import os
from searchtweets import gen_request_parameters, load_credentials, collect_results, ResultStream
from searchtweets.result_stream import request

__API_NAME_LIST = [
    "Twitter",
    "Facebook",
    "Instagram",
    "Youtube",
    "Linkedin"
]

__currentApi = None

class API:
    def __init__(self,name) -> None:
        self.name = name

    def connect(self) -> str:
        return get("www" + self.name + ".com").content.decode()

    def searchKeyword(self, keyword = "", itemSize = 10) -> dict:
        return dict()

class __Tweet:
    def __init__(self,text = "") -> None:
        if text.startswith("RT @"):
            for ind in range(len(text)):
                if text[ind] == ":":
                    break
            ind += 2
            self.tweet = text[ind:]
        else:
            self.tweet = text
    
    def __str__(self) -> str:
        return self.tweet

class Twitter(API):
    def __init__(self,search_args) -> None:
        super().__init__("twitter")
        global __currentApi
        __currentApi = self
        self.searchArgs = search_args
    
    def searchKeyword(self,keyword = "", itemSize = 10) -> list:
        query = gen_request_parameters(keyword, results_per_call = itemSize, granularity= None)
        
        tws = collect_results(query, max_tweets = itemSize, result_stream_args = self.searchArgs)

        tws = tws[0]
        tws = tws["data"]
        results = []
        for tweet in tws:
            results.append(str(__Tweet(tweet["text"])))

        return results

def connectToApi(apiName = ""):
    cwd = os.getcwd()
    if cwd.endswith("Data Mining"):
        fp = open("keys.json","r")
    else:
        fp = open("./Data Mining/keys.json","r")
    keys = load(fp)
    fp.close()
    if apiName == "":
        return API("")
    elif apiName == "Twitter":
        os.environ["SEARCHTWEETS_ENDPOINT"] = "https://api.twitter.com/2/tweets/search/recent"
        os.environ["SEARCHTWEETS_BEARER_TOKEN"] = keys[apiName]["Bearer Token"]
        os.environ["SEARCHTWEETS_CONSUMER_KEY"] = keys[apiName]["API Key"]
        os.environ["SEARCHTWEETS_CONSUMER_SECRET"] = keys[apiName]["API Key Secret"]

        cred = load_credentials("","")
        return Twitter(cred)
        # headers = {'Authorization': f'Bearer {keys[apiName]["Bearer Token"]}'}
        # get(f"https://api.twitter.com/2/tweets/search/recent?query=Elon%20Musk&max_results=10",headers=headers).content.decode()

api = connectToApi("Twitter")
res = api.searchKeyword("Elon Musk")
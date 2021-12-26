from API import API
from requests import get

class _Twitter__Tweet:
    def __init__(self, text="") -> None:
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
    def __init__(self, search_args) -> None:
        super().__init__("twitter")
        self.searchArgs = search_args

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        results = []
        takenNumOfResult = 0
        oldest = None
        nextToken = None
        headers = {'Authorization': f'Bearer {self.searchArgs}'}
        while takenNumOfResult < itemSize:
            tws = self.__getResults(keyword, itemSize, headers, nextToken, oldest)
            meta = tws["meta"]
            data = tws["data"]
            takenNumOfResult += int(meta["result_count"])
            nextToken = meta["next_token"] if "next_token" in meta.keys() else None
            oldest = meta["oldest_id"]
            for tweet in data:
                tw = str(_Twitter__Tweet(tweet["text"]))
                for result in results:
                    if tw.startswith(result[:len(result) - 5]) and result.endswith("...") and len(tw) > len(result):
                        results.remove(result)
                        results.append(tw)
                if tw not in results:
                    results.append(tw)

        return results

    def __getResults(self, keyword, itemSize, headers, next_token=None, until_id=None):
        if next_token == None:
            string = f"https://api.twitter.com/2/tweets/search/recent?query={self.createQuery(keyword)}&max_results={itemSize if itemSize <= 100 else 100}"
        else:
            string = f"https://api.twitter.com/2/tweets/search/recent?query={self.createQuery(keyword)}&max_results={itemSize if itemSize <= 100 else 100}&next_token={next_token}&until_id={until_id}"

        return get(string, headers=headers).json()

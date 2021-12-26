from requests import get

class API:
    def __init__(self, name) -> None:
        self.name = name

    def connect(self) -> str:
        return get("www" + self.name + ".com").content.decode()

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        return list()

    def createQuery(self, string) -> str:
        if " " in string:
            st = string.split(" ")
            string = ""
            for s in st:
                string += s + ("" if (st[::-1])[0] == s else "%20")
        return string
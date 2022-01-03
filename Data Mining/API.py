from requests import get
from selenium.webdriver import Firefox
from os import getcwd
from time import sleep


class API:
    def __init__(self, name) -> None:
        self.name = name

    def openBrowser(self):
        cwd = getcwd()
        if cwd.endswith("Data Mining"):
            self.browser = Firefox(executable_path="geckodriver.exe")
        else:
            self.browser = Firefox(executable_path="./Data Mining/geckodriver.exe")

    def closeBrowser(self):
        self.browser.close()

    def infiniteScroll(self,pauseTime:float):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(pauseTime)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scroll(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

    def makeQuery(self, keyword =""):
        turToEng = {
            "ç": "c",
            "ı": "i",
            "ö": "o",
            "ş": "s",
            "ü": "u"
        }
        keyword = keyword.lower()
        value = ""
        for que in keyword:
            if que in turToEng.keys():
                value += turToEng[que]
            elif que == " ":
                value += "-"
            else:
                value += que
        return value
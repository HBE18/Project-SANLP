from time import sleep

import bs4
from requests import get

from API import API
from pytube import Search
from xml.etree import ElementTree as eT
from selenium.webdriver import Firefox
from os import getcwd


class YouTube(API):
    def __init__(self) -> None:
        super().__init__("YouTube")
        # cwd = getcwd()
        # if cwd.endswith("Data Mining"):
        #     self.browser = Firefox(executable_path="geckodriver.exe")
        # else:
        #     self.browser = Firefox(executable_path="./Data Mining/geckodriver.exe")

    def closeBrowser(self):
        self.browser.close()

    def searchKeyword(self, keyword="", itemSize=9, numberOfComments=0) -> dict:
        ind = 0
        videos = []
        while ind < itemSize:
            search = Search(keyword)
            for res in search.results:
                videos.append(res)
            ind = len(videos)
        if ind > itemSize:
            videos = videos[:itemSize]
        results = {}
        captRes = []
        results["Content"] = captRes
        commS = []
        results["Comments"] = commS
        allComments = []
        while len(allComments) < numberOfComments:
            for yt in videos:
                id = yt.vid_info["videoDetails"]["videoId"]
                try:
                    caption = yt.captions["tr"]
                except:
                    caption = yt.captions["a.tr"]

                comments = self.__getComments(id,numberOfComments)
                allComments.extend(comments)
                sentList = self.xmlToSentenceList(caption.xml_captions)
                captRes.append(sentList.copy())
        if len(allComments) > numberOfComments:
            allComments = allComments[:numberOfComments]
        commS.append(allComments.copy())
        return results

    def xmlToSentenceList(self, xml: str) -> list:
        root = eT.fromstring(xml)
        body = root[1]
        sentenceList = []
        sentence = ""
        for p in body.findall("p"):
            for string in p.findall("s"):
                sentence += string.text + " "
            sentence2 = ""
            for index in range(len(sentence)):
                if index + 1 != len(sentence):
                    sentence2 += sentence[index]
                else:
                    sentence2 += "."
            sentenceList.append(sentence2)
        return sentenceList

    def __getComments(self, id, numberOfComments) -> list:
        url = f"https://www.youtube.com/watch?v={id}"
        # self.browser.get(url)
        # sleep(1)
        # commentsTurnedOff = True if "Comments are turned off. " in [com.text for com in self.browser.find_elements_by_class_name("style-scope.yt-formatted-string")] else False
        # if commentsTurnedOff:
        #     return []
        #
        # comments = self.browser.find_elements_by_class_name("style-scope.ytd-comment-renderer")

        data = get(url).content  # example XhFtHW4YB7M
        soup = bs4.BeautifulSoup(data,"html.parser")
        cmnts = soup.findAll(attrs={'class': 'style-scope.ytd-comment-renderer'})

        for i in cmnts:
            print(i.text)
        return cmnts
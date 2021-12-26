from time import sleep
from API import API
from pytube import Search
from xml.etree import ElementTree as eT
from selenium.webdriver import Firefox
from os import getcwd


class YouTube(API):
    def __init__(self) -> None:
        super().__init__("YouTube")
        cwd = getcwd()
        if cwd.endswith("Data Mining"):
            self.browser = Firefox(executable_path="geckodriver.exe")
        else:
            self.browser = Firefox(executable_path="./Data Mining/geckodriver.exe")

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

        results = {}
        captRes = []
        results["Content"] = captRes
        commS = []
        results["Comments"] = commS
        allComments = []
        allCaptions = []
        while len(allComments) * len(allCaptions) != itemSize * numberOfComments:
            for yt in videos:
                id = yt.vid_info["videoDetails"]["videoId"]
                try:
                    caption = yt.captions["tr"]
                except KeyError:
                    try:
                        caption = yt.captions["a.tr"]
                    except KeyError:
                        continue

                comments = self.__getComments(id)
                allComments.append(comments.copy())
                sentList = self.xmlToSentenceList(caption.xml_captions)
                sentList = sentList[::-1]
                allCaptions.append(sentList[0])
                if len(allCaptions) >= itemSize:
                    break
        if len(allCaptions) > itemSize:
            allCaptions = allCaptions[:itemSize]
        if len(allComments) > itemSize:
            allComments = allComments[:itemSize]
            for ind in range(len(allComments)):
                if len(allComments[ind]) > numberOfComments:
                    allComments[ind] = allComments[ind][:numberOfComments]
        commS.append(allComments)
        captRes.append(allCaptions.copy())
        return results

    def xmlToSentenceList(self, xml: str) -> list:
        sentenceList = []
        sentence = ""
        try:
            root = eT.fromstring(xml)
            body = root[1]
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
        except IndexError:
            root = eT.fromstring(xml)
            body = root.find("body")
            for p in body.findall("p"):
                sentence += p.text + " "
                sentence2 = ""
                for index in range(len(sentence)):
                    if index + 1 != len(sentence):
                        sentence2 += sentence[index]
                    else:
                        sentence2 += "."
                sentenceList.append(sentence2)
        return sentenceList

    def __getComments(self, id:str) -> list:
        url = f"https://www.youtube.com/watch?v={id}"
        self.browser.get(url)
        sleep(5)
        commentsTurnedOff = True if "Comments are turned off. " in [com.text for com in
                                                                    self.browser.find_elements_by_class_name(
                                                                        "style-scope.yt-formatted-string")] else False
        if commentsTurnedOff:
            print("Turned off")
        else:
            self.__infiniteScroll(5)
            commentsS = self.browser.find_elements_by_css_selector(
                "ytd-comment-thread-renderer.style-scope > ytd-comment-renderer:nth-child(1) > div:nth-child(3) > div:nth-child(2) > ytd-expander:nth-child(2) > div:nth-child(1) > yt-formatted-string:nth-child(3)")
            comments = []
            for txt in commentsS:
                spans = txt.find_elements_by_tag_name("span")
                if len(spans) == 0:
                    comments.append(txt.text)
                else:
                    text = ""
                    for span in spans:
                        text += span.text
                    comments.append(text)

            return comments
        return []

    def __infiniteScroll(self,pauseTime:int):
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

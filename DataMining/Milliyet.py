from time import sleep

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

from .API import API
from .News import News

turToEng = {
    "ç": "c",
    "ı": "i",
    "ö": "o",
    "ş": "s",
    "ü": "u"
}


class Milliyet(API):
    def __init__(self):
        super().__init__("Milliyet")

    def makeQuery(self, keyword=""):
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

    def searchKeyword(self, keyword="", itemSize=10, *args) -> list:
        self.openBrowser()
        links = []
        newsWillReturned = []

        url = f"https://www.milliyet.com.tr/haberleri/{self.makeQuery(keyword)}"
        self.browser.get(url)
        sleep(1)

        ##Button click for more news
        self.scroll()
        sleep(0.3)
        otButton = self.browser.find_element(By.ID, "onetrust-accept-btn-handler")
        otButton.click()

        while (True):
            try:
                while self.browser.execute_script("return document.readyState;") != "complete":
                    pass

                self.scroll()
                buttons = self.browser.find_elements(By.TAG_NAME, "button")

                for button in buttons:
                    if button.get_attribute("class") == "news__load-more-button":
                        button.click()
                """
                button = self.browser.find_element(By.CLASS_NAME, "news__load-more-button")
                button.click()
                """
                sleep(2)
            except ElementNotInteractableException:
                break

        openLink = self.browser.find_elements(By.CLASS_NAME, "news__titles-link")

        for newTitle in openLink:
            if len(links) == itemSize:
                break

            links.append(newTitle.get_attribute("href"))

        for link in links:
            if "/milliyet-tv/" in link:
                continue

            self.browser.get(link)
            sleep(0.3)

            title = self.browser.find_element(By.CLASS_NAME, "nd-article__title").text
            spot = self.browser.find_element(By.CLASS_NAME, "nd-article__spot").text
            text = self.browser.find_element(By.CLASS_NAME, "nd-content-column")
            pler = ""

            ps = text.find_elements(By.TAG_NAME, "p")
            for p in ps:
                pler += p.text

            article = spot + "###" + pler
            newsWillReturned.append(News(title, article))

        self.closeBrowser()

        return newsWillReturned
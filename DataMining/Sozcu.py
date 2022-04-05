from time import sleep

from selenium.webdriver.common.by import By

from .API import API
from .News import News


class Sozcu(API):
    def __init__(self):
        super().__init__("Sozcu")

    def searchKeyword(self, keyword="", itemSize=10, *args) -> list:
        self.openBrowser()
        links = []
        newsWillReturned = []
        url = f"https://www.sozcu.com.tr/haberleri/{self.makeQuery(keyword)}/"
        self.browser.get(url)
        self.infiniteScroll(0.3)
        sleep(1)

        try:
            while self.browser.find_element(By.CSS_SELECTOR, ".btn"):
                self.infiniteScroll(0.3)
                self.browser.find_element(By.CSS_SELECTOR, ".btn").click()
                sleep(0.5)
        except:
            print("NMN")

        listNews = self.browser.find_elements(By.CLASS_NAME, "col-6.col-lg-4.news-item._16x9.mb-4")
        for n in listNews:
            if len(links) == itemSize:
                break
            a = n.find_elements(By.CLASS_NAME, "news-item-title")[0]
            if "/sozcutv/" not in a.get_attribute("href"):
                links.append(a.get_attribute("href"))


        for link in links:
            if "/yazarlar/" not in link:
                self.browser.get(link)
                sleep(1)
                articleKutu = self.browser.find_element(By.TAG_NAME, "article")

                title = articleKutu.find_element(By.TAG_NAME, "h1").text

                articleFirstPart = articleKutu.find_element(By.CLASS_NAME, "spot").text
                articleSecondPart = ""
                articleS = articleKutu.find_elements(By.XPATH, ".//*")
                for art in articleS:
                    if art.get_attribute("class") != "spot" and art.tag_name != "h1":
                        if art.tag_name == "p" or art.tag_name == "h2":
                            articleSecondPart += art.text

                article = articleFirstPart + "###" + articleSecondPart
                newsWillReturned.append(News(title, article))
            else:
                self.browser.get(link)
                sleep(1)
                articleKutu = self.browser.find_element(By.TAG_NAME, "article")

                title = articleKutu.find_element(By.TAG_NAME, "h1").text

                articleList = articleKutu.find_elements(By.XPATH, ".//*")
                article = ""
                for art in articleList:
                    if art.tag_name != "div" and art.tag_name != "a" and art.tag_name != "script":
                        article += art.text

                newsWillReturned.append(News(title,article))

        self.closeBrowser()
        return newsWillReturned
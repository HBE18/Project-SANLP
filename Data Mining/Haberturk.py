from API import API
from News import News
from math import ceil
from time import sleep
from selenium.webdriver.common.by import By

class Haberturk(API):
    def __init__(self):
        super().__init__("Haberturk")

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        url = f"https://www.haberturk.com/arama/?tr={self.createQuery(keyword)}&tip=haber&siralama=yeni"

        self.openBrowser()

        self.browser.get(url)

        self.infiniteScroll(1)

        links = []
        newsWillReturned = []

        searchRess = self.browser.find_element(By.ID,"searchResults").find_elements(By.TAG_NAME,"li")

        for searchRes in searchRess:
            if len(links) == itemSize:
                break

            if searchRes.get_attribute("class") == "clearfix.htSearchTwin":
                twins = searchRes.find_elements(By.TAG_NAME,"div")
                for twin in twins:
                    links.append(twin.find_element(By.CSS_SELECTOR,"div > a").get_attribute("href"))
            else:
                links.append(searchRes.find_element(By.TAG_NAME,"a").get_attribute("href"))

        for link in links:
            self.browser.get(link)
            sleep(1)
            self.scroll()
            newsFrame = self.browser.find_element(By.ID,"newsWrapper")
            title = self.browser.find_element(By.TAG_NAME,"title").text
            articleFirstPart = newsFrame.find_element(By.CLASS_NAME,"spot-title").text
            articleSecondCont = newsFrame.find_element(By.CLASS_NAME,"content.type1")
            articleSecondCont = articleSecondCont.find_elements(By.TAG_NAME,"p")
            articleSecondPart = ""
            for artSec in articleSecondCont:
                articleSecondPart += artSec.text
            
            article = articleFirstPart + "###" + articleSecondPart
            newsWillReturned.append(News(title,article))

        for news in newsWillReturned:
            print(f"Title: {news.title}\nArticle: {news.article}\n")


        self.closeBrowser()

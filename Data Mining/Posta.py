from API import API
from News import News
from selenium.webdriver.common.by import By
from time import sleep

class Posta(API):
    def __init__(self):
        super().__init__("Posta")

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        self.openBrowser()
        links = []
        newsWillReturned = []
        url = f"https://www.posta.com.tr/arama?q={keyword}&type=news"
        self.browser.get(url)
        self.infiniteScroll(1)
        for news in self.browser.find_elements(By.CLASS_NAME, "search-results__item"):
            links.append(news.get_attribute("href"))

        for link in links:
            self.browser.get(link)
            sleep(1)
            self.scroll()
            title = self.browser.find_element(By.CLASS_NAME, "news-detail__info__title").text
            articleFirstPart = self.browser.find_element(By.CLASS_NAME, "news-detail__info__spot ").text
            secondPartRaw = self.browser.find_element(By.CLASS_NAME, "news-detail__body__content.clearfix")
            secondPartProcessed = secondPartRaw.find_elements(By.TAG_NAME, "p")
            articleSecondPart = ""
            for spav in secondPartProcessed:
                articleSecondPart += spav.text

            article = articleFirstPart + "###" + articleSecondPart
            newsWillReturned.append(News(title, article))

        self.closeBrowser()
        return newsWillReturned

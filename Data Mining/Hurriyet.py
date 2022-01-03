from API import API
from News import News
from math import ceil
from time import sleep

class Hurriyet(API):
    def __init__(self):
        super().__init__("Hurriyet")

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        pagination = ceil(itemSize/10)
        currentPage = 1
        self.openBrowser()
        links = []
        newsWillReturned = []
        while currentPage <= pagination:
            url = f"https://www.hurriyet.com.tr/arama/#/?page={currentPage}&key={self.createQuery(keyword)}&where=/&how=Article,Column,Recipe&and={self.createQuery(keyword)}&isDetail=true"
            self.browser.get(url)
            sleep(1)
            for news in self.browser.find_elements_by_css_selector("div.col-sm-6:nth-child(n+1)"):
                links.append(news.find_element_by_css_selector("div:nth-child(1) > a:nth-child(1)").get_attribute("href"))
            currentPage += 1

        for link in links:
            self.browser.get(link)
            sleep(1)
            self.scroll()

            if "yerel-haberler" in link:
                title = self.browser.find_element_by_class_name("news-detail-title.selectionShareable.local-news-title").text
                art = self.browser.find_element_by_css_selector("div.clearfix:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
                articleFirstPart = art.find_element_by_tag_name("h2").text
                article = articleFirstPart + "###" + self.browser.find_elements_by_class_name("news-box")[1].text
            elif "yazarlar" in link:
                title = self.browser.find_element_by_xpath("/html/body/article/div[4]/div/section[1]/header/div[2]/div/h1").text
                article = self.browser.find_element_by_xpath("/html/body/article/div[4]/div/section[3]/div/h2").text
            else:
                news = self.browser.find_element_by_xpath("/html/body/div[1]/section[2]/div")
                title = news.find_element_by_tag_name("h1").text
                articleFirstCont = self.browser.find_element_by_class_name("news-content__inf")
                articleFirstPart = articleFirstCont.find_element_by_tag_name("h2").text
                articleSecondPart = news.find_element_by_class_name("news-content").text
                articleSecondPart = articleSecondPart.replace("Haberin Devamı","")

                article = articleFirstPart + "###" + articleSecondPart

            newsWillReturned.append(News(title, article))
        newsWillReturned = newsWillReturned[:itemSize]
        self.closeBrowser()
        for news in newsWillReturned:
            print(f"Title: {news.title}\nArticle: {news.article}")
        return newsWillReturned
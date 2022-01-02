from API import API
from News import News
from math import ceil

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
            url = f"https://www.hurriyet.com.tr/arama/#/?page={currentPage}&key={self.createQuery(keyword)}&where=/&how=Article,Column,NewsPhotoGallery,NewsVideo,Recipe&and={self.createQuery(keyword)}&isDetail=true"
            self.browser.get(url)
            for news in self.browser.find_elements_by_css_selector("div.col-sm-6:nth-child(n+1)"):
                links.append(news.find_element_by_css_selector("div:nth-child(1) > a:nth-child(1)").get_attribute("href"))
            currentPage += 1

        for link in links:
            if link.contains("/video/"):
                continue
            self.browser.get(link)
            self.scroll()
            title = self.browser.find_element_by_xpath("/html/body/div[1]/section[2]/div/h1").text
            articleFirstPart = self.browser.find_element_by_xpath(
                "/html/body/div[1]/section[2]/div/div[3]/div[1]/div[2]/h2").text
            articleSecondPart = self.browser.find_element_by_xpath(
                "/html/body/div[1]/section[2]/div/div[3]/div[1]/div[3]/p").text

            article = articleFirstPart + "###" + articleSecondPart
            newsWillReturned.append(News(title, article))

        return newsWillReturned
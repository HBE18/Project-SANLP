from API import API
from News import News
from math import ceil

class Sabah(API):
    def __init__(self):
        super().__init__("Sabah")

    def searchKeyword(self, keyword="", itemSize=10) -> list:
        self.openBrowser()
        links = []
        newsWillReturned = []
        url = f"https://www.sabah.com.tr/arama?query={self.createQuery(keyword)}&categorytype=haber"
        self.browser.get(url)
        ##This website do not have pagination! Infinite scroll is required
        self.infiniteScroll(1.5)

        ##Getting news links from the search results
        start = 0
        for news in self.browser.find_elements_by_css_selector("#resultList > div:nth-child(n+1) > figure"):
            links.append(news.find_element_by_css_selector("a:nth-child(1)").get_attribute("href"))
            start += 1
            if start == itemSize:
                break

        ##Getting text from related news
        for link in links:
            self.browser.get(link)
            if "/yazarlar/" not in link:
                kutu = self.browser.find_element_by_css_selector("div.col-md-8:nth-child(1)")
                title = kutu.find_element_by_class_name("pageTitle").text
                articleFirstPart = self.browser.find_element_by_css_selector(".spot").text
                articlekutu = kutu.find_element_by_class_name("newsDetailText")
                article2 = articlekutu.find_elements_by_tag_name("p")
                articleSecondPart = ""
                for art in article2:
                    articleSecondPart += art.text
                article = articleFirstPart + "###" + articleSecondPart
                newsWillReturned.append(News(title,article))
            else:
                kutu = self.browser.find_element_by_css_selector("#articleframe > div:nth-child(1) > div")
                title = kutu.find_element_by_class_name("postTitle").text
                title += " - "
                title += kutu.find_element_by_class_name("postCaption").text
                articlekutu = self.browser.find_element_by_css_selector("#articleframe > div:nth-child(1) > div > div.col-md-8.col-sm-12.column-left > div > div:nth-child(2) > div > div")
                articleL = articlekutu.find_elements_by_tag_name("p")
                article = ""
                for art in articleL:
                    if len(art.text) <= 3:
                        continue
                    article += art.text
                    article += "\n"
                newsWillReturned.append(News(title,article))

        self.closeBrowser()
        return newsWillReturned
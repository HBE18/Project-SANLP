class News:
    def __init__(self,title,article):
        self.title = title
        self.article = article

    def __str__(self):
        return f"{self.title}\n\n{self.article.split('###')[0]}\n\n{self.article.split('###')[1]}"
from gensim import utils
from zemberek import TurkishSentenceExtractor, TurkishTokenizer, TurkishMorphology, TurkishSentenceNormalizer

from DataMining.apiConnector import Connector
from DataMining.miner import searchKeyword


class Preprocessor:
    def __init__(self):
        self.__minedData = {}

        with open("stopwords.txt", "r") as file:
            self.stopwordList = file.readlines()

        for i in range(len(self.stopwordList)):
            self.stopwordList[i] = self.stopwordList[i].replace("\n", "")

        self.morphology = TurkishMorphology.create_with_defaults()
        self.normalizer = TurkishSentenceNormalizer(self.morphology)
        self.extractor = TurkishSentenceExtractor()

    def mine(self, sources: list[str], keyword="", itemSize=10, numberOfComments=0):
        for source in sources:
            con = Connector()
            con.connectToApi(source)
            self.__minedData[source] = searchKeyword(con, keyword=keyword, itemSize=itemSize,
                                                     numberOfComments=numberOfComments)
            # del(self.__minedData["YouTube"]["Content"])
            # self.__minedData["YouTube"]["Content"] = []

    def extractSentences(self):

        for source in self.__minedData.keys():
            dataPool = self.__minedData[source]
            if source == "Twitter":
                for data in dataPool.copy():
                    dataPool.remove(data)
                    dataPool.extend(self.__extractor(data))
            elif source == "YouTube":
                contents = dataPool["Content"].copy()
                for data in contents:
                    dataPool["Content"].remove(data)
                    __extracted = self.__extractor(data)

                    something = __extracted.copy()

                    for eXt in something:
                        __extracted.remove(eXt)
                        splitted = eXt.split(" ")
                        if len(splitted) > 60:
                            aList = []
                            bList = []
                            for word in splitted:
                                aList.append(word)
                                if len(aList) == 60:
                                    bList.append(aList.copy())
                                    aList.clear()
                            for wordList in bList:
                                s = ""
                                for word in wordList:
                                    s += word + " "
                                s += "."
                                wordList.clear()
                                __extracted.append(s)

                        else:
                            s = ""
                            for word in splitted:
                                s += word + " "
                            s += "."
                            __extracted.append(s)
                    
                    del(something)
                            

                    dataPool["Content"].extend(__extracted)
                # del(contents)
                # del(data)
                comments = dataPool["Comments"].copy()
                for data in comments:
                    dataPool["Comments"].remove(data)
                    dat = data.copy()
                    for da in dat:
                        dat.remove(da)
                        dat.extend(self.__extractor(da))
                    dataPool["Comments"].extend(dat.copy())
                    del(dat)
                del(comments)
                del(data)
            else:
                for data in dataPool.copy():
                    dataPool.remove(data)
                    
                    title = data.title
                    article_header, article_paragraph = data.article.split("###")

                    data.title = self.__extractor(title)
                    headerList = self.__extractor(article_header)
                    paragraphList = self.__extractor(article_paragraph)
                    headerList.extend(paragraphList)
                    data.article = headerList.copy()

                    dataPool.append(data)




            self.__minedData[source] = dataPool.copy()
            del(dataPool)

    def tokenizeWords(self, fromTitle=False, fromArticle=False, source=None):
        if not fromTitle and not fromArticle:
            fromArticle = True
        if source is None:
            for source, data in self.__minedData.items():
                if source in ["Twitter", "YouTube"]:
                    if source == "Twitter":
                        for da in data.copy():
                            data.remove(da)
                            data.append(self.__tokenizer(da))
                    else:
                        for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                            if fromTitle:
                                data["Content"].remove(cont)
                                data["Content"].append(self.__tokenizer(cont))
                            if fromArticle:
                                for comment in comments.copy():
                                    data["Comments"].remove(comments)
                                    comments.remove(comment)
                                    comments.append(self.__tokenizer(comment))
                                    data["Comments"].append(comments)

                else:
                    for da in data.copy():
                        data.remove(da)
                        if fromTitle:
                            data.append(self.__tokenizer(da.title))
                        if fromArticle:
                            data.append(self.__tokenizer(da.article))

                self.__minedData[source] = data
        else:
            data = self.__minedData[source]
            if source in ["Twitter", "YouTube"]:
                if source == "Twitter":
                    for da in data.copy():
                        data.remove(da)
                        data.append(self.__tokenizer(da))
                else:
                    for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                        if fromTitle:
                            data["Content"].remove(cont)
                            data["Content"].append(self.__tokenizer(cont))
                        if fromArticle:
                            for comment in comments.copy():
                                data["Comments"].remove(comments)
                                comments.remove(comment)
                                comments.append(self.__tokenizer(comment))
                                data["Comments"].append(comments)
            else:
                for da in data.copy():
                    data.remove(da)
                    if fromTitle:
                        data.append(self.__tokenizer(da.title))
                    if fromArticle:
                        data.append(self.__tokenizer(da.article))

                self.__minedData[source] = data

    def normalizeSentences(self):
        for source in self.__minedData.keys():
            dataPool = self.__minedData[source]
            if source == "Twitter":
                for data in dataPool.copy():
                    dataPool.remove(data)
                    dataPool.append(self.__normalizer(data))
            # elif source == "YouTube":
            #     comments = dataPool["Comments"].copy()
            #     for data in comments:
            #         dataPool["Comments"].remove(data)
            #         dataPool["Comments"].append(self.__normalizer(data))
            #     del(comments)
            else:
                pass ##TODO
                
            self.__minedData[source] = dataPool.copy()
            del(dataPool)

    def getData(self):
        return self.__minedData

    def __extractor(self, string: str):
        return self.extractor.from_paragraph(string.replace("\n", " "))

    def __normalizer(self, string: str):
        return self.normalizer.normalize(string)

    def __tokenizer(self, string: str):
        lowerMap = {ord(u'A'): u'a', ord(u'A'): u'a', ord(u'B'): u'b', ord(u'C'): u'c', ord(u'Ç'): u'ç',
                    ord(u'D'): u'd', ord(u'E'): u'e', ord(u'F'): u'f', ord(u'G'): u'g', ord(u'Ğ'): u'ğ',
                    ord(u'H'): u'h', ord(u'I'): u'ı', ord(u'İ'): u'i', ord(u'J'): u'j', ord(u'K'): u'k',
                    ord(u'L'): u'l', ord(u'M'): u'm', ord(u'N'): u'n', ord(u'O'): u'o', ord(u'Ö'): u'ö',
                    ord(u'P'): u'p', ord(u'R'): u'r', ord(u'S'): u's', ord(u'Ş'): u'ş', ord(u'T'): u't',
                    ord(u'U'): u'u', ord(u'Ü'): u'ü', ord(u'V'): u'v', ord(u'Y'): u'y', ord(u'Z'): u'z'}
        inp = string.translate(lowerMap)
        tokenizer = TurkishTokenizer.DEFAULT
        tknL = tokenizer.tokenize(inp)
        ## (not str(t.type_) == "Type.Mention") can be added!
        ls = []
        ls.append("[CLS]")
        for t in tknL:
            if (not t.content.startswith("_")) and (not str(t.type_) == "Type.URL") and (
                    not str(t.type_) == "Type.Punctuation") and (not t.content in self.stopwordList):
                ls.append(utils.to_unicode(t.content))
        ls.append("[SEP]")
        return ls

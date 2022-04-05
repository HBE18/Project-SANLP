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

    def mine(self, sources: list[str], keyword="", itemSize=10, numberOfComments=0):
        for source in sources:
            con = Connector()
            con.connectToApi(source)
            self.__minedData[source] = searchKeyword(con, keyword=keyword, itemSize=itemSize,
                                                     numberOfComments=numberOfComments)

    def extractSentences(self, fromTitle=False, fromArticle=False, source=None):
        if not fromTitle and not fromArticle:
            fromArticle = True
        if source is None:
            for source, data in self.__minedData.items():
                if source in ["Twitter", "YouTube"]:
                    if source == "Twitter":
                        for da in data.copy():
                            data.remove(da)
                            data.append(self.__extractor(da))
                    else:
                        for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                            if fromTitle:
                                data["Content"].remove(cont)
                                sentT = []
                                cont = cont.replace("\n", " ")
                                splitted = cont.split(" ")
                                for i in range(0, len(splitted), 60):
                                    st = ""
                                    for j in range(i, min(i + 60, len(splitted))):
                                        st += splitted[j] + " "
                                    sentT.append(st)

                                data["Content"].append(sentT)
                                # data["Content"].append(self.__extractor(cont))
                            if fromArticle:
                                for comment in comments.copy():
                                    data["Comments"].remove(comments)
                                    comments.remove(comment)
                                    comments.append(self.__extractor(comment))
                                    data["Comments"].append(comments)

                else:
                    for da in data.copy():
                        data.remove(da)
                        if fromTitle:
                            data.append(self.__extractor(da.title))
                        if fromArticle:
                            data.append(self.__extractor(da.article))

                self.__minedData[source] = data
        else:
            data = self.__minedData[source]
            if source in ["Twitter", "YouTube"]:
                if source == "Twitter":
                    for da in data.copy():
                        data.remove(da)
                        data.append(self.__extractor(da))
                else:
                    for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                        if fromTitle:
                            data["Content"].remove(cont)
                            data["Content"].append(self.__extractor(cont))
                        if fromArticle:
                            for comment in comments.copy():
                                data["Comments"].remove(comments)
                                comments.remove(comment)
                                comments.append(self.__extractor(comment))
                                data["Comments"].append(comments)
            else:
                for da in data.copy():
                    data.remove(da)
                    if fromTitle:
                        data.append(self.__extractor(da.title))
                    if fromArticle:
                        data.append(self.__extractor(da.article))

                self.__minedData[source] = data

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

    def normalizeSentences(self, fromTitle=False, fromArticle=False, source=None):
        if not fromTitle and not fromArticle:
            fromArticle = True
        if source is None:
            for source, data in self.__minedData.items():
                if source in ["Twitter", "YouTube"]:
                    if source == "Twitter":
                        for da in data:
                            data.remove(da)
                            for sent in da.copy():
                                da.remove(sent)
                                da.append(self.__normalizer(sent))
                            data.append(da)
                    else:
                        for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                            if fromTitle:
                                if isinstance(cont, list):
                                    for con in cont.copy():
                                        data["Content"].remove(cont)
                                        cont.remove(con)
                                        cont.append(self.__normalizer(con))
                                        data["Content"].append(cont)
                                else:
                                    data["Content"].remove(cont)
                                    data["Content"].append(self.__normalizer(cont))
                            if fromArticle:
                                for comment in comments.copy():
                                    if isinstance(comment, list):
                                        for sent in comment.copy():
                                            data["Comments"].remove(comments)
                                            comments.remove(sent)
                                            comments.append(self.__normalizer(sent))
                                            data["Comments"].append(comments)
                                    else:
                                        data["Content"].remove(cont)
                                        data["Content"].append(self.__normalizer(cont))

                else:
                    for da in data.copy():
                        data.remove(da)
                        for sent in da:
                            da.remove(sent)
                            if fromTitle:
                                da.append(self.__normalizer(sent))
                            if fromArticle:
                                da.append(self.__normalizer(sent))
                        data.append(da)

                self.__minedData[source] = data
        else:
            data = self.__minedData[source]
            if source in ["Twitter", "YouTube"]:
                if source == "Twitter":
                    for da in data:
                        data.remove(da)
                        for sent in da.copy():
                            da.remove(sent)
                            da.append(self.__normalizer(sent))
                        data.append(da)
                else:
                    for cont, comments in zip(data["Content"].copy(), data["Comments"].copy()):
                        if fromTitle:
                            for con in cont.copy():
                                data["Content"].remove(cont)
                                cont.remove(con)
                                cont.append(self.__normalizer(con))
                                data["Content"].append(cont)
                        if fromArticle:
                            for comment in comments.copy():
                                for sent in comment.copy():
                                    data["Comments"].remove(comments)
                                    comments.remove(sent)
                                    comments.append(self.__normalizer(sent))
                                    data["Comments"].append(comments)

            else:
                for da in data.copy():
                    data.remove(da)
                    for sent in da:
                        da.remove(sent)
                        if fromTitle:
                            da.append(self.__normalizer(sent))
                        if fromArticle:
                            da.append(self.__normalizer(sent))
                    data.append(da)

                self.__minedData[source] = data

    def getData(self):
        return self.__minedData

    def __extractor(self, string: str):
        return TurkishSentenceExtractor().from_paragraph(string.replace("\n", " "))

    def __normalizer(self, string: str):
        return TurkishSentenceNormalizer(self.morphology).normalize(string)

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

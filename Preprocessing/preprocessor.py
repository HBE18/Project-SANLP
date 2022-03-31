from zemberek import TurkishSentenceExtractor


class Preprocessor:
    def __init__(self, minedData: dict[str, list[str]]):
        self.__minedData = minedData

    def extractSentences(self):
        for source, data in self.__minedData.items():
            if source in ["Twitter", "Youtube"]:
                pass
            else:
                for da in data:
                    data.remove(da)
                    data.append(TurkishSentenceExtractor().from_paragraph(da.replace("\n", " ")))
                self.__minedData[source] = data


    def getPreprocessedData(self) -> dict[str,list[str]]:
        return self.__minedData
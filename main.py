from DataMining.apiConnector import Connector
from DataMining.miner import searchKeyword
from Preprocessing.preprocessor import Preprocessor

con = Connector()
con.connectToApi("Hurriyet")
res = searchKeyword(con,"Mansur Yavaş",3)

print(res)

prep = Preprocessor(res)
prep.extractSentences()
dat = prep.getPreprocessedData()

for source, data in dat.items():
    print(source + ":\n\n")

    for ind in range(len(data)):
        print(f"{ind}\t {data[ind]}")
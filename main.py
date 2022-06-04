import psycopg2
from Preprocessing.preprocessor import Preprocessor
from eng import Controller, BertClassifier

# db = psycopg2.connect(user = "postgres",
#                       password = "123456",
#                       host = "25.33.228.221",
#                       port = "5432",
#                       database = "sanlp")


# cursor = db.cursor()

# query = "SELECT keyword FROM keywords;"
# cursor.execute(query)

# result = cursor.fetchall()

# for i in result:
#     print(i)




prep = Preprocessor()

prep.mine(["YouTube","Twitter"], "Mansur Yavaş", itemSize=3, numberOfComments=5)

prep.extractSentences()
prep.normalizeSentences()
res = prep.getData()

miningNLPRes = {}
cont = Controller()

for source in res.keys():
    dataPool = res[source].copy()
    resList = []
    if source == "Twitter":
        resList.append(cont.avg_result(dataPool))
        print(dataPool)

    elif source == "YouTube":
        resList.append(cont.avg_result(dataPool["Content"]))

        resList.append(cont.avg_result(dataPool["Comments"]))

    
    else:
        for data in dataPool:
            #resList.append(cont.avg_result(data.title))
            print(data.title)
            print(data.article)
            #resList.append(cont.avg_result(data.article))
            
    
    miningNLPRes[source] = resList.copy()




for key, value in miningNLPRes.items():
    print(key + ":",value)
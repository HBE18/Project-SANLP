import psycopg2
from Preprocessing.preprocessor import Preprocessor
from eng import Controller

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

prep.mine(["Twitter","YouTube","Posta"], "Mansur Yavaş", itemSize=10, numberOfComments=5)

prep.extractSentences()
prep.normalizeSentences()
res = prep.getData()

miningNLPRes = {}
cont = Controller()

for source in res.keys():
    dataPool = res[source]
    resList = []
    if source == "Twitter":
        for data in dataPool:
            resList.append(cont.avg_result(data))

    elif source == "YouTube":
        for data in dataPool["Content"]:
            resList.append(cont.avg_result(data))

        for data in dataPool["Comments"]:
            resList.append(cont.avg_result(data))

    
    else:
        for data in dataPool:
            for title in data.title:
                resList.append(cont.avg_result(title))

            for article in data.article:
                resList.append(cont.avg_result(article))
    
    miningNLPRes[source] = resList.copy()




for key, value in miningNLPRes.items():
    print(key + ":",value)
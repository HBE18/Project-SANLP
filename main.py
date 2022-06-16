import psycopg2
from Preprocessing.preprocessor import Preprocessor
from eng import Controller, BertClassifier
import matplotlib.pyplot as plt
import numpy as np

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

prep.mine(["YouTube","Twitter"], "Mansur Yavaş", itemSize=1, numberOfComments=2)

prep.extractSentences()
prep.normalizeSentences()
res = prep.getData()

miningNLPRes = {}
cont = Controller()

for source in res.keys():
    dataPool = res[source].copy()
    print(len(dataPool))
    resList = []
    if source == "Twitter":
        resList.append(cont.avg_result(dataPool))

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

isempty=[False,False]
labels = ["Olumlu", "Tarafsız", "Olumsuz"]
for key, value in miningNLPRes.items():
    if key == "YouTube":
        if len(value[0][1]) == 0:
            isempty[0] = True
            res = np.array([1])
            lb = ["Değer Yok"]
            plt.pie(res, labels=lb,autopct='%1.1f%%',shadow=True)
            fname = "Youtube_Content.png"
            plt.savefig(fname)
            plt.close()
        if len(value[1][1]) == 0:
            isempty[1] = True
            res = np.array([1])
            lb = ["Değer Yok"]
            plt.pie(res, labels=lb,autopct='%1.1f%%',shadow=True)
            fname = "Youtube_Comment.png"
            plt.savefig(fname)
            plt.close()
    else:
        if len(value[0][1]) == 0:
            res = np.array([1])
            lb = ["Değer Yok"]
            plt.pie(res, labels=lb,autopct='%1.1f%%',shadow=True)
            fname = key + ".png"
            plt.savefig(fname)
            plt.close()
            continue
                   
        
    fname = key
    if key == "YouTube":
        if isempty[0] == False:
            res = np.array(value[0][0])
            #res = res.flatten()
            plt.pie(res, labels=labels,autopct='%1.1f%%',shadow=True)
            plt.legend()
            fname = fname + "_Content.png"
            plt.savefig(fname)
            plt.close()

        if isempty[1] == False:
            res = np.array(value[1][0])
            #res = res.flatten()
            plt.pie(res, labels=labels,autopct='%1.1f%%',shadow=True)
            plt.legend()
            fname = key
            fname = fname + "_Comment.png"
            plt.savefig(fname)
            plt.close()
    else:
        res = np.array(value[0][0])
        #res = res.flatten()
        #print(res)
        plt.pie(res,labels=labels,autopct='%1.1f%%',shadow=True)
        plt.legend()
        fname = fname + ".png"
        plt.savefig(fname)
        plt.close()
    #print(key + ":",value)

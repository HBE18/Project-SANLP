from Preprocessing.preprocessor import Preprocessor
from eng import Controller, BertClassifier
import matplotlib.pyplot as plt
import numpy as np
from Database.postgres import Postgres
from PIL import Image
from pymongo import MongoClient
from datetime import datetime
from io import BytesIO
import base64

def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str

def b64_2_img(data):
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

client = MongoClient("25.33.228.221:27017")
db = client.sanlp

sql = Postgres()
keywordList = sql.getAllKeywords()
prep = Preprocessor()

for keyword in keywordList:
    prep.mine(["YouTube", "Twitter"], keyword,
            itemSize=1, numberOfComments=2)

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
                # resList.append(cont.avg_result(data.title))
                print(data.title)
                print(data.article)
                # resList.append(cont.avg_result(data.article))

        miningNLPRes[source] = resList.copy()

    isempty = [False, False]
    labels = ["Olumlu", "Tarafsız", "Olumsuz"]
    for key, value in miningNLPRes.items():
        if key == "YouTube":
            if len(value[0][1]) == 0:
                isempty[0] = True
                res = np.array([1])
                lb = ["Değer Yok"]
                plt.pie(res, labels=lb, autopct='%1.1f%%', shadow=True)
                fname = "YouTube_Content.png"
                plt.savefig(fname)
                plt.close()
            if len(value[1][1]) == 0:
                isempty[1] = True
                res = np.array([1])
                lb = ["Değer Yok"]
                plt.pie(res, labels=lb, autopct='%1.1f%%', shadow=True)
                fname = "YouTube_Comment.png"
                plt.savefig(fname)
                plt.close()
        else:
            if len(value[0][1]) == 0:
                res = np.array([1])
                lb = ["Değer Yok"]
                fig = plt.pie(res, labels=lb, autopct='%1.1f%%', shadow=True)
                fname = key + ".png"
                plt.savefig(fname)
                plt.close()
                continue

        fname = key
        if key == "YouTube":
            if isempty[0] == False:
                res = np.array(value[0][0])
                #res = res.flatten()
                plt.pie(res, labels=labels, autopct='%1.1f%%', shadow=True)
                plt.legend()
                fname = fname + "_Content.png"
                plt.savefig(fname)
                plt.close()

            if isempty[1] == False:
                res = np.array(value[1][0])
                #res = res.flatten()
                plt.pie(res, labels=labels, autopct='%1.1f%%', shadow=True)
                plt.legend()
                fname = key
                fname = fname + "_Comment.png"
                plt.savefig(fname)
                plt.close()
        else:
            res = np.array(value[0][0])
            #res = res.flatten()
            # print(res)
            plt.pie(res, labels=labels, autopct='%1.1f%%', shadow=True)
            plt.legend()
            fname = fname + ".png"
            plt.savefig(fname)
            plt.close()
        #print(key + ":",value)
    #TODO: if png does not work switch to jpeg!!
    im1 = Image.open("Youtube_Content.png")
    im2 = Image.open("YouTube_Comment.png")
    im3 = Image.open("Twitter.png")
    cont = im_2_b64(im1)
    comt = im_2_b64(im2)
    twt = im_2_b64(im3)
    dt = datetime.now()
    obj = {
        'keyword':keyword,
        'timestamp':dt,
        'yt_content':cont,
        'yt_comment':comt,
        'twitter':twt
    }
    with client.start_session() as session:
        with session.start_transaction():
            obj = db.results.insert_one(obj)
    userList = sql.getUserIdListOfTheKeyword(keyword) # Users who are searching the keyword."""



    
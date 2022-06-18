from pymongo import MongoClient
from PIL import Image
import io
from datetime import date, datetime

"""cli = MongoClient("25.33.228.221:27017")
db = cli.sanlp
#db.results.insert_one({'id':88, 'psw':888})

for i in range(5):
    obj = {
        'id' : i,
        'psw' : i * i
    }
    result = db.userids.insert_one(obj)
    print(result)

with cli.start_session() as session:
    with session.start_transaction():
        obj = db.results.find_one({'keyword':"Mansur Yavaş"})

im = Image.frombytes('RGBA',(640,480),obj['yt_content'])
im.show()"""
print(str(datetime.now()))
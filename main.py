from Preprocessing.preprocessor import Preprocessor

prep = Preprocessor()

prep.mine(["YouTube"], "Mansur Yavaş", itemSize=10, numberOfComments=5)
res = prep.getData()

"""for source, data in res.items():
    print("\n" + source)
    if source == "YouTube":
        for cont in data["Content"]:
            print(cont)
            print("--------")"""

prep.extractSentences(True, True)
res = prep.getData()

for source, data in res.items():
    print("\n" + source)
    if source == "YouTube":
        for cont in data["Content"]:
            for c in cont:
                print(len(c.split(" ")))
            print("--------")
    elif source == "Twitter":
        for da in data:
            for d in da:
                print(d)
            print()
    print()
"""
print("\n\nNormalization\n\n")
prep.normalizeSentences(True,True)
res = prep.getData()

for source, data in res.items():
    print(source)
    if source == "YouTube":
        for cont,comments in zip(data["Content"], data["Comments"]):
            print(cont)
            print()
            for comment in comments:
                print(comment)
            print("--------")
    elif source == "Twitter":
        for da in data:
            for d in da:
                print(d)
            print()
    print()
"""

from apiConnector import connectToApi, _getCurrentApi

def searchKeyword(keyword="",itemSize=10, numberOfComments = 0) -> list:
    """
    Takes a keyword and an itemSize and searches that keyword in connected API.

    ``keyword`` is the string which is searched on the API.

    ``itemSize`` is the integer which is requested result size.

    Example Usage:
    >>> searchKeyword("Ankara",10)
    """
    if numberOfComments == 0:
        return _getCurrentApi().searchKeyword(keyword,itemSize)
    else:
        return _getCurrentApi().searchKeyword(keyword,itemSize,numberOfComments = numberOfComments)

"""
Example Usage:
>>> connectToApi("Twitter")
>>> res = searchKeyword("Ankara",10)
"""

connectToApi("YouTube")
res = searchKeyword("dolar",2,numberOfComments=3)
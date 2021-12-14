from apiConnector import connectToApi, _getCurrentApi

def searchKeyword(keyword="",itemSize=10) -> list:
    """
    Takes a keyword and an itemSize and searches that keyword in connected API.

    ``keyword`` is the string which is searched on the API.

    ``itemSize`` is the integer which is requested result size.

    Example Usage:
    >>> searchKeyword("Ankara",10)
    """

    return _getCurrentApi().searchKeyword(keyword,itemSize)

"""
Example Usage:
>>> connectToApi("Twitter")
>>> res = searchKeyword("Ankara",10)
"""
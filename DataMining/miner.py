from .apiConnector import Connector


def searchKeyword(con: Connector, keyword="", itemSize=10, numberOfComments=0) -> dict:
    """
    Takes a keyword and an itemSize and searches that keyword in connected API.

    ```con```is the object of the Connector class.

    ``keyword`` is the string which is searched on the API.

    ``itemSize`` is the integer which is requested result size.

    Example Usage:
    >>> searchKeyword("Ankara",10)
    """
    currentApi = con._getCurrentApi()
    result = currentApi.searchKeyword(keyword, itemSize, numberOfComments)

    return result


"""
Example Usage:
>>> con = Connector()
>>> con.connectToApi("Twitter")
>>> res = searchKeyword("Ankara",10)

For YouTube:
    YouTube API's search keyword function takes 1 additional parameter named ``numberOfComments`` and returns a dictionary.
    That dictionary has 2 keys: Captions and Comments.
    Captions has caption list of the videos.
    Comments has commments list of the videos.
    
    Example Usage:
        >>> con = Connector()
        >>> con.connectToApi("YouTube")
        >>> res = searchKeyword("Atari",10,numberOfComments=10)
"""

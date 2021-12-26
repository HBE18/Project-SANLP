from apiConnector import connectToApi, _getCurrentApi
from YouTube import YouTube

def searchKeyword(keyword="",itemSize=10, numberOfComments = 0) -> list:
    """
    Takes a keyword and an itemSize and searches that keyword in connected API.

    ``keyword`` is the string which is searched on the API.

    ``itemSize`` is the integer which is requested result size.

    Example Usage:
    >>> searchKeyword("Ankara",10)
    """
    if numberOfComments == 0:
        result = _getCurrentApi().searchKeyword(keyword,itemSize)
    else:
        result = _getCurrentApi().searchKeyword(keyword,itemSize,numberOfComments = numberOfComments)
    if isinstance(_getCurrentApi(),YouTube):
        _getCurrentApi().closeBrowser()

    return result

"""
Example Usage:
>>> connectToApi("Twitter")
>>> res = searchKeyword("Ankara",10)

For YouTube:
    YouTube API's search keyword function takes 1 additional parameter named ``numberOfComments`` and returns a dictionary.
    That dictionary has 2 keys: Captions and Comments.
    Captions has caption list of the videos.
    Comments has commments list of the videos.
    
    Example Usage:
        >>> connectToApi("YouTube")
        >>> res = searchKeyword("Atari",10,numberOfComments=10)
"""

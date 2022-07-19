class Group:
    """
    A class used to represent a Channel of Telegram

    ...

    Attributes
    ----------
    id : str
        identification of the channel in Telegram's API
    distance : str
        distance from the pinpoint
    name : str
        name of the channel in Telegram

    Methods
    -------
    None
    """
    id = None
    distance = None
    name = None

    def __init__(self, _id, _distance, _name):
        self.id = _id
        self.distance = _distance
        self.name = _name


    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance': self.distance
        }

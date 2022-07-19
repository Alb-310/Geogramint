class User:
    """
    A class used to represent a User of Telegram

    ...

    Attributes
    ----------
    id : str
        identification of the user in Telegram's API
    distance : str
        distance from the pinpoint
    username : str
        username of the user in Telegram
    firstname : str
        first name of the user
    lastname : str
        last name of the user
    phone : str
        phone number associated to the Telegram account

    Methods
    -------
    None
    """
    id = None
    distance = None
    username = None
    firstname = None
    lastname = None
    phone = None

    def __init__(self, _id, _distance, _username, _firstname=None, _lastname=None, _phone=None):
        self.id = _id
        self.distance = _distance
        self.username = _username
        self.firstname = _firstname
        self.lastname = _lastname
        self.phone = _phone

    def __dict__(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'phone': self.phone,
            'distance': self.distance
        }

import asyncio

from kivy import Logger
from kivy.clock import Clock
from telethon import TelegramClient

from utils import User
from utils import Group
import os

'''
A function that parse the result of Telegram's API request
and isolate the Users

:param res: str
    result of Telegram's API request
:return str
    isolated string that contain all users
'''


def isolation_Users(res):
    usersStrtIndex = str.find(res, "users=[")
    usersEndIndex = str.find(res, "\n\t],", usersStrtIndex)
    usersList = res[usersStrtIndex:usersEndIndex + len("\n\t]")]
    return usersList


'''
A function that parse the result of Telegram's API request
and isolate the Channels

:param res: str
    result of Telegram's API request
:return str
    isolated string that contain all channels
'''


def isolation_Channels(res):
    channelsStrtIndex = str.find(res, "chats=[")
    channelsEndIndex = str.find(res, "\n\t],", channelsStrtIndex)
    channelsList = res[channelsStrtIndex:channelsEndIndex + len("\n\t]")]
    return channelsList


'''
A function that parse the result of Telegram's API request
and isolate the Peers

:param res: str
    result of Telegram's API request
:return str
    isolated string that contain all peers
'''


def isolation_Peers(res):
    peersStrtIndex = str.find(res, "peers=[")
    peersEndIndex = str.find(res, "\n\t],", peersStrtIndex)
    peersList = res[peersStrtIndex:peersEndIndex + len("\n\t]")]
    return peersList


'''
A function that parse the isolation 
of Users List from exported result of Telegram's API request
and retrieve the required parameter

:param res: str
    isolation of Users List
:param start: int
    starting index
:return str
    required parameter
'''


def find_param(res, start):
    end = str.find(res, ",", start)
    return res[start:end]


'''
A function that parse the isolation 
of Channels List from exported result of Telegram's API request
and retrieve the required parameter

:param res: str
    isolation of Channels List
:param start: int
    starting index
:return str
    required parameter
'''


def find_dist(res, start):
    end = str.find(res, "\n", start)
    return res[start:end]


'''
A function that generate a List of User objects
from the isolation of Users List from exported 
result of Telegram's API request

:param usersList: str
    isolation of Users List
:param peersList: str
    isolation of Peers List
:return list
    User list
'''


def generate_ListOfUsers(usersList, peersList):
    output = []
    i = 0
    while (i != -1):
        # parse elements to create a User Object in the Users Isolation
        i = str.find(usersList, "\tid=", i)
        uid = find_param(usersList, i + len("\tid="))
        i = str.find(usersList, "first_name=", i)
        firstname = find_param(usersList, i + len("first_name="))
        i = str.find(usersList, "last_name=", i)
        lastname = find_param(usersList, i + len("last_name="))
        i = str.find(usersList, "username=", i)
        username = find_param(usersList, i + len("username="))
        i = str.find(usersList, "phone=", i)
        phone = find_param(usersList, i + len("phone="))

        # parse elements to create User Object in the Peers Isolation
        j = str.find(peersList, uid)
        j = str.find(peersList, "distance=", j)
        distance = find_dist(peersList, j + len("distance="))

        # Adding new User to the List of User Objects
        output.append(User.User(uid, distance, username, firstname, lastname, phone))

        # Test if end of File
        i = str.find(usersList, "\tid=", i)

    # Cleaning attributes of User Object
    for elm in output:
        if elm.id == 'None':
            elm.id = None
        if elm.distance == 'None':
            elm.distance = None
        if elm.firstname == 'None':
            elm.firstname = None
        if elm.lastname == 'None':
            elm.lastname = None
        if elm.username == 'None':
            elm.username = None
        if elm.phone == 'None':
            elm.phone = None

    return output


'''
A function that generate a List of Group objects
from the isolation of Channels List from exported 
result of Telegram's API request

:param groupList: str
    isolation of Channels List
:param peersList: str
    isolation of Peers List
:return list
    User list
'''


def generate_ListOfGroups(groupList, peersList):
    output = []
    i = 0
    while (i != -1):
        # parse elements to create a Group Object in the Channels Isolation
        i = str.find(groupList, "\tid=", i)
        uid = find_param(groupList, i + len("\tid="))
        i = str.find(groupList, "title=", i)
        name = find_param(groupList, i + len("title="))

        # parse elements to create Group Object in the Peers Isolation
        j = str.find(peersList, uid)
        j = str.find(peersList, "distance=", j)
        distance = find_dist(peersList, j + len("distance="))

        # Adding new Group to the List of Group Objects
        output.append(Group.Group(uid, distance, name))

        # Test if end of File
        i = str.find(groupList, "\tid=", i)

    # Cleaning attributes of Group Object
    for elm in output:
        if elm.id == 'None':
            elm.id = None
        if elm.distance == 'None':
            elm.distance = None
        if elm.name == 'None':
            elm.name = None

    return output


'''
A function that download all profiles pictures
of detected users and channels (cache/users/ and cache/groups/)

:param client: update
    client obtained by logging to Telegram's API
:param ListofUser: list
    List of User Objects
:param ListofGroup: list
    List of Group Objects
'''


def download_allprofilespics(client, ListofUser, ListofGroup):
    # create cache file for users profiles pictures
    try:
        os.mkdir("cache_telegram/users")
    except OSError as error:
        Logger.warning("Geogramint Files: cache_telegram/users already exist")

    # create cache file for groups profiles pictures
    try:
        os.mkdir("cache_telegram/groups")
    except OSError as error:
        Logger.warning("Geogramint Files: cache_telegram/groups already exist")

    # verification of the contents of User and Group objects
    invalid_objects = True
    while invalid_objects:
        invalid_objects = False
        if len(ListofUser) > 0 and not ListofUser[0].id.isnumeric():
            ListofUser.pop(0)
            invalid_objects = True
        if len(ListofGroup) > 0 and not ListofGroup[0].id.isnumeric():
            ListofGroup.pop(0)
            invalid_objects = True
    if len(ListofUser) == 0 and len(ListofGroup) == 0:
        raise Exception

    # download of users profile pics
    for elm in ListofUser:
        if not elm.id.isnumeric():
            continue
        client.download_profile_photo(int(elm.id), "cache_telegram/users/" + elm.id)

    # download of groups profile pics
    for elm in ListofGroup:
        if not elm.id.isnumeric():
            continue
        client.download_profile_photo(int(elm.id), "cache_telegram/groups/" + elm.id)



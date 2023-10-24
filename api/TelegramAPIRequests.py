import asyncio
import os
from datetime import datetime

from kivy import Logger
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
from utils import ressources

code_dialog = False
connected = False
code = None
password = None


def geolocate_AllEntities_Nearby(api_id, api_hash, phone_number, latitude, longitude):
    global code_dialog, code, connected, password
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        os.mkdir("cache_telegram")
    except OSError:
        Logger.warning("Geogramint Files: cache_telegram folder already exist")
    client = TelegramClient("Geogramint", api_id, api_hash, device_model="A320MH", app_version="2.1.4a",
                            system_version="Windows 10", lang_code="en", system_lang_code="fr-FR", loop=loop)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)  # message send by Telegram with verification code
        code_dialog = True
        while True:  # authentication
            try:
                if code is not None:
                    client.sign_in(phone=phone_number, code=code)
                if client.is_user_authorized():
                    code_dialog = False
                    connected = True
                    break
            except SessionPasswordNeededError:  # if the user have 2FA auth
                while True:
                    try:
                        client.sign_in(phone=phone_number, password=password)
                        if client.is_user_authorized():
                            code_dialog = False
                            connected = True
                            break
                    except:  # if the password is wrong
                        password = None
                        code = None
                        code_dialog = True
                        continue
            except:  # if code is wrong
                password = None
                code = None
                code_dialog = True
                continue
        code_dialog = False
        connected = True
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    result = client(functions.contacts.GetLocatedRequest(
        geo_point=types.InputGeoPoint(
            lat=latitude,
            long=longitude
        ),
        self_expires=42
    ))
    res = result.stringify()

    # parse the result of the API request and Isolate important components
    usersList = ressources.isolation_Users(res)
    peersList = ressources.isolation_Peers(res)
    channelsList = ressources.isolation_Channels(res)

    # Create List of Objects from the isolated components
    ListofGroup = ressources.generate_ListOfGroups(channelsList, peersList)
    ListofUser = ressources.generate_ListOfUsers(usersList, peersList)
    ressources.download_allprofilespics(client, ListofUser, ListofGroup)
    client.disconnect()
    return ListofUser, ListofGroup, dt_string

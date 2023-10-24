import os
import typer

from rich.progress import Progress
from datetime import datetime
from telethon.sync import TelegramClient
from telethon import functions, types

from CLI import ressources_cli

connected = False
code = None
password = None


def geolocate_AllEntities_Nearby(api_id, api_hash, latitude, longitude, pictures):
    global code, connected, password
    try:
        os.mkdir("cache_telegram")
    except OSError:
        typer.echo(
            typer.style("[WARNING] cache_telegram folder already exist", fg=typer.colors.YELLOW, bold=True))
    with TelegramClient("Geogramint", api_id, api_hash, device_model="A320MH", app_version="2.1.4a",
                        system_version="Windows 10", lang_code="en", system_lang_code="fr-FR") as client:
        client.connect()

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
        usersList = ressources_cli.isolation_Users(res)
        peersList = ressources_cli.isolation_Peers(res)
        channelsList = ressources_cli.isolation_Channels(res)

        # Create List of Objects from the isolated components
        ListofGroup = ressources_cli.generate_ListOfGroups(channelsList, peersList)
        ListofUser = ressources_cli.generate_ListOfUsers(usersList, peersList)
        if pictures:
            with Progress() as progress:
                task1 = progress.add_task("[yellow] Searching Users...", total=len(ListofUser))
                # create cache file for users profiles pictures
                try:
                    os.mkdir("cache_telegram/users")
                except OSError as error:
                    typer.echo(typer.style("[WARNING] cache_telegram/users already exist", fg=typer.colors.YELLOW,
                                           bold=True))

                # create cache file for groups profiles pictures
                try:
                    os.mkdir("cache_telegram/groups")
                except OSError as error:
                    typer.echo(typer.style("[WARNING] cache_telegram/groups already exist", fg=typer.colors.YELLOW,
                                           bold=True))

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
                    progress.update(task1, advance=1)
                    if not elm.id.isnumeric():
                        continue
                    client.download_profile_photo(int(elm.id), "cache_telegram/users/" + elm.id)

                # download of groups profile pics
                task2 = progress.add_task("[grey] Searching Groups...", total=len(ListofGroup))
                for elm in ListofGroup:
                    progress.update(task2, advance=1)
                    if not elm.id.isnumeric():
                        continue
                    client.download_profile_photo(int(elm.id), "cache_telegram/groups/" + elm.id)

    return ListofUser, ListofGroup, dt_string

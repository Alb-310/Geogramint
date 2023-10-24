import codecs
import json
import time
import os
import folium

from io import BytesIO
from rich.progress import Progress
from selenium import webdriver
from xhtml2pdf import pisa, default
from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject
from utils.osintracker_export import generate_empty_dexie_json, fill_dexie_json
from utils import User
from utils import Group
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

global_template = '''
<meta charset="UTF-8">
<pdf:language name="arabic"/>
<h1><img style="display: block; margin-left: auto; margin-right: auto; text-align: right;" src="appfiles/Geogramint.png"  width="75" height="75" /></h1>
<h4>&nbsp;</h4>
<p style="font-size: 16px;">{date}</p>
<p style="text-align: center; font-size: 25px;"><b>Geogramint Report:</b></p>
<p>&nbsp;</p>
<style>
{font}
</style>
<p><img style="display: block; margin-left: auto; margin-right: auto; text-align: center;" src="cache_telegram/reportfiles/map.png"  width="500" height="250" /></p>
<p style="text-align: center; font-size: 15px;"><i> {lat}, {lon} </i></p>
<p>&nbsp;</p>
'''

start_user_table = '''
<p style="font-size: 18px;">Users detected in the area:</p>
<table style="height: 50px; width: 101.209%; border-collapse: collapse; text-align: center;" border="1">
<tbody>
<tr style="height: 36px;">
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Profile Picture</strong></p></td>
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>ID</strong></p></td>
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>First Name</strong></p></td>
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Last Name</strong></p></td>
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Username</strong></p></td>
<td style="width: 14.2857%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Phone</strong></p></td>
<td style="width: 15.4947%; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Distance</strong></p></td></tr>
'''

elem_user_table = '''
<tr>
<td ><p style="font-size: 15px;"><img src="{image}" /></p></td>
<td style="width: 14.2857%;"><p style=" font-size: 15px;">{id}</p></td>
<td style="width: 14.2857%;"><p style=" font-size: {size1}px;">{firstname}</p></td>
<td style="width: 14.2857%;"><p style=" font-size: {size2}px;">{lastname}</p></td>
<td style="width: 14.2857%;"><p style=" font-size: {size3}px;">{username}</p></td>
<td style="width: 14.2857%;"><p style=" font-size: 12px;">{phone}</p></td>
<td style="width: 15.4947%;">{distance}</td>
</tr>
'''

end_table = "</tr></tbody></table>"

elem_group_table = '''
<tr>
<td><p style="font-size: 15px;"><img src="{image}" /></p></td>
<td style="width: 14.2857%;"><p style="font-size: 15px;">{id}</p></td>
<td style="width: 14.2857%;"><p style="font-size: 15px;">{name}</p></td>
<td style="width: 14.2857%;">{distance}</td>
</tr>
'''

start_groups_table = '''
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p style="font-size: 18px;">Groups detected in the area:</p>
<table style="border-collapse: collapse; width: 100%; text-align: center;" border="1">
<tbody>
<tr>
<td style="width: 14.2857%; text-align: center; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Group Picture</strong></p></td>
<td style="width: 14.2857%; text-align: center; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>ID</strong></p></td>
<td style="width: 14.2857%; text-align: center; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Name</strong></p></td>
<td style="width: 14.2857%; text-align: center; height: 36px; background-color: rgb(211, 211, 211);"><p style="font-size: 15px;"><strong>Distance</strong></p></td></tr>

'''

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
    while i != -1:
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
    while i != -1:
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
A function that generate a pdf with the data obtained from the scan

:param userlist: list of user object
    list of users
:param groupslist: list of group object
    list of groups
:param lat: float
    latitude of the scan
:param lon: float
    longitude of the scan
:param timestamp: string
    date and time of the scan
:param path: string
    export path
:param extended_report: string
    option to enable extended report
:return None
'''

def generate_pdf_report(userlist, grouplist, lat, lon, timestamp, path, extended_report):
    global start_groups_table, start_user_table, elem_group_table, elem_user_table, end_table, global_template

    if extended_report == 'True':
        zoom = 14
    else:
        zoom = 15

    with Progress() as progress:
        task3 = progress.add_task("[red] Generating report...", total=5)
        try:
            service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument('--headless')
            options.add_argument('window-size=1920x1080')
            driver = webdriver.Chrome(service=service, options=options)
        except:
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                options = webdriver.EdgeOptions()
                options.use_chromium = True
                options.add_argument("disable-logging")
                options.add_argument('--headless')
                options.add_argument('window-size=1920x1080')
                driver = webdriver.Edge(service=service, options=options)
            except:
                service = FirefoxService(GeckoDriverManager().install())
                options = webdriver.FirefoxOptions()
                options.add_argument('--headless')
                options.add_argument('window-size=1920x1080')
                driver = webdriver.Firefox(service=service, options=options)
        m = folium.Map(location=[lat, lon], zoom_start=zoom)
        folium.Marker(
            [lat, lon]
        ).add_to(m)

        if extended_report == 'True':
            folium.Circle(
                location=(lat, lon),
                radius=3000,
                color="#d75f5f",
                fill=True,
                fill_color="#d75f5f",
            ).add_to(m)

        folium.Circle(
            location=(lat, lon),
            radius=2000,
            color="#ff8700",
            fill=True,
            fill_color="#ff8700",
        ).add_to(m)

        folium.Circle(
            location=(lat, lon),
            radius=1000,
            color="#ffff5f",
            fill=True,
            fill_color="#ffff5f",
        ).add_to(m)

        folium.Circle(
            location=(lat, lon),
            radius=500,
            color="#00ff00",
            fill=True,
            fill_color="#00ff00",
        ).add_to(m)
        try:
            os.mkdir('cache_telegram/reportfiles/')
        except OSError:
            print()
        m.save('cache_telegram/reportfiles/map.html')

        progress.update(task3, advance=1)

        temp_name = "file://" + os.path.abspath('cache_telegram/reportfiles/map.html')

        driver.maximize_window()
        driver.get(temp_name)
        time.sleep(5)
        driver.save_screenshot('cache_telegram/reportfiles/map.png')
        driver.quit()

        progress.update(task3, advance=2)

        distance = '<p style="font-size: 15px; color: {col};"><strong>{dist}m</strong></p>'
        template = global_template.format(date=timestamp, lat=lat, lon=lon, font=r"@font-face { font-family: 'test'; "
                                                                                 r"src: url( "
                                                                                 r"'appfiles/DejaVuSans.ttf') } "
                                                                                 r"p { font-family: 'test' }")

        template += start_user_table

        for user in userlist:
            if user.distance == '500':
                col = '#5fff5f'
            elif user.distance == '1000':
                col = '#ffec00'
            elif user.distance == '2000':
                col = '#ffaf00'
            elif extended_report == 'True':
                col = '#d75f5f'
            else:
                continue
            if len(user.firstname) <= 12:
                size1 = '14'
            else:
                size1 = '11'
            if user.lastname and len(user.lastname) <= 12:
                size2 = '14'
            else:
                size2 = '11'
            if user.username and len(user.username) <= 12:
                size3 = '14'
            else:
                size3 = '11'
            tmp = elem_user_table.format(image='cache_telegram/users/' + str(user.id) + ".jpg" if os.path.exists(
                "cache_telegram/users/" + str(user.id) + ".jpg") else 'appfiles/placeholder.png',
                                         id=str(user.id),
                                         firstname=user.firstname[1:-1],
                                         lastname=user.lastname[1:-1] if user.lastname is not None else "",
                                         username=user.username[1:-1] if user.username is not None else "",
                                         phone='+' + user.phone[1:-1] if user.phone is not None else "",
                                         distance=distance.format(col=col, dist=user.distance),
                                         size1=size1,
                                         size2=size2,
                                         size3=size3)
            template += tmp
        template += end_table
        template += start_groups_table
        for group in grouplist:
            if group.distance == '500':
                col = '#5fff5f'
            elif group.distance == '1000':
                col = '#ffec00'
            elif group.distance == '2000':
                col = '#ffaf00'
            elif extended_report == 'True':
                col = '#d75f5f'
            else:
                continue
            tmp = elem_group_table.format(image='cache_telegram/groups/' + str(group.id) + ".jpg" if os.path.exists(
                "cache_telegram/groups/" + str(group.id) + ".jpg") else 'appfiles/placeholder.png',
                                          id=str(group.id),
                                          name=group.name[1:-1],
                                          distance=distance.format(col=col, dist=group.distance))
            template += tmp
        template += end_table
        result_file = open(path + '/Report_' + str(lat) + ',' + str(lon) + '.pdf', "w+b")

        progress.update(task3, advance=1)

        default.DEFAULT_CSS = DEFAULT_CSS.replace("background-color: transparent;", "", 1)
        pisaFileObject.getNamedFile = lambda self: self.uri

        pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result_file, encoding='UTF-8')
        progress.update(task3, advance=1)

def generate_osintracker_investigation(users, groups, lat, lon, path, extended_report):

    dexie = generate_empty_dexie_json()

    osintracker_investigation = fill_dexie_json(users, groups, f"{lat}, {lon}", dexie, extended_report)

    json_osintracker = json.dumps(osintracker_investigation, ensure_ascii=False, indent=4)
    with codecs.open(path + '/Investigation_Geogramint_' + str(lat) + ',' + str(lon) + '.json', 'w', 'utf-8') as f:
        f.write(json_osintracker)
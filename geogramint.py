# v1.0
import codecs
import trio
import shutil
import json

from api import TelegramAPIRequests
from threading import Thread
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.config import Config
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.logger import Logger
from api.TelegramAPIRequests import geolocate_AllEntities_Nearby
from mapfiles.markercenter import MarkerHelper
from utils import settings
from utils import resultDisplay

lat = None
lon = None
loop = None
users = None
groups = None
enabled = False
searchStarted = False
api_id = None
api_hash = None
phone_number = None


def telegramAPICall():
    global lat, lon, users, groups, enabled, searchStarted
    try:
        users, groups = geolocate_AllEntities_Nearby(api_id, api_hash, phone_number, float(lat), float(lon))
    except Exception as e:
        print(e)

        Logger.info(f"Geogramint Search: Nothing Found")
        searchStarted = False
        return
    enabled = True
    json_string_user = json.dumps([ob.__dict__() for ob in users], ensure_ascii=False)
    with codecs.open('cache_telegram/users.json', 'w', 'utf-8') as f:
        f.write(json_string_user)
    json_string_group = json.dumps([ob.__dict__() for ob in groups], ensure_ascii=False)
    with codecs.open('cache_telegram/groups.json', 'w', 'utf-8') as f:
        f.write(json_string_group)


def startSearch(dt):
    global lat, lon, users, searchStarted
    Logger.info(f"Geogramint Search: Search Started at : {lat}, {lon}")
    if users is None and searchStarted == False \
            and api_id is not None and api_hash is not None and phone_number is not None:
        searchStarted = True
        Logger.info(f"Geogramint Search: Searching ...")
        try:
            t = Thread(target=telegramAPICall)
            t.start()
        except:
            Logger.info(f"Geogramint Search: Nothing Found")
            searchStarted = False


def telegramCodeDialog():
    """
    verification code pop-up
    """
    content = BoxLayout(
        orientation="vertical",
        spacing="10dp",
        size_hint_y=None,
        height="100dp",
    )
    ok = MDFlatButton(
        text="Ok",
        theme_text_color="Custom",
    )

    code_input = MDTextField(
        hint_text="Code:",
        helper_text_mode="on_error",
        helper_text="Wrong format"
    )
    password_input = MDTextField(
        hint_text="Password Two-Step Verification (optional):",
        helper_text_mode="on_error",
        helper_text="Wrong format"
    )
    content.add_widget(code_input)
    content.add_widget(password_input)

    dialog = MDDialog(
        title="Telegram's verification code",
        type="custom",
        content_cls=content,
        auto_dismiss=False,
        buttons=[
            ok,
        ],
    )

    def submit(dt):
        if not code_input.text.isnumeric():
            code_input.error = True
            return
        if password_input.text != "":
            TelegramAPIRequests.password = password_input.text
        TelegramAPIRequests.code = code_input.text

        dialog.dismiss()

    def debug(dt):
        print(TelegramAPIRequests.code)

    ok.bind(on_press=submit)
    dialog.bind(on_dismiss=debug)
    return dialog


def background_loop(dt):
    """
    Main background loop of this app
    """
    global lat, lon, users, enabled
    lat = App.get_running_app().root.ids.mapview.ids.mark.lat
    lon = App.get_running_app().root.ids.mapview.ids.mark.lon
    if users is not None and enabled:
        for user in users:
            name = ""
            if user.firstname is not None:
                name += user.firstname + " "
            if user.lastname is not None:
                name += user.lastname
            resultDisplay.UserList().add_elm(user.id, name, user.username, user.distance)
        groups.sort(key=lambda x: x.distance, reverse=False)
        for group in groups:
            resultDisplay.GroupList().add_elm(group.id, group.name, group.distance)

        resultDisplay.GroupList().add_empty()
        resultDisplay.GroupList().add_empty()
        resultDisplay.UserList().add_empty()
        resultDisplay.UserList().add_empty()
        enabled = False

    if TelegramAPIRequests.code_dialog is True and TelegramAPIRequests.connected is False:
        TelegramAPIRequests.code = None
        telegramCodeDialog().open()
        TelegramAPIRequests.code_dialog = False


def search_location(dt):
    str = App.get_running_app().root.ids.searchInput.text

    if str.count(' ') < 1 and str.count(',') < 1:
        App.get_running_app().root.ids.searchInput.error = True
        return

    try:
        lat, long = str.split(',')
        if lat.count('.') > 1 or long.count('.') > 1:
            App.get_running_app().root.ids.searchInput.error = True
            return
        numlat, numlong = float(lat), float(long)
        App.get_running_app().root.ids.mapview.center_on(numlat, numlong)

        App.get_running_app().root.ids.searchInput.error = False
    except:
        try:
            lat, long = str.split(' ')
            if lat.count('.') > 1 or long.count('.') > 1:
                App.get_running_app().root.ids.searchInput.error = True
                return
            numlat, numlong = float(lat), float(long)
            App.get_running_app().root.ids.mapview.center_on(numlat, numlong)

            App.get_running_app().root.ids.searchInput.error = False
        except:
            App.get_running_app().root.ids.searchInput.error = True
            return


def reload_settings(dt):
    global api_id, api_hash, phone_number
    api_id, api_hash, phone_number = settings.loadConfig()


def settings_menu(dt):
    global api_id, api_hash, phone_number
    dialog = settings.settings_dialog(str(api_id), api_hash, phone_number)
    dialog.bind(on_dismiss=reload_settings)
    dialog.open()


def reset(dt):
    global users, groups, searchStarted
    shutil.rmtree("cache_telegram", ignore_errors=True)
    resultDisplay.UserList().clear_all()
    resultDisplay.GroupList().clear_all()
    users = None
    groups = None
    searchStarted = False


class Geogramint(MDApp):
    def build(self):
        global api_id, api_hash, phone_number
        Window.size = (1100, 600)
        api_id, api_hash, phone_number = settings.loadConfig()

    def on_start(self):
        global loop
        self.window = GridLayout()
        self.icon = "appfiles/Geogramint.png"
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        # display marker in the middle of the map
        MarkerHelper().run()

        # Background loop
        loop = Clock.schedule_interval(background_loop, 1 / 30.)

        # Buttons Bindings
        App.get_running_app().root.ids.Start.bind(on_press=startSearch)
        App.get_running_app().root.ids.Reset.bind(on_press=reset)
        App.get_running_app().root.ids.searchInput.bind(on_text_validate=search_location)
        App.get_running_app().root.ids.settings.bind(on_press=settings_menu)

    def on_stop(self):
        shutil.rmtree("cache", ignore_errors=True)  # deleting cache created by Mapview
        Clock.unschedule(loop)


if __name__ == "__main__":
    shutil.rmtree("cache_telegram", ignore_errors=True)
    shutil.rmtree("cache", ignore_errors=True)
    try:
        trio.run(Geogramint().run())
    except TypeError:
        shutil.rmtree("cache", ignore_errors=True)
        print()

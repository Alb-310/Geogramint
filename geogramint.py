# v1.2
import os
import sys
import codecs
import trio
import shutil
import json
import pandas as pd

if len(sys.argv) < 2:
    from kivy.uix.image import AsyncImage
    from api import TelegramAPIRequests
    from threading import Thread
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.uix.button import MDFlatButton, MDRaisedButton
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
    from plyer import filechooser
    from utils import ressources

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
    error = False
    export_report = None
    extended_report = None
    timestamp = None
    real_lat, real_lon = None, None

    Loading = AsyncImage(
        pos_hint={'bottom': 1, 'right': 1},
        size_hint={0.1, None},
        source='appfiles/orange_loading.gif',
        anim_delay=0.1,
        anim_loop=0
    )
    success_anim = AsyncImage(
        pos_hint={'bottom': 1, 'right': 1},
        size_hint={0.1, None},
        source='appfiles/ok_anim.gif',
        anim_delay=0.1,
        anim_loop=1
    )
    error_anim = AsyncImage(
        pos_hint={'bottom': 1, 'right': 1},
        size_hint={0.1, None},
        source='appfiles/error_anim.gif',
        anim_delay=0.1,
        anim_loop=1
    )


else:
    from CLI import geogramint_cli


def telegramAPICall():
    global lat, lon, users, groups, enabled, searchStarted, error, timestamp, real_lat, real_lon
    try:
        real_lat, real_lon = lat, lon
        users, groups, timestamp = geolocate_AllEntities_Nearby(api_id, api_hash, phone_number, float(lat), float(lon))
    except Exception as e:
        error = True
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

    df = pd.read_json('cache_telegram/users.json')
    df.to_csv('cache_telegram/users.csv', index=None)
    df = pd.read_json('cache_telegram/groups.json')
    df.to_csv('cache_telegram/groups.csv', index=None)


def startSearch(dt):
    global lat, lon, users, searchStarted, Loading
    Logger.info(f"Geogramint Search: Search Started at : {lat}, {lon}")
    if users is None and searchStarted == False \
            and api_id is not None and api_hash is not None and phone_number is not None:
        searchStarted = True
        Logger.info(f"Geogramint Search: Searching ...")
        App.get_running_app().root.ids.mapzone.add_widget(Loading)
        try:
            t = Thread(target=telegramAPICall)
            t.start()
        except:
            Logger.info(f"Geogramint Search: Nothing Found")
            App.get_running_app().root.ids.mapzone.add_widget(error_anim)
            Clock.schedule_once(remove_erroranim, error_anim.anim_delay * 50)
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


def remove_successanim(dt):
    App.get_running_app().root.ids.mapzone.remove_widget(success_anim)


def remove_erroranim(dt):
    App.get_running_app().root.ids.mapzone.remove_widget(error_anim)


def export_pdf_report(dt):
    global timestamp, users, groups, extended_report, real_lat, real_lon
    current_dir = os.getcwd()

    _path = filechooser.save_file(title="Export a Geogramint Report :",
                                  filters=[("Geogramint Report", "*.pdf")])

    os.chdir(current_dir)
    if len(_path) == 0 or _path[0] == "":
        return
    path = _path[0]

    if os.path.isdir(path):
        if path[-1] != '/':
            path += 'Report_' + str(lat) + ',' + str(lon) + '.pdf'
        else:
            path += '/Report_' + str(lat) + ',' + str(lon) + '.pdf'
        try:
            t = Thread(target=ressources.generate_pdf_report, args=(users, groups, real_lat, real_lon, timestamp, path,
                                                                    extended_report))
            t.start()
        except:
            Logger.info("Geogramint report: an error has occured during report creation")
    elif not os.path.isfile(path):
        if path[len(path) - 4:] != '.pdf':
            path += '.pdf'
        try:
            t = Thread(target=ressources.generate_pdf_report, args=(users, groups, real_lat, real_lon, timestamp, path,
                                                                    extended_report))
            t.start()
        except:
            Logger.info("Geogramint report: an error has occured during report creation")
    else:
        return


def background_loop(dt):
    """
    Main background loop of this app
    """
    global lat, lon, users, enabled, Loading, error, export_report
    lat = App.get_running_app().root.ids.mapview.ids.mark.lat
    lon = App.get_running_app().root.ids.mapview.ids.mark.lon
    if users is not None and enabled:
        App.get_running_app().root.ids.mapzone.remove_widget(Loading)
        App.get_running_app().root.ids.mapzone.add_widget(success_anim)
        export_report = MDRaisedButton(
            id="export",
            text="[b]Export PDF[/b]",
            md_bg_color=(1, 0.52, 0, 0.9),
            pos_hint={'center_y': 0.05, 'center_x': 0.15}
        )
        export_report.bind(on_press=export_pdf_report)
        App.get_running_app().root.ids.mapzone.add_widget(export_report)
        Clock.schedule_once(remove_successanim, success_anim.anim_delay * 100)
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

    if not searchStarted and Loading is not None:
        App.get_running_app().root.ids.mapzone.remove_widget(Loading)
    if error:
        App.get_running_app().root.ids.mapzone.add_widget(error_anim)
        Clock.schedule_once(remove_erroranim, error_anim.anim_delay * 50)
        error = False


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
    global api_id, api_hash, phone_number, extended_report
    api_id, api_hash, phone_number, extended_report = settings.loadConfig()


def settings_menu(dt):
    global api_id, api_hash, phone_number
    dialog = settings.settings_dialog(str(api_id), api_hash, phone_number, extended_report)
    dialog.bind(on_dismiss=reload_settings)
    dialog.open()


def reset(dt):
    global users, groups, searchStarted, export_report
    shutil.rmtree("cache_telegram", ignore_errors=True)
    resultDisplay.UserList().clear_all()
    resultDisplay.GroupList().clear_all()
    users = None
    groups = None
    searchStarted = False
    if export_report:
        App.get_running_app().root.ids.mapzone.remove_widget(export_report)


if len(sys.argv) < 2:
    class Geogramint(MDApp):
        def build(self):
            global api_id, api_hash, phone_number, extended_report
            Window.size = (1100, 600)
            api_id, api_hash, phone_number, extended_report = settings.loadConfig()

        def on_start(self):
            global loop, export_report
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

    if len(sys.argv) < 2:
        try:
            trio.run(Geogramint().run())
        except TypeError:
            shutil.rmtree("cache", ignore_errors=True)
    else:
        geogramint_cli.CLI()
    shutil.rmtree("cache", ignore_errors=True)
    if os.path.exists("geckodriver.log"):
        os.remove("geckodriver.log")
    print()

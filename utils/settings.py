import configparser
import os

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label.label import MDLabel

'''
A function that load api_id, api_hash and phone number from config.ini

:return tuple
    tuple containing api_id as an int, api_hash as a string and phone number as a string
'''


def loadConfig():
    config = configparser.ConfigParser()
    if not os.path.exists('appfiles/config.ini'):
        return
    config.read('appfiles/config.ini')
    api_id = int(config.get('API', 'ID'))
    api_hash = config.get('API', 'HASH')
    phone_number = config.get('API', 'PHONE')
    extended_report = config.get('REPORT', 'EXTENDED')
    return api_id, api_hash, phone_number, extended_report

'''
A function that save api_id, api_hash and phone number in config.ini

:param api_id: int
    Telegram's api id
:param api_id: str
    Telegram's api hash
:param api_id: str
    Telegram's api associated phone number
'''


def saveConfig(api_id, api_hash, phone_number, extended_report):
    if api_id is None or len(api_hash) == 0 or len(phone_number) == 0:
        return
    config = configparser.ConfigParser()
    config['API'] = {'ID': str(api_id),
                     'HASH': str(api_hash),
                     'PHONE': str(phone_number)}
    config['REPORT'] = {'EXTENDED': extended_report}
    with open('appfiles/config.ini', 'w') as configfile:
        config.write(configfile)
    return loadConfig()

'''
A function that return a dialog object to be displayed as settings menu
'''


def settings_dialog(id, hash, number, extended_report):
    content = BoxLayout(
        orientation="vertical",
        spacing="12dp",
        size_hint_y=None,
        height="200dp",
    )
    api_id = MDTextField(
        hint_text="API ID",
    )
    api_id.text = id
    api_hash = MDTextField(
        hint_text="API Hash",
    )
    api_hash.text = hash
    phone_number = MDTextField(
        hint_text="Phone Number",
    )
    report_settings = BoxLayout(
        orientation="horizontal",
        spacing="0dp",
    )
    label = MDLabel(
        text="Extended Report"
    )

    checkbox = MDSwitch(
        active=True if extended_report == "True" else False,
        pos_hint={'center_x': .1, 'center_y': .1}
    )
    phone_number.text = number

    content.add_widget(api_id)
    content.add_widget(api_hash)
    content.add_widget(phone_number)
    report_settings.add_widget(label)
    report_settings.add_widget(checkbox)
    content.add_widget(report_settings)



    save = MDFlatButton(
        text="SAVE",
        theme_text_color="Custom",
    )
    cancel = MDFlatButton(
        text="CANCEL",
        theme_text_color="Custom",
    )

    dialog = MDDialog(
        title="Settings",
        type="custom",
        content_cls=content,
        buttons=[
            cancel,
            save,
        ],
    )

    def closefunc(dlt):
        dialog.dismiss()

    def savefunc(dlt):
        if not (api_id.text is not None and api_id.text.isnumeric()):
            return
        if api_hash is None:
            return
        if phone_number is None:
            return
        saveConfig(int(api_id.text), api_hash.text, phone_number.text, checkbox.active)
        dialog.dismiss()

    cancel.bind(on_press=closefunc)
    save.bind(on_press=savefunc)
    return dialog

import configparser
import os

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

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
    return api_id, api_hash, phone_number

'''
A function that save api_id, api_hash and phone number in config.ini

:param api_id: int
    Telegram's api id
:param api_id: str
    Telegram's api hash
:param api_id: str
    Telegram's api associated phone number
'''


def saveConfig(api_id, api_hash, phone_number):
    if api_id is None or len(api_hash) == 0 or len(phone_number) == 0:
        return
    config = configparser.ConfigParser()
    config['API'] = {'ID': str(api_id),
                     'HASH': str(api_hash),
                     'PHONE': str(phone_number)}
    with open('appfiles/config.ini', 'w') as configfile:
        config.write(configfile)
    return loadConfig()

'''
A function that return a dialog object to be displayed as settings menu
'''


def settings_dialog(id, hash, number):
    content = BoxLayout(
        orientation="vertical",
        spacing="12dp",
        size_hint_y=None,
        height="180dp",
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
    phone_number.text = number

    content.add_widget(api_id)
    content.add_widget(api_hash)
    content.add_widget(phone_number)

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
        saveConfig(int(api_id.text), api_hash.text, phone_number.text)
        dialog.dismiss()

    cancel.bind(on_press=closefunc)
    save.bind(on_press=savefunc)
    return dialog

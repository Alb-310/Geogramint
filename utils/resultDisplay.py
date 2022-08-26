import os

from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import fitimage
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.card import MDCard


class MD3Card(MDCard):
    """
    A class used to create a custom MDCard object to display results

    ...

    Attributes
    ----------
    None

    Methods
    -------
    add_elm_user(id, name, username, distance):
        Returns MDCard with an image and a label representing a user

    add_elm_group(id, name, username, distance):
        Returns MDCard with an image and a label representing a group
    """
    text = StringProperty()

    def add_elm_user(self, id, name, username, distance):
        if os.path.exists("cache_telegram/users/" + str(id) + ".jpg"):
            self.add_widget(fitimage.FitImage(
                source="cache_telegram/users/" + str(id) + ".jpg",
                size_hint=(None, None),
            ))
        else:
            self.add_widget(fitimage.FitImage(
                source="appfiles/placeholder.png",
                size_hint=(None, None),
            ))
        if len(name) > 50:
            name = name[:50]
        self.add_widget(MDLabel(
            font_name="DejaVuSans",
            text="[font=DejaVuSans]Id: " + str(
                id) + "\nName: " + name + "\nUsername: " + username + "\nDistance: " + distance + "m[/font]",
            font_style=theme_font_styles[11],
            markup=True
        ))
        return self

    def add_elm_group(self, id, name, distance):
        if os.path.exists("cache_telegram/groups/" + str(id) + ".jpg"):
            self.add_widget(fitimage.FitImage(
                source="cache_telegram/groups/" + str(id) + ".jpg",
                size_hint=(None, None),
            ))
        else:
            self.add_widget(fitimage.FitImage(
                source="appfiles/placeholder.png",
                size_hint=(None, None),
            ))
        if len(name) > 50:
            name = name[:50]
        self.add_widget(MDLabel(
            font_name="DejaVuSans",
            text="[font=DejaVuSans]Id: " + str(id) + "\nName: " + name + "\nDistance: " + distance + "m[/font]",
            font_style=theme_font_styles[11],
            markup=True
        ))
        return self


class UserList():
    """
    A class used to display an MD3Card object to display results for users

    ...

    Attributes
    ----------
    None

    Methods
    -------
    add_elm(id, name, username, distance):
        add new MD3Card to users results list

    add_empty():
        add an empty invisible object to the users results list (it is mainly used to to fix some visual bugs)

    clear_all():
        empty the users result list
    """
    def add_elm(self, id, name, username, distance):
        if id is None:
            id = ""
        if name is None:
            name = ""
        if username is None:
            username = ""
        if distance == "500":
            App.get_running_app().root.ids.usersList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(0.654, 0.95, 0.447, 1),
            ).add_elm_user(id, name, username, distance))
        elif distance == "1000":
            App.get_running_app().root.ids.usersList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(1, 1, 0.368, 1),
            ).add_elm_user(id, name, username, distance))
        elif distance == "2000":
            App.get_running_app().root.ids.usersList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(1, 0.658, 0.267, 1),
            ).add_elm_user(id, name, username, distance))
        else:
            App.get_running_app().root.ids.usersList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(0.90, 0.31, 0.31, 1),
            ).add_elm_user(id, name, username, distance))

    def add_empty(self):
        App.get_running_app().root.ids.usersList.add_widget(MDLabel(
            size_hint_y=None,
        ))

    def clear_all(self):
        App.get_running_app().root.ids.usersList.clear_widgets()


class GroupList():
    """
    A class used to display an MD3Card object to display results for groups

    ...

    Attributes
    ----------
    None

    Methods
    -------
    add_elm(id, name, username, distance):
        add new MD3Card to grous results list

    add_empty():
        add an empty invisible object to the groups results list (it is mainly used to to fix some visual bugs)

    clear_all():
        empty the groups result list
    """
    def add_elm(self, id, name, distance):
        if id is None:
            id = ""
        if name is None:
            name = ""
        if distance == "500":
            App.get_running_app().root.ids.groupsList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(0.654, 0.95, 0.447, 1),
            ).add_elm_group(id, name, distance))
        elif distance == "1000":
            App.get_running_app().root.ids.groupsList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(1, 1, 0.368, 1),
            ).add_elm_group(id, name, distance))
        elif distance == "2000":
            App.get_running_app().root.ids.groupsList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(1, 0.658, 0.267, 1),
            ).add_elm_group(id, name, distance))
        else:
            App.get_running_app().root.ids.groupsList.add_widget(MD3Card(
                size_hint_y=None,
                md_bg_color=(0.90, 0.31, 0.31, 1),
            ).add_elm_group(id, name, distance))

    def add_empty(self):
        App.get_running_app().root.ids.groupsList.add_widget(MDLabel(
            size_hint_y=None,
        ))

    def clear_all(self):
        App.get_running_app().root.ids.groupsList.clear_widgets()
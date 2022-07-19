from kivy_garden.mapview import MapMarker
from kivy.app import App


class MarkerHelper():
    marker = None

    def run(self):
        marker = App.get_running_app().root.ids.mapview.ids.mark
        marker.blink()
        pass


class MarkerCenter(MapMarker):
    def blink(self):
        pass

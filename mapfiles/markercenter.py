from kivy.app import App
from kivy_garden.mapview import MapMarker


class MarkerHelper():
    marker = None

    def run(self):
        marker = App.get_running_app().root.ids.mapview.ids.mark
        marker.blink()


class MarkerCenter(MapMarker):
    def blink(self):
        pass

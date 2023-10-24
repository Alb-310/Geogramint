from kivy_garden.mapview import MapView
from kivy.core.window import Window


class Map(MapView):
    """
    Function that limit out of bounds in the map
    """
    def on_map_relocated(self, *kwargs):
        x1, y1, x2, y2 = self.get_bbox()
        centerX, centerY = Window.center
        latRemainder = self.get_latlon_at(centerX, centerY, zoom=self.zoom)[0] - (x1 + x2) / 2
        if x1 < -85.8: self.center_on((x1 + x2) / 2 + latRemainder + .01, self.lon)
        if x2 > 84.6: self.center_on((x1 + x2) / 2 + latRemainder - .01, self.lon)
        if y1 == -180: self.center_on(self.lat, (y1 + y2) / 2 + 0.01)
        if y2 == 180: self.center_on(self.lat, (y1 + y2) / 2 - 0.01)








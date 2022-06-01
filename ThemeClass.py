# Light
class Theme:
    def __init__(self):
        self.AREA_COLOR = (255, 255, 255)
        self.BG_COLOR = (255, 255, 255)
        self.ACTIVE_CIRCLE_COLOR = (0, 0, 0)
        self.ACTIVE_AREA_COLOR = (255, 255, 255)
        self.CIRCLE_COLOR = (0, 0, 0)
        self.EDGE_COLOR = (0, 0, 0)
        self.BUTTON_TEXT_COLOR = (0, 0, 0)
        self.BUTTON_AREA_COLOR = (255, 255, 255)
        self.GRID_COLOR = (255, 255, 255)
        # text
        self.FONT = "CONSOLA.ttf"


class BlueLightTheme(Theme):
    def __init__(self):
        super().__init__()

        self.AREA_COLOR = self.BG_COLOR = (240, 245, 255)
        self.ACTIVE_CIRCLE_COLOR = (32, 79, 206)
        self.ACTIVE_AREA_COLOR = (176, 194, 242)
        self.CIRCLE_COLOR = self.EDGE_COLOR = (14, 36, 97)
        self.BUTTON_TEXT_COLOR = (14, 36, 97)
        self.BUTTON_AREA_COLOR = (222, 229, 245)
        self.GRID_COLOR = (222, 229, 245)


class OrangeDarkTheme(Theme):
    def __init__(self):
        super().__init__()

        self.AREA_COLOR = self.BG_COLOR = (20, 20, 20)
        self.ACTIVE_AREA_COLOR = self.BUTTON_AREA_COLOR = (40, 40, 40)
        self.CIRCLE_COLOR = self.BUTTON_TEXT_COLOR = (255, 128, 0)
        self.ACTIVE_CIRCLE_COLOR = (255, 153, 51)
        self.EDGE_COLOR = (153, 76, 0)
        self.GRID_COLOR = (40, 40, 40)

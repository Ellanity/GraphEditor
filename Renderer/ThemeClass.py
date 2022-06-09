# Light
class Theme:
    def __init__(self):
        self.BG_COLOR = (255, 255, 255)
        self.AREA_COLOR = (255, 255, 255)
        self.AREA_COLOR_ACTIVE = (255, 255, 255)
        self.CIRCLE_COLOR = (0, 0, 0)
        self.CIRCLE_COLOR_ACTIVE = (0, 0, 0)
        self.EDGE_COLOR = (0, 0, 0)
        self.EDGE_COLOR_ACTIVE = (64, 64, 64)
        self.BUTTON_COLOR_AREA = (255, 255, 255)
        self.BUTTON_COLOR_TEXT = (0, 0, 0)
        self.GRID_COLOR = (255, 255, 255)
        # text
        self.FONT = "font/CONSOLA.TTF"


class BlueLightTheme(Theme):
    def __init__(self):
        super().__init__()

        self.BG_COLOR = (240, 245, 255)
        self.AREA_COLOR = (240, 245, 255)
        self.AREA_COLOR_ACTIVE = (176, 194, 242)
        self.CIRCLE_COLOR = (14, 36, 97)
        self.CIRCLE_COLOR_ACTIVE = (32, 79, 206)
        self.EDGE_COLOR = (14, 36, 97)
        self.EDGE_COLOR_ACTIVE = (71, 100, 178)
        self.BUTTON_COLOR_AREA = (222, 229, 245)
        self.BUTTON_COLOR_TEXT = (14, 36, 97)
        self.GRID_COLOR = (222, 229, 245)


class OrangeDarkTheme(Theme):
    def __init__(self):
        super().__init__()

        self.BG_COLOR = (20, 20, 20)
        self.AREA_COLOR = (20, 20, 20)
        self.AREA_COLOR_ACTIVE = (40, 40, 40)
        self.CIRCLE_COLOR = (255, 128, 0)
        self.CIRCLE_COLOR_ACTIVE = (255, 153, 51)
        self.EDGE_COLOR = (153, 76, 0)
        self.EDGE_COLOR_ACTIVE = (255, 128, 0)
        self.BUTTON_COLOR_AREA = (40, 40, 40)
        self.BUTTON_COLOR_TEXT = (255, 128, 0)
        self.GRID_COLOR = (40, 40, 40)


class GreenDarkTheme(Theme):
    def __init__(self):
        super().__init__()

        self.BG_COLOR = (20, 20, 20)
        self.AREA_COLOR = (20, 20, 20)
        self.AREA_COLOR_ACTIVE = (40, 40, 40)
        self.CIRCLE_COLOR = (102, 204, 0)
        self.CIRCLE_COLOR_ACTIVE = (0, 204, 102)
        self.EDGE_COLOR = (204, 255, 153)
        self.EDGE_COLOR_ACTIVE = (0, 204, 102)
        self.BUTTON_COLOR_AREA = (40, 40, 40)
        self.BUTTON_COLOR_TEXT = (102, 204, 0)
        self.GRID_COLOR = (40, 40, 40)


class RedDarkTheme(Theme):
    def __init__(self):
        super().__init__()

        self.BG_COLOR = (20, 20, 20)
        self.AREA_COLOR = (20, 20, 20)
        self.AREA_COLOR_ACTIVE = (40, 40, 40)
        self.CIRCLE_COLOR = (204, 0, 102)
        self.CIRCLE_COLOR_ACTIVE = (255, 0, 127)
        self.EDGE_COLOR = (255, 51, 153)
        self.EDGE_COLOR_ACTIVE = (255, 0, 127)
        self.BUTTON_COLOR_AREA = (40, 40, 40)
        self.BUTTON_COLOR_TEXT = (204, 0, 102)
        self.GRID_COLOR = (40, 40, 40)

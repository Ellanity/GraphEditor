import pygame


class CustomButton:
    def __init__(self, identifier, display):
        # main
        self.identifier = identifier
        self.display = display
        self.on_click = None
        self.on_press = None
        # additional
        self.position = [0, 0]
        self.font = None
        self.theme = None
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.width = 0
        self.height = 0
        self.content = list()  # list of dicts  {string, color(r,g,b), size}
        self.text_margin_horizontal = 6
        self.text_margin_vertical = 3
        self.padding = 5
        self.text_size = 18

    def check_intersection(self, position):
        if self.position[0] < position[0] < self.position[0] + self.width and \
                self.position[1] < position[1] < self.position[1] + self.height:
            return True
        return False

    def click(self, args=None):
        if self.on_click is not None:
            self.on_click()

    def press(self, args=None):
        if self.on_press is not None:
            self.on_press()

    def set_position(self, position):
        self.position = position

    def add_content(self, content):
        self.content.append(content)

    def set_content(self, content):
        self.content = content

    def set_theme(self, theme):
        self.theme = theme
        self.background_color = theme.BUTTON_AREA_COLOR
        self.border_color = theme.BUTTON_TEXT_COLOR
        self.text_color = theme.BUTTON_TEXT_COLOR
        self.font = theme.FONT

    def render(self):
        texts_to_draw = list()
        for text in self.content:
            texts_to_draw.append(pygame.font.Font(self.font, self.text_size).render(text['string'],
                                                                                    True, self.text_color))

        # ## draw bg
        max_width_of_text = 0
        for text in texts_to_draw:
            if text.get_width() >= max_width_of_text:
                max_width_of_text = text.get_width()
        sum_height_of_text = 0
        for text in texts_to_draw:
            sum_height_of_text += text.get_height()

        bg_width = max_width_of_text + self.text_margin_horizontal * 2
        bg_height = sum_height_of_text + self.text_margin_vertical * 2 * (len(texts_to_draw) + 1)
        self.width = bg_width
        self.height = bg_height
        bg_rectangle = (self.position[0], self.position[1], bg_width, bg_height)
        pygame.draw.rect(self.display, self.background_color, bg_rectangle)
        pygame.draw.rect(self.display, self.border_color, bg_rectangle, 1)
        # ## find location of texts
        for text in texts_to_draw:
            text_x = self.position[0] + self.text_margin_horizontal
            text_y = self.position[1] + self.text_margin_vertical
            for text_ in texts_to_draw:
                text_y += self.text_margin_vertical
                if text_ != text:
                    text_y += text_.get_height() + self.text_margin_vertical
                else:
                    break
            self.display.blit(text, (text_x, text_y))

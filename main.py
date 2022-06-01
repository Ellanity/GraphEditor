import pygame
import sys
from GraphRendererClass import GraphRenderer
from EventsHandlerClass import EventsHandler
from StoreClass import Store

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 500
pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GE:GraphEditor")
clock = pygame.time.Clock()


class App:

    def __init__(self):
        self.display = display
        self.clock = clock
        self.store = Store()
        self.renderer = GraphRenderer()
        self.events_handler = EventsHandler(self)

    def stop(self):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    def run(self):
        self.events_handler.command("graph import 1-0")
        self.events_handler.command("graph choose 1")
        self.events_handler.check_events()


if __name__ == '__main__':
    App().run()

import os

import pygame
import sys
from GraphRendererClass import GraphRenderer
from EventsHandlerClass import EventsHandler
from StoreClass import Store
from GraphEditorClass import GraphEditor

DISPLAY_WIDTH = DISPLAY_HEIGHT = 500
pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("WWG:WorkerWithGraphs")
clock = pygame.time.Clock()


class App:

    def __init__(self):
        self.display = display
        self.clock = clock
        self.renderer = GraphRenderer()
        self.events_handler = EventsHandler(self)
        self.store = Store()

    def stop_program(self):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    def run(self):
        self.events_handler.events()


if __name__ == '__main__':
    App().run()

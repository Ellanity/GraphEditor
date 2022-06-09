import pygame
# from OpenGL.GL import *

import sys
from Renderer.GraphRendererClass import GraphRenderer
from Handler.EventsHandlerClass import EventsHandler
from Store.StoreClass import Store
from Calculator.GraphCalculator import GraphCalculator

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.RESIZABLE )
# display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.RESIZABLE |pygame.DOUBLEBUF |pygame.OPENGL)
pygame.display.set_caption("GraphEditor :D")
try:
    pygame.display.set_icon(pygame.image.load("img/icon.png"))
except Exception as ex:
    print(ex)
clock = pygame.time.Clock()


class App:

    def __init__(self):
        self.display = display
        self.clock = clock
        self.store = Store()
        self.renderer = GraphRenderer()
        self.graph_calculator = GraphCalculator()
        self.events_handler = EventsHandler(self)

    def stop(self):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    def run(self):
        # ## ### comment out the following three lines to get started with empty storage
        self.events_handler.command("graph import example")
        self.events_handler.command("graph choose example")
        self.events_handler.command("graph rename example MyGraph")
        self.events_handler.check_events()


if __name__ == '__main__':
    App().run()

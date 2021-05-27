import os
import pygame.font as pyfont
from pygame import error
from pygame.compat import geterror

from .bbb_local import *
from .bbb_frozen_dir import main_dir

font_dir = os.path.join(main_dir, 'data\\font')


def load_font(name, size):
    """
    Load pygame.font.Font() object
    :param name: Font file name
    :param size: font size
    :return: pygame.font.Font()
    """
    # In case of loading error
    class NoneFont:
        def play(self): pass
    if not pyfont or not pyfont.get_init():
        return NoneFont()

    fullname = os.path.join(font_dir, name)

    try:
        font = pyfont.Font(fullname, size)
    except error:
        print('Cannot load font: %s' % fullname)
        raise SystemExit(str(geterror()))
    return font


class MyFont:
    def __init__(self, screen, font, text='', center_position=(10, 10),
                 anti_alias=True, color=WHITE, background=None, visible=True):
        self.font = font
        self.anti_alias = anti_alias
        self.color = color
        self.background = background
        self.text = text
        self.render = self.font.render(text, anti_alias, color, background)
        self.screen = screen
        self.rect = self.render.get_rect()
        self.rect.center = center_position
        self.visible = visible

    def blit(self):
        if self.visible:
            self.screen.blit(self.render, (self.rect[0], self.rect[1]))

    def move_center(self, center_position):
        self.rect.center = center_position

    def move(self, position):
        self.rect.move(position)

    def change_text(self, text):
        self.text = text
        self.change_render()

    def change_font(self, font):
        self.font = font
        self.change_render()

    def change_color(self, color):
        self.color = color
        self.change_render()

    def change_render(self):
        self.render = self.font.render(self.text, self.anti_alias, self.color, self.background)

    def set_visible(self, visible=True):
        self.visible = visible

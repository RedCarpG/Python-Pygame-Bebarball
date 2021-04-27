import pygame, os
from GLOBAL import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
font_dir = os.path.join(main_dir, 'font')

def load_font(name, size):
    class NoneFont:
        def play(self): pass
    if not pygame.font or not pygame.font.get_init():
        return NoneFont()
    fullname = os.path.join(font_dir, name)
    try:
        font = pygame.font.Font(fullname, size)
    except pygame.error:
        print ('Cannot load font: %s' % fullname)
        raise SystemExit(str(geterror()))
    return font

class myFont:
    def __init__(self, screen, font, text='', center_positon=(10,10), antialias=True, color=WHITE, background=None):
        self.font = font
        self.antialias = antialias
        self.color = color
        self.background = background
        self.text = text
        self.render = self.font.render(self.text, self.antialias, self.color, self.background)        
        self.screen = screen
        self.rect = self.render.get_rect()
        self.rect.center = center_positon
    def blit(self):
        self.screen.blit(self.render, (self.rect[0], self.rect[1]))
    def move_center(self, center_positon):
        self.rect.center = center_positon
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
        self.render = self.font.render(self.text, self.antialias, self.color, self.background)
# Texture Manager - Mc_snurtle
# imports
import pygame
pygame.init()


class Textures(dict):
    
    def __init__(self, screen):
        
        self.screen = screen
        
        self.car = {
            'car': {
                'car-w': pygame.image.load('res/car-W.png').convert_alpha(),
                'car-sw': pygame.image.load('res/car-SW.png').convert_alpha(),
                'car-s': pygame.image.load('res/car-S.png').convert_alpha(),
                'car-se': pygame.image.load('res/car-SE.png').convert_alpha(),
                'car-e': pygame.image.load('res/car-E.png').convert_alpha(),
                'car-ne': pygame.image.load('res/car-NE.png').convert_alpha(),
                'car-n': pygame.image.load('res/car-N.png').convert_alpha(),
                'car-nw': pygame.image.load('res/car-NW.png').convert_alpha()
                },
            'jeep': {
                'jeep-w': pygame.image.load('res/jeep-W.png').convert_alpha(),
                'jeep-sw': pygame.image.load('res/jeep-SW.png').convert_alpha,
                'jeep-s': pygame.image.load('res/jeep-S.png').convert_alpha(),
                'jeep-se': pygame.image.load('res/jeep-SE.png').convert_alpha(),
                'jeep-e': pygame.image.load('res/jeep-E.png').convert_alpha(),
                'jeep-ne': pygame.image.load('res/jeep-NE.png').convert_alpha(),
                'jeep-n': pygame.image.load('res/jeep-N.png').convert_alpha(),
                'jeep-nw': pygame.image.load('res/jeep-NW.png').convert_alpha()
                }
            }
        self.tile = {
            'transitions': {
                'grass_blend': pygame.image.load('res/tile/grass_blend.png').convert_alpha(),
                'grass_blend-side': pygame.image.load('res/tile/grass_blend-angle.png').convert_alpha(),
                'dirt_blend-side': pygame.image.load('res/tile/dirt_blend-side.png').convert_alpha(),
                'dirt_blend-top': pygame.image.load('res/tile/dirt_blend-top.png').convert_alpha(),
                'dirt_blend-top-flip': pygame.image.load('res/tile/dirt_blend-top-flip.png').convert_alpha(),
                'dirt_blend-side-flip': pygame.image.load('res/tile/dirt_blend-side-flip.png').convert_alpha(),
                },
            'animations': {
                'water': [pygame.image.load('res/tile/water1.png').convert(),
                          pygame.image.load('res/tile/water2.png').convert(),
                          pygame.image.load('res/tile/water3.png').convert(),
                          pygame.image.load('res/tile/water4.png').convert(),
                          pygame.image.load('res/tile/water5.png').convert()
                          ],
                'grass_blades': {
                    'grass1': None,
                    },
                },
            'textures': {    
                'grass': pygame.image.load('res/tile/grass-64.png').convert(),
                'grass-side': pygame.image.load('res/tile/grass-side-64.png').convert(),
                'dirt': pygame.image.load('res/tile/dirt-64.png').convert(),
                'road': pygame.image.load('res/tile/road-64.png').convert(),
                'hill': pygame.image.load('res/tile/hill.png').convert_alpha(),
                'boulder': pygame.image.load('res/tile/boulder-64.png').convert_alpha()
                }
            }
        self.gui = {
            'gauge': {
                'background': pygame.image.load('res/gauge/gauge-clean.png').convert_alpha(),
                'speed_needle': pygame.image.load('res/gauge/speed_needle.png').convert_alpha(),
                'vector_needle': pygame.image.load('res/gauge/raw_speed_needle.png').convert_alpha(),
                'steer_needle': pygame.image.load('res/gauge/steer_needle.png').convert_alpha(),
                'drift_needle': pygame.image.load('res/gauge/drift_needle.png').convert_alpha()
                },
            'menu': {
                'backgrounds': {
                    'main_menu': None
                    }
                }    
            }

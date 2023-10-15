# Texture Manager - Mc_snurtle
# imports
import os
from PIL import Image


class Textures(dict):
    
    def __init__(self, screen):
        
        self.screen = screen
        self.image_dir = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir)), 'res')
        
        self.car = {
            'car': {
                'car-w': PNG(os.path.join(self.image_dir, 'car-W.png')),
                'car-sw': PNG(os.path.join(self.image_dir, 'car-SW.png')),
                'car-s': PNG(os.path.join(self.image_dir, 'car-S.png')),
                'car-se': PNG(os.path.join(self.image_dir, 'car-SE.png')),
                'car-e': PNG(os.path.join(self.image_dir, 'car-E.png')),
                'car-ne': PNG(os.path.join(self.image_dir, 'car-NE.png')),
                'car-n': PNG(os.path.join(self.image_dir, 'car-N.png')),
                'car-nw': PNG(os.path.join(self.image_dir, 'car-NW.png'))
                },
            'jeep': {
                'jeep-w': PNG(os.path.join(self.image_dir, 'jeep-W.png')),
                'jeep-sw': PNG(os.path.join(self.image_dir, 'jeep-SW.png')),
                'jeep-s': PNG(os.path.join(self.image_dir, 'jeep-S.png')),
                'jeep-se': PNG(os.path.join(self.image_dir, 'jeep-SE.png')),
                'jeep-e': PNG(os.path.join(self.image_dir, 'jeep-E.png')),
                'jeep-ne': PNG(os.path.join(self.image_dir, 'jeep-NE.png')),
                'jeep-n': PNG(os.path.join(self.image_dir, 'jeep-N.png')),
                'jeep-nw': PNG(os.path.join(self.image_dir, 'jeep-NW.png'))
                }
            }
        self.tile = {
            'transitions': {
                'grass_blend': PNG(os.path.join(self.image_dir, 'tile', 'grass_blend.png')),
                'grass_blend-side': PNG(os.path.join(self.image_dir, 'tile', 'grass_blend-angle.png')),
                'dirt_blend-side': PNG(os.path.join(self.image_dir, 'tile', 'dirt_blend-side.png')),
                'dirt_blend-top': PNG(os.path.join(self.image_dir, 'tile', 'dirt_blend-top.png')),
                'dirt_blend-top-flip': PNG(os.path.join(self.image_dir, 'tile', 'dirt_blend-top-flip.png')),
                'dirt_blend-side-flip': PNG(os.path.join(self.image_dir, 'tile', 'dirt_blend-side-flip.png')),
                },
            'animations': {
                'water': [PNG(os.path.join(self.image_dir, 'tile', 'water1.png')),
                          PNG(os.path.join(self.image_dir, 'tile', 'water2.png')),
                          PNG(os.path.join(self.image_dir, 'tile', 'water3.png')),
                          PNG(os.path.join(self.image_dir, 'tile', 'water4.png')),
                          PNG(os.path.join(self.image_dir, 'tile', 'water5.png'))
                          ],
                'grass_blades': {
                    'grass1': None,
                    },
                },
            'textures': {    
                'grass': PNG(os.path.join(self.image_dir, 'tile', 'grass-64.png')),
                'grass-side': PNG(os.path.join(self.image_dir, 'tile', 'grass-side-64.png')),
                'dirt': PNG(os.path.join(self.image_dir, 'tile', 'dirt-64.png')),
                'road': PNG(os.path.join(self.image_dir, 'tile', 'road-64.png')),
                'hill': PNG(os.path.join(self.image_dir, 'tile', 'hill.png')),
                'boulder': PNG(os.path.join(self.image_dir, 'tile', 'boulder-64.png'))
                }
            }
        self.gui = {
            'gauge': {
                'background': PNG(os.path.join(self.image_dir, 'gauge', 'gauge-clean.png')),
                'speed_needle': PNG(os.path.join(self.image_dir, 'gauge', 'speed_needle.png')),
                'vector_needle': PNG(os.path.join(self.image_dir, 'gauge', 'raw_speed_needle.png')),
                'steer_needle': PNG(os.path.join(self.image_dir, 'gauge', 'steer_needle.png')),
                'drift_needle': PNG(os.path.join(self.image_dir, 'gauge', 'drift_needle.png'))
                },
            'menu': {
                'backgrounds': {
                    'main_menu': None
                    }
                }    
            }


class PNG:

    def __init__(self, path: str):

        self.path = path
        self.image = Image.open(self.path)

    def get_width(self):
        return self.image.width

    def get_height(self):
        return self.image.height

    def get_size(self):
        return (self.get_width(), self.get_height())

    def copy(self):
        return self

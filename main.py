# imports
from calendar import c
import math
import json
import numpy as np
from managers.texture import Textures
from managers.animation import AnimManager
from managers.map import MapLoader

import pygame
pygame.init()
pygame.joystick.init()


class SkidManager:

    def __init__(self, max_age: int):
        
        self.SKID_MARK_MAX_AGE = max_age
        self.SKID_COL = (0, 0, 0, 1)
        self.skid_marks = []

    def calc_skids(self, car_x: int, car_y: int, drift_angle: int, car_angle: int) -> list:
        
         # Add skid mark at each wheel position of the car's current position if drifting
        if abs(drift_angle) > 15.0:
            wheel_positions = [
            (12, 14),  # Front left wheel position relative to car center
            (-12, 14),  # Front right wheel position relative to car center
            (12, -14),  # Rear left wheel position relative to car center
            (-12, -14)  # Rear right wheel position relative to car center
        ]

            car_angle_rad = math.radians(car_angle)

            for wheel_position in wheel_positions:
                wheel_x = car_x + (wheel_position[0]) * math.cos(car_angle_rad) - wheel_position[1] * math.sin(car_angle_rad)
                wheel_y = car_y + (wheel_position[0]) * math.sin(car_angle_rad) + wheel_position[1] * math.cos(car_angle_rad)
                self.skid_marks.append((wheel_x, wheel_y, self.SKID_MARK_MAX_AGE, self.SKID_COL))

        # Update skid marks and remove old ones
        updated_skid_marks = []
        for mark in self.skid_marks:
            x, y, age, color = mark
            age -= 1
            if age > 0:
                updated_skid_marks.append((x, y, age, color))
        self.skid_marks = updated_skid_marks
        return self.skid_marks


class Screen(pygame.Surface):
    
    def __init__(self, width, height):
    
        super().__init__((width, height))
        self.width, self.height = width, height
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.car_name = 'car'
        self.skid_manager = SkidManager(150)
        self.animanager = AnimManager(frame_duration=350)
        self.textures = Textures(self.screen)

        
        # Map Properties
        self.map = MapLoader('dirty_dancing')
        self.distance_map = None
        self.perspective = 55
        self.tile_width = 90
        self.current_tile = None
        self.tile_height = self.perspective

        # Gauge properties
        self.gauge_padding = 20
        self.gauge_x = self.gauge_padding
        self.gauge_y = self.height - self.textures.gui['gauge']['background'].get_height() - self.gauge_padding
        self.speedometer_rect = pygame.Rect(self.gauge_x, self.gauge_y, self.textures.gui['gauge']['background'].get_width(), self.textures.gui['gauge']['background'].get_height())
        
        # Controller properties
        self.joystick = None
        if pygame.joystick.get_count() != 0:        # If there are more than 0 controllers connected
            self.joystick = pygame.joystick.Joystick(0) # Use the first one that is
            self.joystick.init()

        # Car properties
        self.car_mirror = self.textures.car['car']['car-e'].copy()
        self.CAR_X = self.map.SPAWN[0] * self.tile_width
        self.CAR_Y = self.map.SPAWN[1] * self.tile_height
        self.PREV_X = self.CAR_X
        self.PREV_Y = self.CAR_Y
        self.CAR_SPEED = 2
        self.CAR_ANGLE = 0
        self.MOM_DECAY = 0.0245
        self.TOP_MOM = 7.0
        self.CAR_DIRECTION = 'car-e'
        self.THROTTLE_MUL = 0.155
        self.STEER_THRESH = 230.0
        self.CAR_WIDTH, self.CAR_HEIGHT = self.car_mirror.get_size()

        # Drift properties
        self.DRIFT_ANGLE = 0
        self.DRIFT_MUL = 0.06
        self.DRIFT_THRESH = 2.0
        self.MAX_DRIFT_ANGLE = 90.0

        # Material properties
        self.ROAD_FRICTION = 2
        self.ROAD_SPEED = 8.0
            
        self.DIRT_FRICTION = 5       # Drift angle multiplier while on the material
        self.DIRT_SPEED = 7.0        # Maximum speed while on the material

        self.GRASS_FRICTION = 15
        self.GRASS_SPEED = 2.0

        self.WATER_FRICTION = 50.0
        self.WATER_SPEED = 1.0

    def run(self):
        while self.running:
            self.event_handler()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(75)

    def event_handler(self):
        
        # Before any calculations, check the material
        tile_x = int(self.CAR_X // self.tile_width)
        tile_y = int(self.CAR_Y // self.tile_height)

        try:
            self.current_tile = self.map.LAYOUT[tile_y][tile_x]
        
            if self.current_tile == '#':                
                self.skid_manager.SKID_COL = (15, 20, 25)
                material_friction = self.ROAD_FRICTION
                self.TOP_MOM = self.ROAD_SPEED
            elif self.current_tile == '@':
                self.skid_manager.SKID_COL = (50, 40, 40)
                material_friction = self.DIRT_FRICTION
                self.TOP_MOM = self.DIRT_SPEED
            elif self.current_tile == '.':
                self.skid_manager.SKID_COL = (65, 65, 45)
                material_friction = self.GRASS_FRICTION
                self.TOP_MOM = self.GRASS_SPEED
            else:   # Anything else, it's gotta be water
                self.skid_manager.SKID_COL = (190, 190, 190)
                material_friction = self.WATER_FRICTION
                self.TOP_MOM = self.WATER_SPEED
        
        except IndexError:                              # Travelled out of bounds
            material_friction = self.GRASS_FRICTION      # Set the material stats to the default road
            self.TOP_MOM = self.GRASS_SPEED

        # Controller event listener
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.joystick.quit()
                
        if self.joystick is not None:

            x_axis = self.joystick.get_axis(0)
            lt_axis = self.joystick.get_axis(4)
            rt_axis = self.joystick.get_axis(5)            

            if abs(x_axis) > 0.2 and self.CAR_SPEED > 0.5:
                self.CAR_ANGLE += x_axis * 2.6
                if self.DRIFT_ANGLE < self.MAX_DRIFT_ANGLE:
                    self.DRIFT_ANGLE -= x_axis * material_friction
            else:
                if self.DRIFT_ANGLE > 0:
                    self.DRIFT_ANGLE -= 1.0
                elif self.DRIFT_ANGLE < 0:
                    self.DRIFT_ANGLE += 1.0
                        
            if (lt_axis + 1.0 / 2.0) > 0.2:
                self.CAR_SPEED -= (lt_axis + 1.0) / 15.0
            if (rt_axis + 1.0 / 2.0) > 0.2 and self.CAR_SPEED < self.TOP_MOM:
                self.CAR_SPEED += (rt_axis + 1.0) / 12.0
            else:
                self.CAR_SPEED -= self.MOM_DECAY * 5.0

        # Keyboard event listener
        elif self.joystick is None:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] and self.CAR_SPEED > 0.5:
                self.CAR_ANGLE -= 3
                if self.DRIFT_ANGLE < 0:
                    self.DRIFT_ANGLE += 5.0
                else:
                    if self.DRIFT_ANGLE < self.MAX_DRIFT_ANGLE:
                        self.DRIFT_ANGLE += 1.0 * material_friction
            elif keys[pygame.K_d] and self.CAR_SPEED > 0.5:
                self.CAR_ANGLE += 3
                if self.DRIFT_ANGLE > 0:
                    self.DRIFT_ANGLE -= 5.0
                else:
                    if self.DRIFT_ANGLE > -self.MAX_DRIFT_ANGLE:
                        self.DRIFT_ANGLE -= 1.0 * material_friction
            else:
                if self.DRIFT_ANGLE > 0:
                    self.DRIFT_ANGLE -= 1.0
                elif self.DRIFT_ANGLE < 0:
                    self.DRIFT_ANGLE += 1.0

            if keys[pygame.K_w] and self.CAR_SPEED < self.TOP_MOM and self.current_tile != 'O':
                self.CAR_SPEED += self.THROTTLE_MUL
            if keys[pygame.K_s]:
                self.CAR_SPEED -= (self.THROTTLE_MUL * 0.5)
            else:
                self.CAR_SPEED -= self.MOM_DECAY

        self.CAR_SPEED = max(0, self.CAR_SPEED)
        self.DRIFT_ANGLE = max(-self.MAX_DRIFT_ANGLE, min(self.MAX_DRIFT_ANGLE, self.DRIFT_ANGLE))  # Clamp the drift angle

    def calculate_grass_distance(self, x, y):
        # Calculate the distance from the grass tile at (x, y) to the nearest road or water tile
        min_distance = float(15.0)

        for j, row in enumerate(self.map.LAYOUT):
            for i, tile in enumerate(row):
                if tile in ['#', '@']:  # Road or water tile
                    distance = abs(x - i) + abs(y - j)  # Manhattan distance
                    min_distance = min(min_distance, distance)

    def update(self):
        self.PREV_X = self.CAR_X
        self.PREV_Y = self.CAR_Y
        
        car_angle_rad = math.radians(self.CAR_ANGLE)

        self.swap_car_sprite()

        # Calculate the new car position based on angle and speed
        car_angle_rad = math.radians(self.CAR_ANGLE)
        new_x = self.CAR_X + self.CAR_SPEED * math.cos(car_angle_rad)
        new_y = self.CAR_Y + self.CAR_SPEED * math.sin(car_angle_rad) * (self.perspective * 0.01)
        
        # Add sideways drift effect
        drift_angle_rad = math.radians(self.CAR_ANGLE + self.DRIFT_ANGLE)   
        drift_x = 0
        drift_y = 0
        if self.DRIFT_ANGLE > 0:
            drift_x = (self.DRIFT_ANGLE * 0.01) * (self.CAR_SPEED) * math.cos(drift_angle_rad)
            drift_y = (self.DRIFT_ANGLE * 0.01) * (self.CAR_SPEED) * math.sin(drift_angle_rad) * (self.perspective * 0.01)
        elif self.DRIFT_ANGLE < 0:
            drift_x = (-self.DRIFT_ANGLE * 0.01) * (self.CAR_SPEED) * math.cos(drift_angle_rad)
            drift_y = (-self.DRIFT_ANGLE * 0.01) * (self.CAR_SPEED) * math.sin(drift_angle_rad) * (self.perspective * 0.01)

        # Calculate the new car position with drift
        new_x += drift_x
        new_y += drift_y

        # Check for screen boundary collisions
        self.CAR_X = new_x
        self.CAR_Y = new_y
        
        self.camera_x = self.CAR_X - self.width / 2
        self.camera_y = self.CAR_Y - self.height / 2

    def swap_car_sprite(self):
        
        # Determine the car direction based on the angle
        angle = self.CAR_ANGLE % 360  # Ensure the angle is within [0, 360]

        if 45 <= angle < 90:
            self.CAR_DIRECTION = 'se'
        elif 90 <= angle < 135:
            self.CAR_DIRECTION = 's'
        elif 135 <= angle < 180:
            self.CAR_DIRECTION = 'sw'
        elif 180 <= angle < 225:
            self.CAR_DIRECTION = 'w'
        elif 225 <= angle < 270:
            self.CAR_DIRECTION = 'nw'
        elif 270 <= angle < 315:
            self.CAR_DIRECTION = 'n'
        elif 315 <= angle < 355:
            self.CAR_DIRECTION = 'ne'
        else:
            self.CAR_DIRECTION = 'e'

    def draw(self):
        # grass_rect = pygame.Rect(1, 1, self.width - 1, self.height - 1)
        # texture = pygame.transform.scale(self.tile_textures['grass'], (self.width, self.height))
        # self.screen.blit(texture, grass_rect)  # Fill the screen surface with the background color
        self.screen.fill((0, 0, 0))

        self.draw_tiles()

        car_x_rel = self.CAR_X - self.camera_x
        car_y_rel = self.CAR_Y - self.camera_y
        
        # Draw skid marks on the screen with alpha and in black color
        for mark in self.skid_manager.calc_skids(self.CAR_X, self.CAR_Y, self.DRIFT_ANGLE, self.CAR_ANGLE):
            x, y, age, color = mark
            screen_x = x - self.CAR_X + self.width / 2
            screen_y = y - self.CAR_Y + self.height / 2
            # alpha = int(255 * (age / self.SKID_MARK_MAX_AGE) * 0.2)
            pygame.draw.circle(self.screen, color, (int(screen_x), int(screen_y)), 3)


        # Rotate the car image and draw it on the screen
        car_texture = self.textures.car[self.car_name][self.car_name+'-'+self.CAR_DIRECTION]

        car_rect = car_texture.get_rect(center=(car_x_rel, car_y_rel))
        self.screen.blit(car_texture, car_rect.topleft)
        
        self.draw_fps()
        self.draw_speedometer()

    def draw_tiles(self):
        
        # Draw the map based on the map_layout
        
        for y, row in enumerate(self.map.LAYOUT):
            for x, tile in enumerate(row):
                if 0 <= y * self.tile_height >= self.camera_y - self.tile_height and 0 <= x * self.tile_width >= self.camera_x - self.tile_width:
                    tile_rect = pygame.Rect(x * self.tile_width - self.camera_x, y * self.tile_height - self.camera_y, self.tile_width, self.tile_height)

                    if tile == '#':  # Road tile
                        decoration = None
                        color =  self.textures.tile['textures']['road']
                        color = pygame.transform.rotate(color, 90)
                    elif tile == '@':   # Dirt tile
                        decoration = None
                        color = self.textures.tile['textures']['dirt']
                    elif tile == '.':
                        decoration = None
                        color = self.textures.tile['textures']['grass']
                    elif tile == 'O':
                        color = self.textures.tile['textures']['grass']
                        decoration = self.textures.tile['textures']['boulder']
                    else:
                        color = self.animanager.calc_frame(self.textures.tile['animations']['water'])
                        decoration = None

                    color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                    self.screen.blit(color, tile_rect)
                    if decoration is not None:
                        decoration = pygame.transform.scale(decoration, (self.tile_width, self.tile_height))
                        self.screen.blit(decoration, tile_rect)

                    # Draw connected textures
                    if tile == '@' and self.map.LAYOUT[y][x-1] == '#':  # Road left of dirt
                        color = self.textures.tile['transitions']['dirt_blend-side']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        self.screen.blit(color, tile_rect)
                    if tile == '@' and self.map.LAYOUT[y-1][x] == '#':  # Road above dirt
                        color = self.textures.tile['transitions']['dirt_blend-top']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        self.screen.blit(color, tile_rect)
                    if tile == '@' and self.map.LAYOUT[y+1][x] == '#':  # Road below dirt
                        color = self.textures.tile['transitions']['dirt_blend-top-flip']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        self.screen.blit(color, tile_rect)
                    if tile == '@' and self.map.LAYOUT[y][x+1] == '#':  # Road right of dirt
                        color = self.textures.tile['transitions']['dirt_blend-side-flip']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        self.screen.blit(color, tile_rect)
                    if tile != '.' and self.map.LAYOUT[y-1][x] == '.':
                        color = self.textures.tile['transitions']['grass_blend']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        self.screen.blit(color, tile_rect)
                    if tile != '.' and self.map.LAYOUT[y][x-1] == '.' and self.map.LAYOUT[y-1][x] == '.':
                        color = self.textures.tile['transitions']['grass_blend-side']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        color = pygame.transform.rotate(color, 90)
                        self.screen.blit(color, tile_rect)
                    elif tile != '.' and self.map.LAYOUT[y][x-1] == '.' and self.map.LAYOUT[y-1][x] != '.':
                        color = self.textures.tile['transitions']['grass_blend']
                        color = pygame.transform.scale(color, (self.tile_width, self.tile_height))
                        color = pygame.transform.rotate(color, 90)
                        self.screen.blit(color, tile_rect)

    def draw_speedometer(self):
        # Gauge the Gauge Textures
        self.screen.blit(self.textures.gui['gauge']['background'], self.speedometer_rect.topleft)

        # Calculate the angle for the speedometer needle based on car speed
        max_speed = 8.0
        min_angle = 0
        max_angle = 180
        current_speed = self.CAR_SPEED * 1.5
        raw_speed = ((self.CAR_X - self.PREV_X) ** 2 + (self.CAR_Y - self.PREV_Y) ** 2) ** 0.5 * 1.5
        angle_range = max_angle - min_angle
        angle = min_angle - (current_speed / max_speed) * angle_range
        raw_angle = (min_angle - (raw_speed / max_speed) * angle_range)

        # Create a rotated needle image
        rotated_needle = pygame.transform.rotate(self.textures.gui['gauge']['speed_needle'], angle)
        rotated_raw_needle = pygame.transform.rotate(self.textures.gui['gauge']['vector_needle'], raw_angle)

        # Calculate the position for the needle
        needle_x = self.speedometer_rect.centerx - rotated_needle.get_width() // 2
        needle_y = self.speedometer_rect.centery - rotated_needle.get_height() // 2
        raw_needle_x = self.speedometer_rect.centerx - rotated_raw_needle.get_width() // 2
        raw_needle_y = self.speedometer_rect.centery - rotated_raw_needle.get_height() // 2
        needle_position = (needle_x, needle_y)
        raw_needle_position = (raw_needle_x, raw_needle_y)

        # Draw the rotated needle
        self.screen.blit(rotated_needle, needle_position)
        self.screen.blit(rotated_raw_needle, raw_needle_position)

    def draw_fps(self):
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (self.width - 10, 10)
        self.screen.blit(fps_text, fps_rect)
        

if __name__ == '__main__':
    screen = Screen(2560//2, 1440//2)

    screen.run()

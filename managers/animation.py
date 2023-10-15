# Animation Manager - Mc_Snurtle
# imports
import pygame
pygame.init()


class AnimManager:

    def __init__(self, frame_duration: int):
        
        self.FRAME_DURATION = frame_duration
        self.CURRENT_FRAME = 0
        self.FRAME_TIMER = 0
        self.LAST_FRAME_TIME = pygame.time.get_ticks()

    def calc_frame(self, frames: list):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.LAST_FRAME_TIME > self.FRAME_DURATION:
            self.CURRENT_FRAME = (self.CURRENT_FRAME + 1) % len(frames)
            self.LAST_FRAME_TIME = current_time

        return frames[self.CURRENT_FRAME]


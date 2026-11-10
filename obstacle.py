import pygame as pg
import random

class Obstacle:

    def __init__(self, pos, color, width, height, window):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height
        self.window = window
    
    def draw(self):
        pg.draw.rect(self.window, self.color, (self.pos[0], self.pos[1], self.width, self.height))
    
def create_obstacle(window, window_width, window_height, obstacle_list):
    width = random.randint(20, 40)
    height = random.randint(20, 40)

    pos = pg.math.Vector2(random.randint(0, window_width - width), random.randint(0, window_height - height))

    obstacle = Obstacle(pos, (255, 255, 255), width, height, window)
    obstacle_list.append(obstacle)
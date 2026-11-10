import pygame as pg
from obstacle import Obstacle, create_obstacle
from moving_object import Boids, Hoiks

pg.init()

klokke = pg.time.Clock()

window_width = 1000
window_height = 600
window = pg.display.set_mode((window_width, window_height))

obstacle_list = []

# Add boids, hoiks and obstacles
boid_group = pg.sprite.Group()
for _ in range(150):
    boid_group.add(Boids(window, obstacle_list))
hoik_group = pg.sprite.Group()
for _ in range(3):
    hoik_group.add(Hoiks(window, obstacle_list))
for _ in range(3):
    create_obstacle(window, window_width, window_height, obstacle_list)

while True:
    event = pg.event.poll()
    if event.type == pg.QUIT:
        break
    # Paints background black
    window.fill((0, 0, 0))

    boid_group.update(boid_group, hoik_group, obstacle_list)
    boid_group.draw(window)

    hoik_group.update(boid_group)
    hoik_group.draw(window)

    for obstacle in obstacle_list:
        obstacle.draw()

    # Sets framerate
    klokke.tick(60)  # 60 fps

    pg.display.update()
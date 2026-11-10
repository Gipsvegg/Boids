import pygame as pg
import random

BOID_FILENAME = "sirkel.png"
HOIK_FILENAME = "Pan_Blue_Circle.png"

boid_img = pg.image.load(BOID_FILENAME)
boid_img = pg.transform.scale(boid_img, (20, 20))
hoik_img = pg.image.load(HOIK_FILENAME)
hoik_img = pg.transform.scale(hoik_img, (20, 20))

class Moving_object(pg.sprite.Sprite):

    def __init__(self, window, obstacle_list):
        super().__init__()
        self.width = 20
        self.height = 20
        self.pos = pg.math.Vector2(random.randint(0, 1000 - self.width), random.randint(0, 600 - self.height))
        self.window = window
        self.obstacle_list = obstacle_list
        self.speed = pg.math.Vector2(random.uniform(-1, 1),random.uniform(-1, 1))
        self.rect = pg.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
    
    def collision(self):
        # Puts moving objekt on the other side of the screen if the objekt hits the edge
        if self.pos[0] < 0:
            self.pos[0] = self.window.get_width() - self.width
        if self.pos[0] > self.window.get_width() - self.width:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = self.window.get_height() - self.height
        if self.pos[1] > self.window.get_height() - self.height:
            self.pos[1] = 0
        
        # Obstacle collision
        for obstacle in self.obstacle_list:
            obstacle_hitbox = pg.Rect(obstacle.pos[0], obstacle.pos[1], obstacle.width, obstacle.height)
            if self.rect.colliderect(obstacle_hitbox):
                self.kill()



class Boids(Moving_object):

    def __init__(self, window, obstacle_list):
        super().__init__(window, obstacle_list)
        self.image = boid_img
        self.rect = self.image.get_rect(topleft=(self.pos[0], self.pos[1]))

    def update(self, boid_group, hoik_group, obstacle_list):
        self.pos = self.pos + self.speed
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.speed += self.separation(boid_group)
        self.speed += self.cohesion(boid_group)
        self.speed += self.alignment(boid_group)
        self.speed += self.avoid_obstacle(obstacle_list)
        if self.speed.length() != 0:
            self.speed.clamp_magnitude_ip(0.1, 1)
        self.collision()
        self.hoik_collision(hoik_group)
    
    def hoik_collision(self, hoik_group):
        for hoik in hoik_group:
            if self.rect.colliderect(hoik.rect):
                self.kill()
    
    def separation(self, boid_group):
        seperation_factor = 5  # How much separation velocity affects boids
        number_to_avoid = 0
        seperation_velocity = pg.math.Vector2(0, 0)
        # Loops through every boid
        for boid in boid_group:
            # Disregard self
            if boid is self:
                continue
            distance = self.pos.distance_to(boid.pos)  # Distance between self and boid
            if distance < 200:
                distance_vector = self.pos - boid.pos
                if distance_vector.length() != 0:
                    travel = distance_vector.normalize()
                    weighted_vel = travel / (distance + 0.01)
                else:
                        weighted_vel = pg.math.Vector2(0,0)
                seperation_velocity += weighted_vel
                number_to_avoid += 1
        if number_to_avoid > 0:
            seperation_velocity = seperation_velocity / number_to_avoid
        if seperation_velocity.length() != 0:
            seperation_velocity.normalize_ip()
        seperation_velocity *= seperation_factor
        return seperation_velocity

    def alignment(self, boid_group):
        alignment_factor = 5  # How aligned boids are
        average_speed = pg.math.Vector2()
        number_of_boids = 0
        for boid in boid_group:
            # Disregard self
            if boid is self:
                continue
            distance = self.pos.distance_to(boid.pos)  # Distance between self and boid
            # Finds average speed of nearby boids
            if distance < 50:
                number_of_boids += 1
                average_speed += boid.speed
        if number_of_boids > 0:
            average_speed = average_speed / number_of_boids
        # Points boid in direction of average speed
        direction = average_speed - self.speed
        if direction.length() != 0:
            direction.normalize_ip()
        direction *= alignment_factor
        return direction

    def cohesion(self, boid_group):
        cohesion_factor = 0.001  # How cohesive boids are
        average_pos = pg.math.Vector2()
        number_of_boids = 0
        for boid in boid_group:
            # Disregard self
            if boid is self:
                continue
            distance = self.pos.distance_to(boid.pos)  # Distance between self and boid
            # Finds average position of nearby boids
            if distance < 150:
                number_of_boids += 1
                average_pos += boid.pos
        if number_of_boids > 0:
            average_pos = average_pos / number_of_boids
        # Points boid in direction of nearby boids
        direction = average_pos - self.pos
        if direction.length() != 0:
            direction.normalize_ip()
        direction *= cohesion_factor
        return direction

    def avoid_obstacle(self, obstacle_list):
        avoid_factor = 4  # How much avoid velocity affects boids
        number_to_avoid = 0
        avoid_velocity = pg.math.Vector2(0, 0)
        for obstacle in obstacle_list:
            distance = self.pos.distance_to(obstacle.pos)  # Distance between self and obstacle
            if distance < 40:
                distance_vector = self.pos - obstacle.pos
                if distance_vector.length() != 0:
                    travel = distance_vector.normalize()
                    weighted_vel = travel / (distance + 0.01)
                else:
                        weighted_vel = pg.math.Vector2(0,0)
                avoid_velocity += weighted_vel
                number_to_avoid += 1
        if number_to_avoid > 0:
            avoid_velocity = avoid_velocity / number_to_avoid
        if avoid_velocity.length() != 0:
            avoid_velocity.normalize_ip()
        avoid_velocity *= avoid_factor
        return avoid_velocity

class Hoiks(Moving_object):
    
    def __init__(self, window, obstacle_list):
        super().__init__(window, obstacle_list)
        self.image = hoik_img
        self.rect = self.image.get_rect(topleft=(self.pos[0], self.pos[1]))

    def update(self, boid_group):
        self.pos = self.pos + self.speed
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.speed += self.eat(boid_group)
        if self.speed.length() != 0:
            self.speed.clamp_magnitude_ip(0.1, 1)
        self.collision()
    
    def eat(self, boid_group):
        nearest_boid = None
        nearest_boid_distance = 100
        for boid in boid_group:
            distance = self.pos.distance_to(boid.pos)  # Distance between self and boid

            # Find nearest boid
            if distance < nearest_boid_distance:
                nearest_boid_distance = distance
                nearest_boid = boid.pos

        if nearest_boid is None:
            nearest_boid_distance = 100
            return pg.math.Vector2(0, 0)  # No boids to hunt
            
        direction = nearest_boid - self.pos
        if direction.length() != 0:
            direction.normalize_ip()
        return direction

import pygame
from objects import Wall, Door  # import Door so isinstance works

class Player:
    def __init__(self, x, y, size, speed, health=3):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.health = health

    def move(self, keys, walls, doors):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = self.speed

        # Move X-axis
        self.rect.x += dx
        for w in walls + doors:
            if (isinstance(w, Door) and w.hidden) or isinstance(w, Wall):
                if self.rect.colliderect(w.rect):
                    self.rect.x -= dx

        # Move Y-axis
        self.rect.y += dy
        for w in walls + doors:
            if (isinstance(w, Door) and w.hidden) or isinstance(w, Wall):
                if self.rect.colliderect(w.rect):
                    self.rect.y -= dy

        # Keep inside screen
        self.rect.x = max(0, min(self.rect.x, 640 - self.rect.width))
        self.rect.y = max(25, min(self.rect.y, 480 - self.rect.height))

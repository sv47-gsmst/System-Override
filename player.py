import pygame

class Player:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.moves = 0

    def move(self, keys):
        moved = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moved = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            moved = True
        if moved:
            self.moves += 1

    def undo_move(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x += self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x -= self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y += self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y -= self.speed

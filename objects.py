import pygame

# ------------------ WALL ------------------
class Wall:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

# ------------------ FAKE WALL ------------------
class FakeWall:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.discovered = False  # added: revealed when player touches

# ------------------ DOOR ------------------
class Door:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.hidden = True  # added: starts hidden
        self.open = False

    def reveal(self):
        self.hidden = False  # added: revealed
        self.open = True

# ------------------ SWITCH ------------------
class Switch:
    def __init__(self, x, y, size, linked_doors=None, linked_exits=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.linked_doors = linked_doors
        self.linked_exits = linked_exits
        self.active = False

    def try_activate(self, player_rect, keys):
        if player_rect.colliderect(self.rect) and keys[pygame.K_SPACE] and not self.active:  # added: activation check
            self.active = True
            if self.linked_doors:
                for door in self.linked_doors: door.reveal()  # added: reveal doors
            if self.linked_exits:
                for ex in self.linked_exits: ex.active = True  # added: activate exits

# ------------------ EXIT ------------------
class Exit:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.active = False  # added: starts inactive

# ------------------ GREEN TILE ------------------
class GreenTile:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

# ------------------ SHOOTER ENEMY ------------------
class ShooterEnemy:
    def __init__(self, x, y, size, speed=1):  # changed speed to 1 for slower enemy #added
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.bullets = []
        self.last_shot = 0

    def move_towards_player(self, player):
        if player.rect.x > self.rect.x: self.rect.x += self.speed
        elif player.rect.x < self.rect.x: self.rect.x -= self.speed
        if player.rect.y > self.rect.y: self.rect.y += self.speed
        elif player.rect.y < self.rect.y: self.rect.y -= self.speed

    def shoot(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_shot < 1000: return  # slower fire rate #added
        self.last_shot = now
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max((dx**2 + dy**2)**0.5, 1)
        speed = 3
        self.bullets.append({
            "rect": pygame.Rect(self.rect.centerx, self.rect.centery, 5, 5),
            "vx": dx / distance * speed,
            "vy": dy / distance * speed
        })

    def update_bullets(self, player, walls):
        for bullet in self.bullets[:]:
            bullet["rect"].x += bullet["vx"]
            bullet["rect"].y += bullet["vy"]

            if bullet["rect"].colliderect(player.rect):
                player.health -= 1  # added: reduce player health
                self.bullets.remove(bullet)
            elif any(bullet["rect"].colliderect(w.rect) for w in walls):
                self.bullets.remove(bullet)
            elif bullet["rect"].x < 0 or bullet["rect"].x > 640 or bullet["rect"].y < 0 or bullet["rect"].y > 480:
                self.bullets.remove(bullet)

import pygame

# ------------------
# WALL
# ------------------
class Wall:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

# ------------------
#    Fake Wall
# ------------------
class FakeWall:
    def __init__(self,x,y,size):
        self.rect = pygame.Rect(x, y, size, size)
        self.discovered = False


# ------------------
# DOOR
# ------------------
class Door:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.hidden = True
        self.open = False
    
    def reveal(self):
        self.hidden = False
        self.open = True

    def hide(self):
        self.hidden = True
        self.open = False

    def update(self):
        if switches:
            all_on = all(sw.active for sw in switches)
            if all_on:
                self.reveal
            else:
                self.hide()

# ------------------
# SWITCH
# ------------------
class Switch:
    def __init__(self, x, y, size, linked_doors=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.linked_doors = linked_doors or []
        self.active = False

    def try_activate(self, player_rect, keys):
        if player_rect.colliderect(self.rect) and keys[pygame.K_SPACE] and not self.active:
            self.active = True
            for door in self.linked_doors:
                door.reveal()

# ------------------
# EXIT
# ------------------
class Exit:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.active = False

# ------------------
# GREEN TILE (feedback)
# ------------------
class GreenTile:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.active = False

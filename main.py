import pygame
import sys
from player import Player
from objects import Wall, FakeWall, Door, Switch, Exit, GreenTile
from levels import levels

pygame.init()

WIDTH, HEIGHT = 640, 480
TILE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("System Override")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
PLAYER_COLOR = (50, 50, 255)
BLUE = (50, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 215, 0)
SWITCH_COLOR = (0, 0, 200)
SWITCH_ACTIVE = (0, 200, 255)
BLACK = (0, 0, 0)

# ------------------
# GAME STATES
# ------------------
MENU = "menu"
PLAYING = "playing"
state = MENU

# ------------------
# UI + TIMER
# ------------------
FONT_BIG = pygame.font.SysFont(None, 56)
FONT_UI = pygame.font.SysFont(None, 22)
LEVEL_TIME = 60  # seconds
timer_start = None

# ------------------
# GAME OBJECTS
# ------------------
current_level = 0
player = None
walls = []
fake_walls = []
doors = []
switches = []
green_tiles = []
exit_tile = None
green_tiles = []  # NEW: holds GreenTile objects for visual feedback

# ------------------
# LOAD LEVEL
# ------------------
def load_level(data):
    global player, walls, doors, switches, exit_tile, green_tiles, timer_start
    walls = []
    fake_walls = []
    doors = []
    switches = []
    green_tiles = []
    exit_tile = None
    player = None
    timer_start = pygame.time.get_ticks()  # NEW: reset timer

    for row_idx, row in enumerate(data):
        for col_idx, tile in enumerate(row):
            x, y = col_idx * TILE, row_idx * TILE
            if tile == "W":
                walls.append(Wall(x, y, TILE))
            elif tile == "F":
                fake_walls.append(FakeWall(x, y, TILE))
            elif tile == "P":
                player = Player(x, y, TILE, 5)
            elif tile == "D":
                doors.append(Door(x, y, TILE))
            elif tile == "S":
                switches.append(Switch(x, y, TILE, doors))
            elif tile == "E":
                exit_tile = Exit(x, y, TILE)
    if not player:
        player = Player(TILE, TILE, TILE, 5)  # default spawn if missing

    # NEW: create a green tile for each switch
    for sw in switches:
        green_tiles.append(GreenTile(sw.rect.x, sw.rect.y, TILE))

    print(f"Loaded Level {current_level + 1}")

load_level(levels[current_level])

# ------------------
# MAIN LOOP
# ------------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # ------------------
    # EVENT HANDLING
    # ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_level = 0
                load_level(levels[current_level])
                state = PLAYING

    if state == MENU:
        title = FONT_BIG.render("SYSTEM OVERRIDE", True, BLUE)
        prompt = pygame.font.SysFont(None, 28).render("Press SPACE to Start", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 240))
        pygame.display.flip()
        continue

    # ------------------
    # PLAYER INPUT
    # ------------------
    keys = pygame.key.get_pressed()
    if player:
        player.move(keys)

    # ------------------
    # COLLISIONS
    # ------------------
    for wall in walls:
        if player and player.rect.colliderect(wall.rect):
            player.undo_move(keys)
    
    for fw in fake_walls:
        if not fw.discovered and player.rect.colliderect(fw.rect):
            player.undo_move(keys)

    for door in doors:
        if door.hidden and player.rect.colliderect(door.rect):
            player.undo_move(keys)

    # ------------------
    # SWITCHES + GREEN TILES
    # ------------------
    for i, switch in enumerate(switches):
        if player:
            switch.try_activate(player.rect, keys)
        if switch.active:
            green_tiles[i].active = True

    # ------------------
    # DOOR LOGIC
    # ------------------
    all_on = all(sw.active for sw in switches) if switches else True
    for door in doors:
        door.hidden = not all_on

    # ------------------
    # EXIT LOGIC
    # ------------------
    if exit_tile:
        exit_tile.active = all_on
        if player and exit_tile.active and player.rect.colliderect(exit_tile.rect):
            current_level += 1
            if current_level < len(levels):
                load_level(levels[current_level])
            else:
                state = MENU

    # ------------------
    # DRAW LEVEL
    # ------------------
    for wall in walls:
        pygame.draw.rect(screen, RED, wall.rect)

    for fw in fake_walls:
        if not fw.discovered:
            pygame.draw.rect(screen, (120, 120, 120), fw.rect)

    for door in doors:
        color = GREEN if door.open else RED
        pygame.draw.rect(screen, color, door.rect)

    for switch in switches:
        color = SWITCH_ACTIVE if switch.active else SWITCH_COLOR
        pygame.draw.rect(screen, color, switch.rect)

    for tile in green_tiles:  # NEW: draw green tiles
        if tile.active:
            pygame.draw.rect(screen, GREEN, tile.rect)
    
    if exit_tile:
        color = YELLOW if exit_tile.active else (255, 230, 100)
        pygame.draw.rect(screen, color, exit_tile.rect)

    # ------------------
    # HUD
    # ------------------
    pygame.draw.rect(screen, (235, 235, 235), (0, 0, WIDTH, 40))
    pygame.draw.line(screen, BLACK, (0, 40), (WIDTH, 40), 2)

    # Level
    level_text = FONT_UI.render(f"Level: {current_level + 1}", True, BLACK)
    screen.blit(level_text, (10, 12))

    # Moves
    moves_text = FONT_UI.render(f"Moves: {player.moves}", True, BLACK)
    screen.blit(moves_text, (120, 12))

    # Timer
    elapsed = (pygame.time.get_ticks() - timer_start) // 1000 if timer_start else 0
    remaining = max(0, LEVEL_TIME - elapsed)
    timer_text = FONT_UI.render(f"Time: {remaining}", True, BLACK)
    screen.blit(timer_text, (240, 12))

    # Instructions
    help_text = FONT_UI.render("Move: WASD | Switch: SPACE", True, BLACK)
    screen.blit(help_text, (360, 12))

    # ------------------
    # DRAW PLAYER
    # ------------------
    if player:
        pygame.draw.rect(screen, PLAYER_COLOR, player.rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

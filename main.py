import pygame, time
from objects import *
from levels import LEVELS
from player import Player

# ------------------ INIT ------------------
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("System Override")
clock = pygame.time.Clock()
TILE_SIZE = 32
font = pygame.font.SysFont(None, 24)

# ------------------ PLAYER ------------------
player = Player(64, 64, TILE_SIZE-4, 4, health=3)  # added health parameter

# ------------------ GAME STATE ------------------
current_level = 0
level_start_time = time.time()
walls, fake_walls, doors, switches, exits, green_tiles, enemies = [], [], [], [], [], [], []

# ------------------ LOAD LEVEL ------------------
def load_level(index):
    global walls, fake_walls, doors, switches, exits, green_tiles, enemies, player, level_start_time
    walls, fake_walls, doors, switches, exits, green_tiles, enemies = [], [], [], [], [], [], []  # reset lists
    level_start_time = time.time()  # added: reset level timer
    layout = LEVELS[index]

    # First pass: create objects
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            px, py = x * TILE_SIZE, y * TILE_SIZE
            if tile == "W": walls.append(Wall(px, py, TILE_SIZE))
            elif tile == "F": fake_walls.append(FakeWall(px, py, TILE_SIZE))
            elif tile == "D": doors.append(Door(px, py, TILE_SIZE))
            elif tile == "S": switches.append(Switch(px, py, TILE_SIZE))  # added switch
            elif tile == "E": exits.append(Exit(px, py, TILE_SIZE))  # added exit
            elif tile == "G": green_tiles.append(GreenTile(px, py, TILE_SIZE))
            elif tile == "P": player.rect.x, player.rect.y = px + 2, py + 2  # player spawn
            elif tile == "X": enemies.append(ShooterEnemy(px, py, TILE_SIZE, speed=1))  # added slower enemy

    # Second pass: link switches to doors and exits
    for sw in switches:
        sw.linked_doors = doors  # added linking doors to switches
        sw.linked_exits = exits  # added linking exits to switches

# Initial load
load_level(current_level)

# ------------------ GAME LOOP ------------------
running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    # ------------------ EVENTS ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # ------------------ PLAYER ------------------
    player.move(keys, walls, doors)  # added walls and doors collision

    # ------------------ FAKE WALL DISCOVERY ------------------
    for fw in fake_walls:
        if player.rect.colliderect(fw.rect): fw.discovered = True  # added: reveal fake walls when touched

    # ------------------ SWITCHES ------------------
    for sw in switches:
        sw.try_activate(player.rect, keys)  # added: activate doors and exits

    # ------------------ ENEMIES ------------------
    for enemy in enemies:
        enemy.move_towards_player(player)          # move enemy toward player
        enemy.shoot(player)                         # enemy shoots
        enemy.update_bullets(player, walls)        # bullets hit player or walls

    # ------------------ EXIT CHECK ------------------
    for ex in exits:
        if ex.active and player.rect.colliderect(ex.rect):  # added: can only exit if activated
            current_level += 1
            if current_level < len(LEVELS):
                load_level(current_level)
            else:
                running = False

    # ------------------ DRAW ------------------
    screen.fill((0,0,0))
    for w in walls: pygame.draw.rect(screen, (100,100,100), w.rect)
    for fw in fake_walls:
        if fw.discovered: pygame.draw.rect(screen, (50,50,50), fw.rect)
    for d in doors:
        if not d.hidden: pygame.draw.rect(screen, (0,0,255), d.rect)  # added: only show doors when revealed
    for sw in switches:
        color = (0,255,0) if sw.active else (0,155,0)  # added: switch color depends on active
        pygame.draw.rect(screen, color, sw.rect)
    for ex in exits:
        color = (0,255,255) if ex.active else (255,0,255)  # added: exit color depends on active
        pygame.draw.rect(screen, color, ex.rect)
    for gt in green_tiles: pygame.draw.rect(screen, (0,150,0), gt.rect)
    for enemy in enemies:
        pygame.draw.rect(screen, (255,0,0), enemy.rect)
        for bullet in enemy.bullets: pygame.draw.rect(screen, (255,255,255), bullet["rect"])
    pygame.draw.rect(screen, (0,255,0), player.rect)

    # ------------------ HUD ------------------
    elapsed = int(time.time() - level_start_time)
    hud_text = f"Level: {current_level+1}  Health: {player.health}  Time: {elapsed}s  Controls: WASD/Arrows + Space"  # added health display
    hud = font.render(hud_text, True, (255,255,255))
    pygame.draw.rect(screen, (50,50,50), (0,0,WIDTH,25))
    screen.blit(hud, (5,3))
    pygame.display.flip()

    # ------------------ GAME OVER ------------------
    if player.health <= 0:  # added: check for player death
        print("GAME OVER")
        running = False

pygame.quit()
print("Thanks for play")
print("Created by: Sarvesh Vijayamanikanda")

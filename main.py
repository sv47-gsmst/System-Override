import pygame, sys, random, math
pygame.init()

# -------------------- CONSTANTS --------------------
WIDTH, HEIGHT = 900, 600
TILE = 40
COLS, ROWS = WIDTH//TILE, HEIGHT//TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("System Override")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
large_font = pygame.font.SysFont("consolas", 50, bold=True)

WHITE, BLACK, RED, GREEN, BLUE, GRAY, YELLOW, PURPLE = (
    (255,255,255),(0,0,0),(200,0,0),(0,200,0),(0,100,255),(60,60,60),(255,255,0),(255,0,255)
)

# -------------------- GLOBALS --------------------
player = None
bullets = []
particles = []
enemies = []
current_level = 1
total_time = 0

# -------------------- PLAYER --------------------
class Player:
    def __init__(self):
        self.rect = pygame.Rect(TILE+5, TILE+5, TILE-10, TILE-10)
        self.speed = 4
        self.health = 100
        self.max_health = 100

    def move(self, dx, dy, walls):
        self.rect.x += dx
        for w in walls:
            if self.rect.colliderect(w):
                if dx>0: self.rect.right=w.left
                if dx<0: self.rect.left=w.right
        self.rect.y += dy
        for w in walls:
            if self.rect.colliderect(w):
                if dy>0: self.rect.bottom=w.top
                if dy<0: self.rect.top=w.bottom

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# -------------------- BULLET --------------------
class Bullet:
    def __init__(self,pos,target,speed=3):
        self.rect = pygame.Rect(pos[0],pos[1],8,8)
        dx,dy = target[0]-pos[0], target[1]-pos[1]
        dist = math.hypot(dx,dy)
        if dist !=0: dx/=dist; dy/=dist
        self.vel=(dx*speed,dy*speed)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if pygame.time.get_ticks()-self.spawn_time > 2000:
            if self in bullets: bullets.remove(self)
        elif self.rect.colliderect(player.rect):
            player.health -= 2
            if self in bullets: bullets.remove(self)

    def draw(self):
        pygame.draw.rect(screen,YELLOW,self.rect)

# -------------------- PARTICLES --------------------
def spawn_particles(x,y,color,num=5):
    for _ in range(num):
        particles.append([x,y,random.uniform(-2,2),random.uniform(-2,2),color, random.randint(15,30)])

def update_particles():
    for p in particles[:]:
        p[0]+=p[2]; p[1]+=p[3]; p[5]-=1
        if p[5]<=0: particles.remove(p)
        else: pygame.draw.circle(screen,p[4],(int(p[0]),int(p[1])),2)
        if player.rect.collidepoint(p[0],p[1]):
            player.health -= 1

# -------------------- SWITCH --------------------
class Switch:
    def __init__(self,x,y,decoy=False):
        self.rect = pygame.Rect(x,y,25,25)
        self.decoy = decoy
        self.active = True

    def draw(self):
        color = PURPLE if self.decoy else GREEN
        pygame.draw.rect(screen,color,self.rect)

    def try_activate(self, keys, mouse_pos, mouse_pressed):
        if not self.active: return False
        if self.rect.colliderect(player.rect):
            kb_press = keys[pygame.K_e] or keys[pygame.K_SPACE] or keys[pygame.K_c]
            click = mouse_pressed[0] and self.rect.collidepoint(mouse_pos)
            if kb_press or click:
                self.active=False
                return True
        return False

# -------------------- MAZE --------------------
def generate_maze():
    grid=[[1 for _ in range(COLS)] for _ in range(ROWS)]
    def carve(x,y):
        dirs=[(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<nx<COLS-1 and 0<ny<ROWS-1:
                if grid[ny][nx]==1:
                    grid[ny][nx]=0
                    grid[y+dy//2][x+dx//2]=0
                    carve(nx,ny)
    grid[1][1]=0; carve(1,1)
    grid[1][1]=0; grid[1][2]=0; grid[2][1]=0
    return grid

def place_switches(maze,num_decoys=2):
    switches=[]
    free_tiles=[(x,y) for y in range(ROWS) for x in range(COLS) if maze[y][x]==0]
    exit_tile=random.choice(free_tiles)
    ex,ey=exit_tile
    switches.append(Switch(ex*TILE+TILE//4,ey*TILE+TILE//4,decoy=False))
    for _ in range(num_decoys):
        while True:
            dt=random.choice(free_tiles)
            if dt!=exit_tile:
                dx,dy=dt
                switches.append(Switch(dx*TILE+TILE//4,dy*TILE+TILE//4,decoy=True))
                break
    return switches

# -------------------- ENEMY --------------------
class Enemy:
    def __init__(self,level):
        self.rect = pygame.Rect(random.randint(5,WIDTH-35),random.randint(5,HEIGHT-35),30,30)
        self.base_speed = player.speed*0.1
        self.max_speed = player.speed*0.25
        scale = min(level/15,1)
        self.speed = self.base_speed + (self.max_speed-self.base_speed)*scale
        self.bullet_timer = random.randint(30,90)

    def move(self):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx,dy)
        if dist!=0:
            dx/=dist; dy/=dist
            self.rect.x += dx*self.speed
            self.rect.y += dy*self.speed

    def shoot(self):
        if self.bullet_timer<=0:
            bullets.append(Bullet(self.rect.center,player.rect.center,speed=3+self.speed))
            self.bullet_timer=random.randint(60,120)
        else:
            self.bullet_timer-=1

    def draw(self):
        pygame.draw.rect(screen,RED,self.rect)

# -------------------- UI --------------------
def draw_health():
    pygame.draw.rect(screen,RED,(10,10,200,20))
    pygame.draw.rect(screen,GREEN,(10,10,200*player.health/player.max_health,20))

def draw_stats(level,total_time):
    txt=font.render(f"Level:{level} Time:{total_time}s",True,WHITE)
    screen.blit(txt,(10,40))

# -------------------- INTRO --------------------
def intro_screen():
    intro=True
    while intro:
        screen.fill(BLACK)
        title = large_font.render("SYSTEM OVERRIDE",True,WHITE)
        dev = font.render("Developer: Sarvesh V",True,WHITE)
        thanks = font.render("Thanks Hack Club Flavor Town!",True,WHITE)
        start = font.render("Press ENTER to Start",True,WHITE)
        screen.blit(title,(WIDTH//2-title.get_width()//2, HEIGHT//3))
        screen.blit(dev,(WIDTH//2-dev.get_width()//2, HEIGHT//2))
        screen.blit(thanks,(WIDTH//2-thanks.get_width()//2, HEIGHT//2+40))
        screen.blit(start,(WIDTH//2-start.get_width()//2, HEIGHT-100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                intro=False
        clock.tick(60)

# -------------------- POST LEVEL 15 PROMPT --------------------
def post_level_prompt():
    typing_text=""
    full_text="Do you want to EXIT or continue with random levels?"
    text_index=0
    typing_timer=0
    while True:
        screen.fill(BLACK)
        keys=pygame.key.get_pressed()
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()
        typing_timer+=1
        if typing_timer%5==0 and text_index<len(full_text):
            typing_text+=full_text[text_index]; text_index+=1
        txt=font.render(typing_text,True,WHITE)
        opt1=font.render("Press 1 - EXIT",True,WHITE)
        opt2=font.render("Press 2 - CONTINUE RANDOM",True,WHITE)
        screen.blit(txt,(WIDTH//2-350,HEIGHT//2-50))
        screen.blit(opt1,(WIDTH//2-200,HEIGHT//2))
        screen.blit(opt2,(WIDTH//2-200,HEIGHT//2+40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        if keys[pygame.K_1]: return False
        if keys[pygame.K_2]: return True
        clock.tick(60)

# -------------------- GAME LOOP --------------------
def game():
    global player, bullets, particles, enemies, current_level, total_time
    intro_screen()
    current_level=1
    total_time=0
    continue_random=True
    start_time=pygame.time.get_ticks()

    while True:
        maze=generate_maze()
        player=Player()
        walls=[pygame.Rect(x*TILE,y*TILE,TILE,TILE) for y in range(ROWS) for x in range(COLS) if maze[y][x]==1]
        switches=place_switches(maze)
        bullets=[]
        enemies=[Enemy(current_level) for _ in range(3)]
        while True:
            screen.fill(BLACK)
            keys=pygame.key.get_pressed()
            mouse_pos=pygame.mouse.get_pos()
            mouse_pressed=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==pygame.QUIT: pygame.quit(); sys.exit()

            # Player movement
            if player.health>0:
                dx=dy=0
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-player.speed
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=player.speed
                if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-player.speed
                if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=player.speed
                player.move(dx,dy,walls)

            # Draw walls
            for w in walls: pygame.draw.rect(screen,GRAY,w)

            # Switches
            exit_activated=False
            for s in switches:
                if s.active:
                    s.draw()
                    if s.try_activate(keys, mouse_pos, mouse_pressed):
                        if s.decoy:
                            for _ in range(50): spawn_particles(random.randint(0,WIDTH),random.randint(0,HEIGHT),PURPLE)
                        else:
                            exit_activated=True

            # Enemies
            for e in enemies:
                e.move()
                e.shoot()
                e.draw()

            # Bullets
            for b in bullets[:]:
                b.move()
                b.draw()

            # Particles
            player.draw()
            update_particles()

            # UI
            total_time=(pygame.time.get_ticks()-start_time)//1000
            draw_health(); draw_stats(current_level,total_time)

            # Level completion
            if exit_activated:
                player.health=min(player.max_health,player.health+player.max_health*0.25)
                current_level+=1
                break

            # Game over
            if player.health<=0:
                screen.fill(BLACK)
                over=font.render("GAME OVER",True,WHITE)
                restart=font.render("Press R to Restart",True,WHITE)
                screen.blit(over,(WIDTH//2-over.get_width()//2,HEIGHT//2-20))
                screen.blit(restart,(WIDTH//2-restart.get_width()//2,HEIGHT//2+20))
                pygame.display.flip()
                keys=pygame.key.get_pressed()
                if keys[pygame.K_r]: game()
                continue

            pygame.display.flip()
            clock.tick(60)

        # After every 15 levels
        if current_level>=15 and current_level%15==0:
            continue_random=post_level_prompt()
            if not continue_random: pygame.quit(); sys.exit()

# -------------------- RUN --------------------
game()

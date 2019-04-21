import pgzrun
import random

# commenting to use GitHub

# constants to use throughout the program. Adjust these to change game difficulty
HEIGHT = 700
WIDTH = 1000
PLAYER_SPEED = 3
PLAYER_LASER_SPEED = 5
ENEMY_SPEED = 1
ENEMY1_LASER_SPEED = 1
ENEMY2_LASER_SPEED = 2
ENEMY3_LASER_SPEED = 3
ENEMY_FIRING_RATE = 100

player = Actor('player', anchor=('center','bottom'), pos=(WIDTH/2, HEIGHT))
player.laser_active = True
player.lasers = []
player.health = 3
player.speed = PLAYER_SPEED
player.score = 0

wall_left = Actor('wall', pos=(0, 0), anchor=('left', 'top'))
wall_right = Actor('wall',pos=(WIDTH, 0), anchor=('right', 'top'))

enemies = []
enemy_lasers = []
enemy_laser_speeds = [ENEMY1_LASER_SPEED, ENEMY2_LASER_SPEED, ENEMY3_LASER_SPEED]

current_level = 1
# a new comment

def draw():
    screen.clear()
    screen.draw.text("Score: " + str(player.score), (20, 20), color="orange", fontsize=40)
    screen.draw.text("Health: " + str(player.health), (WIDTH-150, 20), color="orange", fontsize=40)
    player.draw()
    draw_lasers()
    draw_enemies()
    wall_left.draw()
    wall_right.draw()
    if player.health == 0:
        screen.draw.text("You Died! GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=100, color="red")

def update():
    if player.health > 0:
        if keyboard.left:
            move_player('left')
        elif keyboard.right:
            move_player('right')
        
        if len(enemies) > 0:
            should_fire = random.randint(1, ENEMY_FIRING_RATE)
            if should_fire == 50:
                enemy_to_fire = random.randint(0, len(enemies)-1)
                fire_enemy_laser(enemies[enemy_to_fire])

        update_lasers()
        move_enemies()
        cleanup_lists()

def on_key_down(key):
    if key == keys.SPACE and player.laser_active:
        fire_player_laser()
    if key == keys.W:
        fire_enemy_laser(enemies[0])

def move_player(direction):
    if direction == 'left' and player.x > 50:
        player.x -= player.speed
    elif direction == 'right' and player.x < WIDTH - 50:
        player.x += player.speed

def fire_player_laser():
    sounds.laser1.play()
    laser = Actor('laserblue1', pos=(player.x, player.y-50))
    laser.active = True
    player.lasers.append(laser)
    player.laser_active = False
    clock.schedule_unique(reset_laser, 0.25)

def fire_enemy_laser(enemy):
    sounds.laser2.play()
    laser = Actor('laserred1', pos=(enemy.x, enemy.y+20))
    laser.active = True
    laser.speed = enemy.laser_speed
    enemy_lasers.append(laser)

def reset_laser():
    player.laser_active = True

def draw_lasers():
    for laser in player.lasers:
        laser.draw()
    for laser in enemy_lasers:
        laser.draw()

def update_lasers():
    for laser in player.lasers:
        laser.y -= PLAYER_LASER_SPEED
        enemy_num = laser.collidelist(enemies)
        if enemy_num > -1:
            laser.active = False
            if enemies[enemy_num].health == 1:
                sounds.explosion2.play()
                enemies[enemy_num].active = False
                player.score += enemies[enemy_num].points
            else:
                sounds.hit1.play()
                enemies[enemy_num].health -= 1

        if laser.y < 0:
            laser.active = False
    
    for laser in enemy_lasers:
        laser.y += laser.speed
        if laser.colliderect(player):
            sounds.player_explosion.play()
            player.health -= 1
            laser.active = False
        if laser.y > HEIGHT:
            laser.active = False
                

def setup_enemies():
    for row in range(3):
        for i in range(10):
            enemy = Actor('enemy' + str(row + 1), pos=(60 * i + 50, 200 - row * 50))
            enemy.laser_active = True
            enemy.active = True
            enemy.health = 1 * (row + 1)
            enemy.speed = ENEMY_SPEED
            enemy.laser_speed = enemy_laser_speeds[row]
            enemy.points = 10 * (row + 1)
            enemies.append(enemy)
    
    # for i in range(10):
    #     enemy = Actor('enemy1', pos=(60 * i + 50, 200))
    #     enemy.laser_active = True
    #     enemy.active = True
    #     enemy.health = 1
    #     enemy.speed = ENEMY_SPEED
    #     enemy.points = 10
    #     enemies.append(enemy)
    # for i in range(10):
    #     enemy = Actor('enemy2', pos=(60 * i + 50, 150))
    #     enemy.laser_active = True
    #     enemy.active = True
    #     enemy.health = 2
    #     enemy.speed = ENEMY_SPEED
    #     enemy.points = 20
    #     enemies.append(enemy)
    # for i in range(10):
    #     enemy = Actor('enemy3', pos=(60 * i + 50, 100))
    #     enemy.laser_active = True
    #     enemy.active = True
    #     enemy.health = 3
    #     enemy.speed = ENEMY_SPEED
    #     enemy.points = 30
    #     enemies.append(enemy)

def draw_enemies():
    for enemy in enemies:
        if enemy.active:
            enemy.draw()

# move enemies across screen.
# when they get to edge, move down screen and reverse direction
# TO DO: make them speed up?
def move_enemies():
    at_edge = False
    if wall_left.collidelist(enemies) > -1 or wall_right.collidelist(enemies) > -1:
        at_edge = True
    for enemy in enemies:
        if at_edge:
            enemy.speed *= -1
            enemy.y += 5
        enemy.x += enemy.speed
    
def cleanup_lists():
    for enemy in enemies[:]:
        if not enemy.active:
            enemies.remove(enemy)
    for laser in player.lasers[:]:
        if not laser.active:
            player.lasers.remove(laser)
    for laser in enemy_lasers[:]:
        if not laser.active:
            enemy_lasers.remove(laser)

setup_enemies()

pgzrun.go()

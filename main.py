import pygame
import sys
import random


def detect_collision(player_pos, enemy_pos):
    global player_size
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if e_x >= p_x and e_x < p_x + player_size or p_x >= e_x and p_x < e_x + player_size:
        if e_y >= p_y and e_y < p_y + player_size or p_y >= e_y and p_y < e_y + player_size:
            return True

    return False


def collision_check(enemy_list):
    global player_position
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos) is True:
            return True
    return False


def drop_enemies(enemy_list):
    delay = random.random()  # delay is in [0,1]
    if len(enemy_list) < number_of_enemies and delay < 0.2:
        x = random.randint(0, width - enemy_size)
        y = 0
        enemy_list.append([x, y])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, blue, (*enemy_pos, enemy_size, enemy_size))


def update_enemy_pos(enemy_list):
    global score
    for index, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(index)
            score += 1


def set_level(score):
    global speed, number_of_enemies
    speed = score / 15 + 5
    if score > 100:
        number_of_enemies = score//10


pygame.init()

width = 800  # screen
height = 600
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
player_size = 50
player_pos = [width / 2, height - 2 * player_size]
enemy_size = 50
enemy_pos = [random.randint(0, width - enemy_size), 0]
number_of_enemies = 10
enemy_list = [enemy_pos]
screen = pygame.display.set_mode((width, height))

game_over = False
clock = pygame.time.Clock()  # fps - speed of the game
myFont = pygame.font.SysFont("monospace", 35)
speed = 10
score = 0  # enemies doged

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exit
            sys.exit()

        if event.type == pygame.KEYDOWN:  # commands
            x, y = player_pos
            if event.key == pygame.K_LEFT:  # move left
                if x == 0:
                    x = width - player_size  # if we exit the screen we want to get to the opposite side
                else:
                    x = x - player_size
            elif event.key == pygame.K_RIGHT:  # move right
                if x == width - player_size:
                    x = 0
                else:
                    x = x + player_size
            elif event.key == pygame.K_UP:  # move up
                if y == 0:
                    y = height - player_size
                else:
                    y = y - player_size
            elif event.key == pygame.K_DOWN:  # move down
                if y == height - player_size:
                    y = 0
                else:
                    y = y + player_size
            player_pos = [x, y]

    screen.fill(black)

    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    update_enemy_pos(enemy_list)
    set_level(score)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, yellow)
    screen.blit(label, (width - 200, height - 40))

    if collision_check(enemy_list):
        game_over = True
        break
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, red, (*player_pos, player_size, player_size))
    clock.tick(30)  # 30 fps
    pygame.display.update()

print(f"Your score is: {score}")
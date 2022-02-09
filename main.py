import pygame
import os

pygame.font.init()
pygame.mixer.init()

#set the window sizes
WIDTH, HEIGHT = 900, 500

SPACESHIP_WIDTH, SPACESHIP_HEIGH = 55,40

WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,255,0)


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


FPS=60

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate( pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55,40)) , 90)
RED_SPACESHIP =pygame.transform.rotate( pygame.transform.scale(RED_SPACESHIP_IMAGE, (55,40)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

VELOCITY = 5

BULLET_VELOCITY = 7
MAX_BULLETS = 5
#create user events to notify the main program when spaceships are hit by bullets
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2+5, 0,10,HEIGHT)

window = pygame.display.set_mode((WIDTH,HEIGHT))
#set window name
pygame.display.set_caption("STAR WARS")

def draw_window(red, yellow, red_bullets, yellow_bullets,red_health, yellow_health):
    # set window colors (in pygame is always RGB, that's why we enter 3 colors)
    #window.fill(WHITE_COLOR)
    #Set space background
    window.blit(SPACE, (0,0))

    #border is Rect so it must be draw with this funct
    pygame.draw.rect(window,BLACK_COLOR, BORDER)

    #text showing
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE_COLOR)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE_COLOR)
    window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))

    #used for images, objects..
    window.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
    window.blit(RED_SPACESHIP, (red.x,red.y))

    #bullets
    for bullet in red_bullets:
        pygame.draw.rect(window, RED_COLOR, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(window, YELLOW_COLOR, bullet)

    pygame.display.update()

def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and (yellow.x - VELOCITY) > 0:  # move the yellow left
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and (yellow.x + VELOCITY) < BORDER.left - BORDER.width:   # move the yellow right
        yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and (yellow.y - VELOCITY) > 0:  # move the yellow up
        yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and (yellow.y + VELOCITY) < HEIGHT - SPACESHIP_HEIGH -15:  # move the yellow down
        yellow.y += VELOCITY

def red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and (red.x - VELOCITY) > BORDER.left:  # move the red left
        red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and (red.x + VELOCITY) < WIDTH-SPACESHIP_WIDTH:  # move the red right
        red.x += VELOCITY
    if key_pressed[pygame.K_UP] and (red.y - VELOCITY) > 0:  # move the red up
        red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and (red.y + VELOCITY) < HEIGHT - SPACESHIP_HEIGH -15:  # move the red down
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE_COLOR)
    window.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))

    #Show the winning text for 5s then restart the game
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    #we need infinite loop, so images (background, player icon etc.) will display infinite many times (just as in digital image processing)4
    run = True
    #set fps (how many times per sec to refresh the window)
    clock = pygame.time.Clock()

    red = pygame.Rect(700,50, SPACESHIP_WIDTH, SPACESHIP_HEIGH)
    yellow = pygame.Rect(100,50, SPACESHIP_WIDTH, SPACESHIP_HEIGH)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    while run:
        clock.tick(FPS)
        #pygame.event is a list of all possible event that are happening in the window defined
        for event in pygame.event.get():
            #if the user quits, stop the running process
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: #must be pressed X times to fire X bullets (discrete)
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y+yellow.height//2-2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health)

       #WASD to move the yellow spaceship, arrows for the red
        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed, yellow)
        red_movement(key_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

    #pygame.quit() --> to restart the game we call the funct again
    main()

if __name__ == "__main__":
    main()
import pygame
import sys
import random
import time

pygame.init()
jumpscare=0
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(":)")

background_image = pygame.image.load("background3.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
jumpscare_image = pygame.image.load("jumpscareimg.png")
escape_image = pygame.image.load("escape.png")

pygame.mixer.init()


pygame.mixer.music.load('song.mp3')  

pygame.mixer.music.play(loops=-1, start=0.0)  

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0,0,0)

clock = pygame.time.Clock()
FPS = 60

player_width, player_height = 50, 50
player_x, player_y = 100, HEIGHT - player_height - 10
player_color = BLUE
player_speed = 5
player_jump = -15
gravity = 0.5
player_velocity_y = 0
on_ground = False

enemy_width, enemy_height = 50, 50
enemy_x, enemy_y = 600, HEIGHT - enemy_height - 10
enemy_color = ORANGE
enemy_speed = 3
enemy_velocity_y = 0
enemy_jump = -12
enemy_on_ground = False

camera_x = 0
jumpscare=0
ground_height = 10

platform_color = BLACK
platforms = [
    pygame.Rect(0, HEIGHT - 10,WIDTH + 1000000, 10),
    pygame.Rect(200, 450, 200, 10),
    pygame.Rect(500, 300, 200, 10),
    pygame.Rect(900, 350, 200, 10),
    pygame.Rect(1500, 400, 200, 10),

]

player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (player_width, player_height))

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_image2 = pygame.image.load('enemy2.png')
enemy_image2 = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_image3 = pygame.image.load('enemy3.png')
enemy_image3 = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
ground_segments = [
    pygame.Rect(0, HEIGHT - 10, 800, 10),
    pygame.Rect(800, HEIGHT - 10, 800, 10),
]

life_essence = 0
difficulty_increase_interval = 2000


def update_camera(player_rect):
    global camera_x
    camera_x = player_rect.centerx - WIDTH // 2
    if camera_x < 0:
        camera_x = 0


def regenerate_platforms(player_x):
    global platforms
    # Generate platforms ahead only, without removing existing ones
    while platforms[-1].right < player_x + WIDTH * 2:
        last_platform = platforms[-1]
        new_x = last_platform.right + random.randint(150, 300)
        new_y = random.randint(HEIGHT // 2, HEIGHT - 50)
        platforms.append(pygame.Rect(new_x, new_y, 200, 10))

def game_over():
    print("Game over")
    screen.blit(jumpscare_image, (0, 0))



running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = player_jump
        on_ground = False
    if enemy_x - player_x < -800:
        if life_essence<2500:
            pygame.mixer.music.load('jumpscare.mp3')  
            pygame.mixer.music.play()  
            pygame.mixer.music.load('song.mp3')  

            pygame.mixer.music.play(loops=-1, start=0.0)  
            enemy_x = player_x+600
        elif life_essence >= 2500:
            screen.blit(escape_image, (0, 0))
            
            pygame.display.flip()
        
            
            pygame.time.Clock().tick(60)
            time.sleep(3)
            sys.quit()
            
          
    else:
        enemy_speed = 3

    player_velocity_y += gravity
    player_y += player_velocity_y

    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for platform in platforms + ground_segments:
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_y = platform.top - player_height
            player_velocity_y = 0
            on_ground = True

    regenerate_platforms(player_x)
  

    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed

    enemy_velocity_y += gravity
    enemy_y += enemy_velocity_y

    enemy_on_ground = False
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    for platform in platforms + ground_segments:
        if enemy_rect.colliderect(platform) and enemy_velocity_y > 0:
            enemy_y = platform.top - enemy_height
            enemy_velocity_y = 0
            enemy_on_ground = True

    if enemy_on_ground and abs(player_y - enemy_y) > 40:
        enemy_velocity_y = enemy_jump

    if player_rect.colliderect(enemy_rect):
        
        running = False
        pygame.mixer.music.load('jumpscare.mp3')
        pygame.mixer.music.play()
         
        while True:
            
            screen.blit(jumpscare_image, (0, 0))
            
            pygame.display.flip()

            
            pygame.time.Clock().tick(60)
     

    if player_x < 0:
        player_x = 0
    if player_y > HEIGHT:
        player_y = HEIGHT - player_height

    update_camera(player_rect)
    screen.blit(background_image, (0, 0))
    for platform in platforms:
        pygame.draw.rect(screen, platform_color, 
                         (platform.x - camera_x, platform.y, platform.width, platform.height))

    for ground_segment in ground_segments:
        pygame.draw.rect(screen, BLACK, 
                         (ground_segment.x - camera_x, ground_segment.y, ground_segment.width, ground_segment.height))

    pygame.draw.rect(screen, player_color, 
                     (player_rect.x - camera_x, player_rect.y, player_width, player_height))

    pygame.draw.rect(screen, enemy_color, 
                     (enemy_rect.x - camera_x, enemy_rect.y, enemy_width, enemy_height))

    
   

    
    screen.blit(player_image, (player_rect.x - camera_x, player_rect.y))
    if jumpscare == 0:
       screen.blit(enemy_image, (enemy_rect.x - camera_x, enemy_rect.y))
    life_essence += 1
    if life_essence % difficulty_increase_interval == 0:
        enemy_speed += 0.5
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Life Essence: {life_essence}", True, BLUE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

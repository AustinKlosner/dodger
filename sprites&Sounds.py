import pygame, sys, random
from pygame.locals import *

SCALE_FACTOR = 0.2

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up window.
WINDOWHEIGHT = 400
WINDOWWIDTH = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

# Set up colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Set up the player and food data structure.
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20

player = pygame.Rect(300, 100, 40, 40) # This repersents the player's bounds / is not what will be drawn on he board now.
playerImage = pygame.image.load('sprite.jpg')
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))
unscaledImage = pygame.image.load('grunt_sprite.jpg') # Image is too large, so I scale it below.

scaledWidth = int(unscaledImage.get_width() * SCALE_FACTOR)
scaledHeight = int(unscaledImage.get_height() * SCALE_FACTOR)

foodImage = pygame.transform.scale(unscaledImage, (scaledWidth, scaledHeight)) # Getting new, scaled image

foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

# Set up movement variables.
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

# Set up the music
pickUpSound = pygame.mixer.Sound('halo_theme.mp3') # Sounds effect
pygame.mixer.music.load('halo_theme.mp3') # Background music
pygame.mixer.music.play(-1, 0.0) # Plays the background music. The parameters are how many times to play (-1 is forever) and where to start playing.
musicPlaying = True

# Run the game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change the keyboard variable. 
            if event.key == K_LEFT or event.key == K_a: # K_LEFT and K_a are constant variables within pygame that designate the left arrow key and the a key respectively.
                moveRight = False # Turn off the opposite, just in case it's set to True for any reason.
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP: # What happens when the key was released (KEYUP)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x: # Telport
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)
            if event.key == K_m:
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying
            
        if event.type == MOUSEBUTTONUP: # What happens when the mouse button was released (MOUSEBUTTONUP)
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))
    
    foodCounter += 1
    if foodCounter >= NEWFOOD:
        # Add new food.
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))
        
    # Draw the white background onto the surface
    windowSurface.fill(WHITE)
    
    # Move the player.
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right > 0:
        player.right += MOVESPEED
        
    # Draw the player onto the surface
    # pygame.draw.rect(windowSurface, playerImage, player)
    
    windowSurface.blit(playerImage, player) # For copying one image (character) onto another (window). The paramates are source (what you want to draw) and destination (what you're drawing on)
        
    # Check whether the player has intersected with any food squares. 
    for food in foods[:]: # foods[:] creates a copy of the list foods. It works the same was as splicing (i..e. foods 1:3 (which would give you foods[2])) In this case, you're pulling the entire list inclsive as a copy, becasue you cannot edit a list that is being iterated over. Essentially, the copy is now what will be iterated over, so the original can be modified.
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
            
        # Draw the food.
        # for i in range(len(foods)):
        #    pygame.draw.rect(windowSurface, GREEN, foods[i])
        
        for food in foods:
            windowSurface.blit(foodImage, food)
            
        # Draw the window onto the screen.
        pygame.display.update()
        mainClock.tick(40)
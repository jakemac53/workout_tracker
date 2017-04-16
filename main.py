import sys, pygame

from db.setup import *
from db.workouts import *

# Pygame setup
pygame.init()
pygame.font.init()
black = 0, 0, 0
white = 255, 255, 255
size = width, height = 1080, 1080
screen = pygame.display.set_mode(size)

# The database connection
conn = setupDb()
workouts = listWorkouts(conn)
if not workouts:
    for i in range(10):
        addWorkout('Workout %s' % i, conn)
    workouts = listWorkouts(conn)

# Set up a font object
font = pygame.font.Font(pygame.font.get_default_font(), 40)

def shutdown():
    conn.close()
    sys.exit()

# Main game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: shutdown()

    screen.fill(black)
    ypos = 10
    for workout in workouts:
        ren = font.render(workout[0], 0, white)
        screen.blit(ren, (10, 10 + ypos))
        ypos += 40

    # Actually render
    pygame.display.flip()

import sys, pygame, time

# Pygame setup
pygame.init()
pygame.font.init()
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
screen = pygame.display.set_mode((0,0))
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenWidth = screen.get_width();
screenHeight = screen.get_height();

CLOCK_STARTED = 0
CLOCK_STOPPED = 1
class Clock(pygame.sprite.Sprite):
    def __init__(self, rect):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font(pygame.font.get_default_font(), round(rect.h / 2))
        self.timerStart = None
        self.extraTime = 0
        self.rect = rect
        self.image = self.font.render(self.print(), 0, white)
        self.state = CLOCK_STOPPED

    def update(self, events):
        self.image = self.font.render(self.print(), 0, white)

    def start(self):
        self.timerStart = time.time()
        self.state = CLOCK_STARTED

    def stop(self):
        self.extraTime = self.elapsed()
        self.timerStart = None
        self.state = CLOCK_STOPPED

    def reset(self):
        self.stop()
        self.extraTime = 0

    def elapsed(self):
        total = 0
        if self.timerStart:
            total += time.time() - self.timerStart
        total += self.extraTime
        return total

    def print(self):
        time = self.elapsed()
        return "%d%d:%d%d" % ((time / 600), (time / 60) % 10, (time % 60) / 10, time % 10)

class ResetButton(pygame.sprite.Sprite):
    # Constructor. Pass in the text, color, and its x and y position
    def __init__(self, clock):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Set up a font object and render the text
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.clock = clock

        # No need to implement `update`, we never change
        text = "RESET"
        renderedText = self.font.render(text, 0, blue)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = renderedText.get_rect()
        self.rect.inflate_ip(20, 20)
        self.rect.move_ip(self.clock.rect.x + 160, self.clock.rect.y + clock.rect.h * 2/3)

        # Set the actual image
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(green)
        self.image.blit(renderedText, (10, 10))

    def click(self):
        self.clock.reset()

class StartStopButton(pygame.sprite.Sprite):
    # Constructor. Pass in the text, color, and its x and y position
    def __init__(self, clock, key):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Set up a font object and render the text
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.clock = clock
        self.key = key
        self.update()

    def update(self, events = []):
        for event in events:
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                if self.rect.collidepoint(pos): self.click()

            if event.type == pygame.KEYUP:
                if event.key == self.key:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.clock.reset()
                    else:
                        self.click()

        text = "START" if self.clock.state == CLOCK_STOPPED else "STOP"
        renderedText = self.font.render(text, 0, blue)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = renderedText.get_rect()
        self.rect.inflate_ip(20, 20)
        self.rect.move_ip(self.clock.rect.x, self.clock.rect.y + clock.rect.h * 2/3)

        # Set the actual image
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(green)
        self.image.blit(renderedText, (10, 10))

    def click(self):
        if self.clock.state == CLOCK_STOPPED:
            self.clock.start()
        elif self.clock.state == CLOCK_STARTED:
            self.clock.stop()

# Set up the clocks/buttons
clockWidth = screenWidth / 2
clockHeight = screenHeight / 2
clocks = [
    Clock(pygame.Rect(0, 0, clockWidth, clockHeight)),
    Clock(pygame.Rect(clockWidth, 0, clockWidth, clockHeight)),
    Clock(pygame.Rect(0, clockHeight, clockWidth, clockHeight)),
    Clock(pygame.Rect(clockWidth, clockHeight, clockWidth, clockHeight)),
]
buttons = []
keynum = 0
for clock in clocks:
    keynum += 1
    key = getattr(pygame, 'K_%d' % keynum)
    buttons.append(StartStopButton(clock, key))
    buttons.append(ResetButton(clock))
sprites = pygame.sprite.Group(clocks, buttons)

# Main game loop
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    sprites.update(events)
    sprites.draw(screen)
    pygame.display.flip()

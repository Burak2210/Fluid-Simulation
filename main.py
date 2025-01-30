import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN | pygame.SCALED)

font = pygame.font.SysFont("Calibri", 36)


class Points:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_temp = y
        self.circle = pygame.draw.circle(screen, (0, 150, 255), (self.x, self.y), 8)
        self.rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)
        self.draw_rect = pygame.draw.rect(screen, (0, 150, 255), (self.x, self.y - 16, 20, 350))
        self.distance_from_rect = 0
        self.acceleration = 0
        self.wave_type = "stopped"
        self.wave_strength = 1
        self.amplitude = 15
        self.frequency = 0.0007
        self.phase_speed = 0.03
        self.time = 0

    def update(self):
        self.circle = pygame.draw.circle(screen, (0, 150, 255), (self.x, self.y), 8)
        self.draw_rect = pygame.draw.rect(screen, (0, 150, 255), (self.x, self.y - 8, 20, 350))
        self.rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)

    def wave(self, distance):
        global rect_fallen_time
        if rect_fallen_time + (distance * 2) < pygame.time.get_ticks():
            if self.wave_type == "down":
                if self.acceleration <= 0.3 * self.wave_strength:
                    self.acceleration += 0.002
                self.y += self.acceleration
                if self.y - self.y_temp >= 50 * self.wave_strength:
                    self.wave_type = "up"

            if self.wave_type == "up":
                if self.acceleration >= -0.3 * self.wave_strength:
                    self.acceleration -= 0.002
                self.y += self.acceleration
                if self.y_temp - self.y >= 30 * self.wave_strength:
                    self.wave_type = "down"
                    self.wave_strength -= 0.4
                    if self.wave_strength <= 0.2:
                        self.wave_type = "last"

            if self.wave_type == "last":
                self.y += self.acceleration
                if self.acceleration <= 0.3 * self.wave_strength:
                    self.acceleration += 0.002
                if self.y > self.y_temp:
                    self.wave_type = "stopped"
            if self.wave_type == "stopped":
                self.acceleration = 0
                self.y = self.y_temp


class Rectange:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colrect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.falling = False
        self.acceleration = 0
        self.x_average = self.x + self.w / 2

    def update(self):
        if self.falling:
            if self.acceleration <= 0.7:
                self.acceleration += 0.002
            self.y += self.acceleration
        self.colrect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.x_average = self.x + self.w / 2
        pygame.draw.rect(screen, (255, 20, 0), self.colrect)


distance_taken = False
rect_fallen = False
wave_stopped = False
rect_fallen_time = pygame.time.get_ticks()
rect = Rectange(100, 100, 100, 100)
water = []
for i in range(70):
    water.append(Points(i * 20, 550))
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for i in water:
        i.update()
        i.wave(i.distance_from_rect)
        if not rect_fallen or (rect_fallen and rect_fallen_time + (i.distance_from_rect * 2) > pygame.time.get_ticks()):
            i.y = i.amplitude * math.sin(2 * math.pi * i.frequency * i.x + i.phase_speed * i.time) + 550
            i.time += 0.1
        if i.rect.colliderect(rect.colrect) and not rect_fallen:
            rect_fallen = True
            rect_fallen_time = pygame.time.get_ticks()
            for x in water:
                x.distance_from_rect = abs(rect.x_average - x.x) - 50
                x.wave_type = "down"

    if not rect.falling:
        rect.x, rect.y = pygame.mouse.get_pos()
        if rect.y + rect.h > 520:
            rect.y = 520 - rect.h

    if pygame.mouse.get_pressed()[0]:
        rect.falling = True

    if rect.y > 650:
        rect.falling = False
        rect.acceleration = 0

    text = font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255), (0, 0, 0))
    screen.blit(text, (0, 0))
    rect.update()
    pygame.display.update()

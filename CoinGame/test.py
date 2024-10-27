import os
import pygame
import random
from pygame.constants import QUIT

pygame.init() # 초기화 (반드시 필요)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("CoinGame")

lines = [] #(start_pos, end_pos, color)
pointer = 0
start_pos_x = 100
start_pos_y = 300
stock_price = start_pos_y
line_width = 5
EVENT_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(EVENT_TIMER, 1000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == EVENT_TIMER:
            price_diff = random.randrange(-100, 100)
            pos_x = start_pos_x + pointer*line_width
            if price_diff >= 0:
                lines.append(((pos_x, stock_price), (pos_x, stock_price+price_diff), (0,0,255)))
            else:
                lines.append(((pos_x, stock_price), (pos_x, stock_price+price_diff), (255,0,0)))                
            stock_price += price_diff
            pointer += 1
    
    screen.fill((255, 255, 255))
    for line in lines:
        pygame.draw.line(screen, line[2], line[0], line[1], line_width)
    pygame.display.update()

pygame.quit()
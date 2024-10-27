import os
import pygame
import random
from pygame.constants import QUIT
from collections import deque
from stock import Stock

pygame.init() # 초기화 (반드시 필요)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("CoinGame")

current_path = os.path.dirname(__file__)     
image_path = os.path.join(current_path, "images")
background = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "background.png")), (1280, 1280))

stocks = []
for i in range(3):  # 3개의 주식 생성
    stocks.append(Stock(deque(), random.randint(30, 50), random.randint(100, 200), 0))
stock_to_show = 0

STOCK_TIMER = pygame.USEREVENT + 1  #주식 업데이트 타이머
pygame.time.set_timer(STOCK_TIMER, 50) #주기 (ms단위)

#fps 설정
clock = pygame.time.Clock()
fps = 60

running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == STOCK_TIMER: #그래프 수치 생성, 저장
            for stock in stocks:
                stock.stock()

    
    screen.blit(background, (0, 0))
    #screen.fill((255,255,255))
    stocks[stock_to_show].rect(pygame, screen)
    stocks[stock_to_show].update(pygame, screen)
    pygame.display.update()

pygame.quit()
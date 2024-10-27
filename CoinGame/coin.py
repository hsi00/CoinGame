import os
import sys
import pygame
import random
from pygame.constants import QUIT
from collections import deque
from stock import Stock
from button import Button

pygame.init()

screen_width = 1280
screen_height = 720
SCREEN = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("CoinGame")

current_path = os.path.dirname(__file__)     
image_path = os.path.join(current_path, "images")
font_path = os.path.join(current_path, "font")
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

def get_font(size):
    return pygame.font.Font(os.path.join(font_path, "font.ttf"), size)

def start(): #시작 메뉴
    running = True
    while running:
        clock.tick(fps)

        mouse_pos = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(None, (640,360), "PLAY", get_font(75), '#585391', "White")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    game()
                    break

        a = get_font(100).render("COIN GAME", True, "#585391")
        b = a.get_rect(center=(640, 150))

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(a, b)
        PLAY_BUTTON.changeColor(mouse_pos)
        PLAY_BUTTON.update(SCREEN)
        #screen.fill((255,255,255))
        pygame.display.update()

def game(): #게임 화면
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            elif event.type == STOCK_TIMER: #그래프 수치 생성, 저장
                for stock in stocks:
                    stock.stock()

        
        SCREEN.blit(background, (0, 0))
        #screen.fill((255,255,255))
        stocks[stock_to_show].rect(pygame, SCREEN)
        stocks[stock_to_show].update(pygame, SCREEN)
        pygame.display.update()

start()

pygame.quit()

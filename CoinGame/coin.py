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

#fps 설정
clock = pygame.time.Clock()
fps = 60

def get_font(size):
    return pygame.font.Font(os.path.join(font_path, "font.ttf"), size)

def start(): #시작 메뉴
    running = True

    TITLE_TEXT = get_font(100).render("COIN GAME", True, "#585391")
    TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 150))
    PLAY_BUTTON = Button(None, (640,360), "PLAY", get_font(75), '#585391', "White")

    while running:
        clock.tick(fps)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    game()
                    break

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        PLAY_BUTTON.changeColor(mouse_pos)
        PLAY_BUTTON.update(SCREEN)
        #screen.fill((255,255,255))
        pygame.display.update()

def game(): #게임 화면
    running = True

    #주식
    stocks = []
    for i in range(3):  # 3개의 주식 생성
        stocks.append(Stock(deque(), random.randint(30, 50), random.randint(100, 200), 0))
    stock_to_show = 0

    STOCK_TIMER = pygame.USEREVENT + 1  #주식 업데이트 타이머
    pygame.time.set_timer(STOCK_TIMER, 50) #주기 (단위:ms)

    #주식 전환 버튼
    button_top_margin = 30
    button_interval = 50
    button_length = ((Stock.end_pos_x - Stock.start_pos_x) - button_interval*2) / 3
    button_pos_y = Stock.end_pos_y + button_top_margin + button_length*0.75
    button1_pos = (Stock.start_pos_x + button_length/2, button_pos_y)
    button2_pos = (Stock.start_pos_x + button_length*1.5 + button_interval, button_pos_y)
    button3_pos = (Stock.start_pos_x + button_length*2.5 + button_interval*2, button_pos_y)

    stock1_button = Button(None, button1_pos, "Stock1", get_font(30), '#585391', "White")
    stock2_button = Button(None, button2_pos, "Stock2", get_font(30), '#585391', "White")
    stock3_button = Button(None, button3_pos, "Stock3", get_font(30), '#585391', "White")
    stock_buttons = [stock1_button, stock2_button, stock3_button]

    #제한시간 타이머
    time = 60 #제한시간 (단위:s)
    time_text: str
    timer_pos_x = 1060
    timer_pos_y = 30
    timer_length = 185
    timer_height = 50

    while running:
        clock.tick(fps)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            elif event.type == STOCK_TIMER: #그래프 수치 생성, 저장
                for stock in stocks:
                    stock.stock()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    btn = stock_buttons[i]
                    if btn.checkForInput(mouse_pos):
                        stock_to_show = i
        
        time_text = f"{(time//60):02}:{(time%60):02}"
        TIME_TEXT = get_font(35).render(time_text, True, "White")
        TIME_RECT = TIME_TEXT.get_rect(center=(timer_pos_x+timer_length/2, timer_pos_y+timer_height/2))                
        
        SCREEN.blit(background, (0, 0))
        #screen.fill((255,255,255))
        stocks[stock_to_show].rect(pygame, SCREEN)
        stocks[stock_to_show].update(pygame, SCREEN)
        for b in stock_buttons:
            b.changeColor(mouse_pos)
            b.update(SCREEN)
        pygame.draw.rect(SCREEN, '#585391', (timer_pos_x, timer_pos_y, timer_length, timer_height))
        SCREEN.blit(TIME_TEXT, TIME_RECT)

        pygame.display.update()

start()

pygame.quit()

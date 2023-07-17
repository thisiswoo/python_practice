# 프래임 설정
import pygame

pygame.init()

# 화면 크기 설정
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름 설정
pygame.display.set_caption("Puzzle Bobble")

# Frame Per Second(FPS) 설정을 통한 어느 곳에서도 일정한 게임 속도를 설정
clock = pygame.time.Clock()

# 게임이 반복적으로 실행되게 설정. 게임 loop 설정
running = True
while running:
    clock.tick(60) # FPS 값이 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit() # 게임 종료
# 천장 충돌 처리
import os, random, math
import pygame

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0, 0)): # 버블 클래스 init 메서드
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center = position)
        self.radius = 18

    def set_rect(self, position):
        self.rect = self.image.get_rect(center = position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle) # 호도법으로 변환

    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        # 튕기기
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.angle = angle
        self.original_image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)

    # 화살표 회전
    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.position)

# 맵 만들기
def setup():
    global map # 전역 변수 사용하기 위한 global 키워드 지정
    map = [
        # ["R", "R", "Y", "Y", "B", "B", "G", "G"]
        list("RRYYBBGG"),
        list("RRYYBBG/"), # / : 버블이 위치할 수 없는 곳
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"), # . : 비어있는 곳
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))

def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2
    return pos_x, pos_y

def get_bubble_image(color):
    if color == "R":
        return bubble_images[0] # 빨강
    elif color == "Y":
        return bubble_images[1] # 노랑
    elif color == "B":
        return bubble_images[2] # 파랑
    elif color == "G":
        return bubble_images[3] # 초록
    elif color == "P":
        return bubble_images[4] # 보라
    else:
        return bubble_images[-1] # 검정

def prepare_bubbles():
    global curr_bubble, next_bubble # 전역 변수로 설정
    if next_bubble:
        curr_bubble = next_bubble
    else:
        curr_bubble = create_bubble() # 새 버블 만들기

    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble() # 새 버블 만들기
    next_bubble.set_rect((screen_width // 4, 688))
def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    return random.choice(colors)

# 버블 충돌 처리
def process_collision():
    global curr_bubble, fire
    # spritecollideany() : bubble_group 내 어떠한 것이라도 충돌했다고 하면 그 충돌된 대상을 가지고 온다.
    # bubble_group과 curr_bubble(현재 버블)이 collide_mask()(투명 영역 제외)하고 이미지(버블)가 있는 부분을 비교했을 때 충돌 되는 부분이 하나라도 있으면 충돌된 버블을 가져오기
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask )
    if hit_bubble or curr_bubble.rect.top <= 0:
        row_idx, col_idx = get_map_idx(*curr_bubble.rect.center) # * : 언패킹(x, y)
        place_bubble(curr_bubble, row_idx, col_idx) # 충돌 후 해당 버블 위치 정의
        curr_bubble = None
        fire = None

def get_map_idx(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2)) // CELL_SIZE
        if col_idx < 0:
            col_idx = 0
        elif col_idx > MAP_COL_COUNT - 2:
            col_idx = MAP_COL_COUNT - 2

    return row_idx, col_idx

def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble_group.add(bubble)

pygame.init()

# 화면 크기 설정
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름 설정
pygame.display.set_caption("Puzzle Bobble")

# Frame Per Second(FPS) 설정을 통한 어느 곳에서도 일정한 게임 속도를 설정
clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 버블 이미지 불러오기
bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

# 발사대 이미지 불러오기
pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
RED = (255, 0, 0)
MAP_ROW_COUNT = 11 # row(줄) 기준
MAP_COL_COUNT = 8 # column(행) 기준

# 화살표 관련 변수
to_angle_left = 0 # 왼쪽으로 움직일 각도 정보
to_angle_right = 0 # 오른쪽으로 움직일 각도 정보
angle_speed = 1.5 # 1.5도씩 움직임

# 버블 관련 변수
curr_bubble = None # 이번에 쏠 버블
next_bubble = None # 다음에 쏠 버블
fire = False # 발사 여부

map = [] # 맵
bubble_group = pygame.sprite.Group()
setup()

# 게임이 반복적으로 실행되게 설정. 게임 loop 설정
running = True
while running:
    clock.tick(60) # FPS 값이 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE:
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not curr_bubble:
        prepare_bubbles()

    if fire:
        process_collision() # 충돌 처리

    screen.blit(background, (0, 0)) # x, y 좌표 설정
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right) # 포인터 이미지를 각도에 맞게 회전
    pointer.draw(screen) # 포인터 그려주기
    if curr_bubble:
        if fire:
            curr_bubble.move()
        curr_bubble.draw(screen)

        # if curr_bubble.rect.top <= 0:
        #     curr_bubble = None
        #     fire = False

    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update() # background.png 파일을 display에 적용

pygame.quit() # 게임 종료
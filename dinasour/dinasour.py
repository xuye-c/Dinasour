import pygame
import os
import random


pygame.init()

#the size of the window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("chrome_dinasour")
#loading works
script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前 .py 文件所在目录
RUNNING = [pygame.image.load(os.path.join(script_dir, "image/dino/DinoRun1.png")),
            pygame.image.load(os.path.join(script_dir, "image/dino/DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join(script_dir, "image/dino/DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join(script_dir, "image/dino/DinoDuck1.png")),
           pygame.image.load(os.path.join(script_dir, "image/dino/DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join(script_dir, "image/cactus/SmallCactus1.png")),
                pygame.image.load(os.path.join(script_dir, "image/cactus/SmallCactus2.png")),
                pygame.image.load(os.path.join(script_dir, "image/cactus/SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join(script_dir, "image/cactus/LargeCactus1.png")),
                pygame.image.load(os.path.join(script_dir, "image/cactus/LargeCactus2.png")),
                pygame.image.load(os.path.join(script_dir, "image/cactus/LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join(script_dir, "image/bird/Bird1.png")),
        pygame.image.load(os.path.join(script_dir, "image/bird/Bird2.png"))]

CLOUD = pygame.image.load(os.path.join(script_dir, "image/else/Cloud.png"))

BG = pygame.image.load(os.path.join(script_dir, "image/else/Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()  #
        self.dino_rect.x = self.X_POS           #设定小恐龙的初始位置
        self.dino_rect.y = self.Y_POS           #

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0                 #恐龙踏步

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN]:
            self.jump_vel = self.JUMP_VEL
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        
        elif not (self.dino_jump or self.dino_duck):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        '''
        elif userInput[pygame.K_DOWN] and self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
'''
    def duck(self): #恐龙俯冲踏步
        self.dino_jump = False
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self): #恐龙常规踏步
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump: #恐龙起飞
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL: #恐龙落地
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH #从左侧出现

    def update(self):
        self.rect.x -= game_speed #左移
        if self.rect.x < -self.rect.width - SCREEN_WIDTH*0.75-game_speed:
            obstacles.pop()#过界消失

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        
        self.type = 0
        super().__init__(image, self.type)
        
        ran = random.randint(1,3)
        if ran == 1: self.rect.y = 300
        elif ran == 2: self.rect.y = 250
        else:  self.rect.y = 80
        
            
        #self.rect.y = 300                   #爆头高度250 防飞高度150 必须飞高度300 
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Bird1(Obstacle):
    def __init__(self, image):
        
        self.type = 0
        super().__init__(image, self.type)
        
        ran = random.randint(1,2)
        if ran == 1: self.rect.y = 300
        else: self.rect.y = 250
        
        
            
        #self.rect.y = 300                   #爆头高度250 防飞高度150 必须飞高度300 
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0: #每百分速度增加
            game_speed += 1

        text = font.render("Score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        #游戏是否结束？
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #游戏未结束：
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        '''
        if len(obstacles) ==0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))
        '''   
        #障碍物刷新规则    
        if random.randint(0,1)==1 and len(obstacles) ==0:
                #check = 0
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))
        elif len(obstacles) ==0:
            #check = 0
            for i in range(2):
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird1 (BIRD))
        
        if len(obstacles)==1 and obstacles[0].rect.x <= SCREEN_WIDTH/2+game_speed and random.randint(0,3)==0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

    
        #遍历obstacles画障碍物
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect): #是否撞到障碍物
                pygame.time.delay(1000)                     #游戏暂停时间
                death_count += 1                            #死亡次数增加
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
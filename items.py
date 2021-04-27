import pygame
import random
from GLOBAL import *

class Bar(pygame.sprite.Sprite):
    
    # 大小
    width = 20
    height = 130
    # 最大bar速度
    max_speed = [0, 4]
    hit_flag = False

    def __init__(self, screen, position):
        # 继承__init__
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        # 所在表面      
        self.screen = screen
        # 自身矩形与位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = position
        self.init_center = position
        # 当前速度
        self.direction = [1, 1]
        self.speed = [0, 0]
        # 移动标志
        self.move_flag = 0

    # 更新函数，每次主循环中更新
    def update(self):
        # bar控制为移动时，且不超过边界     
        if self.move_flag == 1 and self.rect.top > 0 :
            # 速度方向向上
            self.speed = self.max_speed
            self.direction = [1, -1]
            # 移动
            self.rect.move_ip([self.speed[0] * self.direction[0], self.speed[1] * self.direction[1]])
        elif self.move_flag == -1 and self.rect.bottom < self.screen.get_height(): 
            # 速度方向向下
            self.speed = self.max_speed
            self.direction = [1, 1]
            # 移动
            self.rect.move_ip([self.speed[0] * self.direction[0], self.speed[1] * self.direction[1]])
        else :
            # 速度为0
            self.speed = [0, 0]

    # 小球碰撞bar反弹
    def hit(self, ball):
        if (ball.rect.center[0] <= self.rect.left and ball.direction[0] == 1) or \
            (ball.rect.center[0] >= self.rect.right and ball.direction[0] == -1) :
            # x方向翻转，若小于x方向最大速度，则增加 
            ball.direction[0] = - ball.direction[0]
            if ball.speed[0] < ball.max_speed[0]:
                ball.speed[0] += ball.speed_increase
            # y方向速度根据bar改变，若小于y方向最大速度，与bar同向则增加，反向则减小               
            if ball.direction[1] * self.direction[1] == 1 :
                ball.speed[1] = ball.speed[1] + self.speed[1]
            else:
                ball.speed[1] = ball.speed[1] - self.speed[1]
        elif ball.rect.top > self.rect.top and ball.rect.bottom < self.rect.bottom and ball.rect.center[0] < self.rect.right and ball.rect.center[0] > self.rect.left :
            ball.direction[0] = - ball.direction[0]            
            if ball.direction[1] * self.direction[1] == 1 :
                ball.speed[1] = ball.speed[1] + self.speed[1]
            else:
                ball.speed[1] = ball.speed[1] - self.speed[1]
        else:
            ball.direction[1] = - ball.direction[1]
            if ball.direction[1] * self.direction[1] == 1 :
                ball.speed[1] = ball.speed[1] + self.speed[1]
            else:
                ball.speed[1] = ball.speed[1] - self.speed[1]

    # 重置位置和速度
    def reset(self):
        # 回到初始位置，速度移动置0
        self.rect.center = self.init_center
        self.speed = [0, 0]
        self.direction = [1, 1]
        self.move_flag = 0

    def blit(self):
        pygame.draw.rect(self.screen, WHITE, self.rect, 0)


class Ball(pygame.sprite.Sprite):

    # 随机初始速度
    init_speed = [2, 4]
    # 半径
    rad = 10
    # 最大ball速度
    max_speed = [10, 9]
    # ball每次x速度增长
    speed_increase = 1

    def __init__(self, screen, position):
        # 继承__init__
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        # 属性
        self.screen = screen
        # 当前方向
        self.direction = [random.choice((-1, 1)), random.choice((-1, 1))]
        # 当前速度
        self.speed = [self.init_speed[0], random.randrange(0, self.init_speed[1])]
        # 自身矩形
        self.rect = pygame.Rect(0, 0, self.rad, self.rad) 
        self.rect.center = position
        self.init_center = position

    # 更新函数，每次主循环中更新
    def update(self):        
        # 检测与上下边界碰撞，碰撞则y速度取反
        if self.rect.top < 0 and self.direction[1] < 0:
            self.direction[1] = -self.direction[1]
        elif self.rect.bottom > self.screen.get_height() and self.direction[1] > 0:
            self.direction[1] = -self.direction[1]
        # 保持移动
        self.rect.move_ip((self.speed[0] * self.direction[0], self.speed[1] * self.direction[1]))

        if self.speed[1] > self.max_speed[1]:
            self.speed[1] = self.max_speed[1]
        if self.speed[1] < 0:
            self.speed[1] = - self.speed[1]
            self.direction[1] = - self.direction[1]
    # 碰撞检测函数
    def hit(self, target):
        # 取自身的矩形大小
        return self.rect.colliderect(target.rect)

    # 重置速度与位置
    def reset(self):
        # 回到初始位置与速度
        self.speed = [self.init_speed[0], random.randrange(0, self.init_speed[1])]
        self.direction = [random.choice((-1, 1)), random.choice((-1, 1))]
        self.rect.center = self.init_center

    def blit(self):
        pygame.draw.circle(self.screen, WHITE, self.rect.center, self.rad, 0)
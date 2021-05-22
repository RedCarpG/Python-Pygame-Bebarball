from enum import Enum

from pygame.sprite import Sprite
from pygame import Rect
from pygame.draw import rect, circle
import random
from abc import abstractmethod
from .bbb_local import *


class BeBarBallSprite(Sprite):
    FULL_SCREEN_MODE = False

    def __init__(self, screen):
        Sprite.__init__(self)  # call Sprite initializer
        self.screen = screen

    @abstractmethod
    def hit(self, *args):
        pass

    @abstractmethod
    def blit(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def to_full_screen(self, func_full, flag_fs):
        pass

    @classmethod
    def set_full_screen_mode(cls, flag):
        BeBarBallSprite.FULL_SCREEN_MODE = flag


class Bar(BeBarBallSprite):
    number = 1

    def __init__(self, screen):
        # 继承__init__
        BeBarBallSprite.__init__(self, screen)
        self.bar_num = Bar.number
        Bar.number += 1

        if BeBarBallSprite.FULL_SCREEN_MODE:
            # Max speed
            self.max_speed = BAR_MAX_SPEED
            # size
            self.width = BAR_WIDTH
            self.height = BAR_HEIGHT
            # 自身矩形与位置
            if self.bar_num == 1:
                self.init_center = BAR_INIT_POSITION_1
            else:
                self.init_center = BAR_INIT_POSITION_2
        else:
            # Max speed
            self.max_speed = BAR_MAX_SPEED_FS
            # size
            self.width = BAR_WIDTH_FS
            self.height = BAR_HEIGHT_FS
            # 自身矩形与位置
            if self.bar_num == 1:
                self.init_center = BAR_INIT_POSITION_1_FS
            else:
                self.init_center = BAR_INIT_POSITION_2_FS

        self.rect_center = self.init_center
        self.rect = Rect(self.rect_center, (self.width, self.height))

        # 当前速度
        self.direction = [1, 1]
        self.speed = [0, 0]
        # 移动标志
        self.move_flag = 0
        self.hit_flag = False

    def update(self):
        """
        Update method from Sprite.update()
        @return: None
        """
        # bar控制为移动时，且不超过边界
        if self.move_flag == 1 and self.rect.top > 0:
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
        else:
            # 速度为0
            self.speed = [0, 0]

    # 小球碰撞bar反弹
    def hit(self, ball):
        if (ball.rect.center[0] <= self.rect.left and ball.direction[0] == 1) or \
                (ball.rect.center[0] >= self.rect.right and ball.direction[0] == -1):
            # x方向翻转，若小于x方向最大速度，则增加 
            ball.direction[0] = - ball.direction[0]
            if ball.speed[0] < ball.max_speed[0]:
                ball.speed[0] += ball.speed_increase
            # y方向速度根据bar改变，若小于y方向最大速度，与bar同向则增加，反向则减小               
            if ball.direction[1] * self.direction[1] == 1:
                ball.speed[1] = ball.speed[1] + self.speed[1]
            else:
                ball.speed[1] = ball.speed[1] - self.speed[1]
        elif ball.rect.top > self.rect.top and ball.rect.bottom < self.rect.bottom and \
                self.rect.right > ball.rect.center[0] > self.rect.left:
            ball.direction[0] = - ball.direction[0]
            if ball.direction[1] * self.direction[1] == 1:
                ball.speed[1] = ball.speed[1] + self.speed[1]
            else:
                ball.speed[1] = ball.speed[1] - self.speed[1]
        else:
            ball.direction[1] = - ball.direction[1]
            if ball.direction[1] * self.direction[1] == 1:
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
        rect(self.screen, COLOR_BAR, self.rect, 0)

    def to_full_screen(self, func_full, flag_fs):
        if flag_fs:
            self.width, self.height = BAR_WIDTH_FS, BAR_HEIGHT_FS
            self.max_speed = BAR_MAX_SPEED_FS
            if self.bar_num == 1:
                self.init_center = BAR_INIT_POSITION_1_FS
            else:
                self.init_center = BAR_INIT_POSITION_2_FS
        else:
            self.width, self.height = BAR_WIDTH, BAR_HEIGHT
            self.max_speed = BAR_MAX_SPEED
            if self.bar_num == 1:
                self.init_center = BAR_INIT_POSITION_1
            else:
                self.init_center = BAR_INIT_POSITION_2

        self.rect = Rect(self.rect.topleft, (self.width, self.height))
        self.rect.center = func_full(self.rect.center)


class Ball(BeBarBallSprite):

    def __init__(self, screen, position=None):
        # 继承__init__
        BeBarBallSprite.__init__(self, screen)
        # 属性
        self.screen = screen

        if BeBarBallSprite.FULL_SCREEN_MODE:
            self.init_speed = BALL_INIT_SPEED
            # 最大ball速度
            self.max_speed = BALL_MAX_SPEED
            # ball每次x速度增长
            self.speed_increase = BALL_INCREASE_SPEED
            self.init_position = BALL_INIT_POSITION
            self.rad = BALL_RAD
        else:
            self.init_speed = BALL_INIT_SPEED_FS
            # 最大ball速度
            self.max_speed = BALL_MAX_SPEED_FS
            # ball每次x速度增长
            self.speed_increase = BALL_INCREASE_SPEED_FS
            self.init_position = BALL_INIT_POSITION_FS
            self.rad = BALL_RAD_FS

        # 当前方向
        self.direction = [random.choice((-1, 1)), random.choice((-1, 1))]
        # 当前速度
        self.speed = [self.init_speed[0], random.randrange(0, self.init_speed[1])]
        # 自身矩形
        self.rect = Rect(0, 0, self.rad, self.rad)

        if position is not None:
            self.rect.center = position
            self.init_position = position
        else:
            self.rect.center = self.init_position

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
        self.rect.center = self.init_position

    def blit(self):
        circle(self.screen, COLOR_BALL, self.rect.center, self.rad, 0)

    def to_full_screen(self, func_full, flag_fs):
        if flag_fs:
            self.rad = BALL_RAD_FS
            self.init_speed = BALL_INIT_SPEED_FS
            self.max_speed = BALL_MAX_SPEED_FS
            self.speed_increase = BALL_INCREASE_SPEED_FS
            self.init_position = BALL_INIT_POSITION_FS
        else:
            self.rad = BALL_RAD
            self.init_speed = BALL_INIT_SPEED
            self.max_speed = BALL_MAX_SPEED
            self.speed_increase = BALL_INCREASE_SPEED
            self.init_position = BALL_INIT_POSITION

        self.speed = list(func_full(self.speed))
        self.rect = Rect(self.rect.topleft, (self.rad, self.rad))
        self.rect.center = func_full(self.rect.center)

import traceback

import pygame
import sys
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

from sound import load_sound, load_music
from myfont import *
from items import *

# 初始化pygame Init Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
# 时钟 Clock
clock = pygame.time.Clock()
# 初始化窗口
screen = pygame.display.set_mode(SIZE)
screen.fill(BLACK)
pygame.display.set_caption("BeBarBall")
pygame.mouse.set_visible(0)
# 加载音乐 Load Music
load_music("bg.ogg", MAIN_VOLUME)
pygame.mixer.music.play()
# 加载音效 Load Sound
laugh_sound = load_sound("laugh.wav", MAIN_VOLUME)
nope_sound = load_sound("nope.wav", MAIN_VOLUME * 2)
soundGroup = [nope_sound, laugh_sound]
# 字体 Load Font
begin_font = load_font("arialbd.ttf", 30)
title_font = load_font("arialbd.ttf", 150)
score_font = load_font("arial.ttf", 36)
count_font = load_font("arialbd.ttf", 60)
pause_font = load_font("arialbd.ttf", 70)


def main():
    global screen
    volume = 0
    width = screen.get_rect().width
    height = screen.get_rect().height

    running = True
    restart = False
    pause = False
    mute = False
    begin = True
    fullscreen = False

    # begin入场界面
    screen.fill(BLACK)
    begin_text = MyFont(screen, begin_font, "Press Any Key To Begin", (width // 2, 3 * height // 4), color=GRAY)
    title_text = MyFont(screen, title_font, "BeBarBall", (width // 2, height // 2), color=WHITE)
    begin_text.blit()
    title_text.blit()
    pygame.display.flip()

    # begin入场等待
    while begin:
        # 全部事件
        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                print("--退出")
                running = False
                begin = False
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    running = False
                    begin = False
                elif event.key == K_F11:
                    if fullscreen:
                        print("--退出全屏")
                        fullscreen = False
                        screen = pygame.display.set_mode(SIZE)
                        width = screen.get_rect().width
                        height = screen.get_rect().height
                        Ball.init_speed = full(Ball.init_speed, 0)
                        Ball.max_speed = full(Ball.max_speed, 0)
                        Ball.speed_increase = int(Ball.speed_increase / PROPOTION[0])
                        Ball.rad = int(Ball.rad / PROPOTION[1])
                        Bar.width, Bar.height = full((Bar.width, Bar.height), 0)
                        Bar.max_speed = full(Bar.max_speed, 0)
                        screen.fill(BLACK)
                        begin_text.move_center(full(begin_text.rect.center))
                        title_text.move_center(full(title_text.rect.center))
                        begin_text.blit()
                        title_text.blit()
                    # 非全屏变全屏
                    else:
                        print("--进入全屏")
                        fullscreen = True
                        screen = pygame.display.set_mode(FULL_SIZE, FULLSCREEN | HWSURFACE)
                        width = screen.get_rect().width
                        height = screen.get_rect().height
                        Ball.init_speed = full(Ball.init_speed)
                        Ball.max_speed = full(Ball.max_speed)
                        Ball.speed_increase = int(Ball.speed_increase * PROPOTION[0])
                        Ball.rad = int(Ball.rad * PROPOTION[1])
                        Bar.width, Bar.height = full((Bar.width, Bar.height))
                        Bar.max_speed = full(Bar.max_speed)
                        screen.fill(BLACK)
                        begin_text.move_center(full(begin_text.rect.center))
                        title_text.move_center(full(title_text.rect.center))
                        begin_text.blit()
                        title_text.blit()
                else:
                    begin = False
                    # 帧数设置
        clock.tick(10)

        # 位置
    cen_bar1 = width // 10, height // 2
    cen_bar2 = 9 * width // 10, height // 2
    center_ball = width // 2, height // 2
    # 对象
    bar1 = Bar(screen, cen_bar1)
    bar2 = Bar(screen, cen_bar2)
    ball1 = Ball(screen, center_ball)
    # 全部对象加入ALL_Sprites
    ALL_Sprites = pygame.sprite.Group()
    ALL_Sprites.add(bar1)
    ALL_Sprites.add(bar2)
    ALL_Sprites.add(ball1)

    # 分数、字体
    score1 = 0
    score2 = 0
    pause_text = MyFont(screen, pause_font, "PAUSE", color=GRAY)
    restart_text = MyFont(screen, count_font, "Restart")
    score1_text = MyFont(screen, score_font, "P1 : %s" % str(score1))
    score2_text = MyFont(screen, score_font, "P2 : %s" % str(score2))
    number_text = MyFont(screen, score_font, " ")
    w1 = width//2
    w2 = width//4
    h1 = height//2
    h2 = height//4
    pause_text.move_center((w1, h1))
    restart_text.move_center((w1, h2))
    score1_text.move_center((w2, h1))
    score2_text.move_center((3 * w2, h1))
    number_text.move_center((w1, 2 * height // 5))
    # 主循环                
    while running:
        # 全部事件
        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                print("--退出")
                running = False
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    running = False
                # 方向键（w,s），（up,down）控制bar
                elif event.key == K_w:
                    # flag = 1 上移
                    bar1.move_flag = 1
                elif event.key == K_s:
                    # flag = -1 下移
                    bar1.move_flag = -1
                elif event.key == K_UP:
                    bar2.move_flag = 1
                elif event.key == K_DOWN:
                    bar2.move_flag = -1

                elif event.key == K_SPACE:
                    print("--暂停")
                    pause = True

                elif event.key == K_MINUS:
                    if volume > - MAIN_VOLUME:
                        print("--音量降低：", volume + MAIN_VOLUME)
                        volume -= 0.1
                        pygame.mixer.music.set_volume(MAIN_VOLUME + volume)
                        for each in soundGroup:
                            each.set_volume(MAIN_VOLUME + volume)
                elif event.key == K_EQUALS:
                    if volume < MAIN_VOLUME:
                        print("--音量增加：", volume + MAIN_VOLUME)
                        volume += 0.1
                        pygame.mixer.music.set_volume(MAIN_VOLUME + volume)
                        for each in soundGroup:
                            each.set_volume(MAIN_VOLUME + volume)

                elif event.key == K_F11:
                    # 全屏变非全屏
                    if fullscreen:
                        print("--退出全屏")
                        fullscreen = False
                        screen = pygame.display.set_mode(SIZE)
                        width = screen.get_rect().width
                        height = screen.get_rect().height
                        cen_bar1 = width // 10, height // 2
                        cen_bar2 = 9 * width // 10, height // 2
                        center_ball = width // 2, height // 2
                        Ball.init_speed = full(Ball.init_speed, 0)
                        Ball.max_speed = full(Ball.max_speed, 0)
                        Ball.speed_increase = int(Ball.speed_increase / PROPOTION[0])
                        Ball.rad = int(Ball.rad / PROPOTION[1])
                        Bar.width, Bar.height = full((Bar.width, Bar.height), 0)
                        Bar.max_speed = full(Bar.max_speed, 0)
                        bar1 = Bar(screen, cen_bar1)
                        bar2 = Bar(screen, cen_bar2)
                        ball1 = Ball(screen, center_ball)
                        ALL_Sprites.empty()
                        ALL_Sprites.add(ball1)
                        ALL_Sprites.add(bar1)
                        ALL_Sprites.add(bar2)
                        pause_text.move_center(full(pause_text.rect.center, 0))
                        restart_text.move_center(full(restart_text.rect.center, 0))
                        score1_text.move_center(full(score1_text.rect.center, 0))
                        score2_text.move_center(full(score2_text.rect.center, 0))
                        number_text.move_center(full(number_text.rect.center, 0))

                        restart = True
                    # 非全屏变全屏
                    else:
                        print("--进入全屏")
                        fullscreen = True
                        screen = pygame.display.set_mode(FULL_SIZE, FULLSCREEN | HWSURFACE)
                        width = screen.get_rect().width
                        height = screen.get_rect().height
                        cen_bar1 = width // 10, height // 2
                        cen_bar2 = 9 * width // 10, height // 2
                        center_ball = width // 2, height // 2
                        Ball.init_speed = full(Ball.init_speed)
                        Ball.max_speed = full(Ball.max_speed)
                        Ball.speed_increase = int(Ball.speed_increase * PROPOTION[0])
                        Ball.rad = int(Ball.rad * PROPOTION[1])
                        Bar.width, Bar.height = full((Bar.width, Bar.height))
                        Bar.max_speed = full(Bar.max_speed)
                        bar1 = Bar(screen, cen_bar1)
                        bar2 = Bar(screen, cen_bar2)
                        ball1 = Ball(screen, center_ball)
                        ALL_Sprites.empty()
                        ALL_Sprites.add(ball1)
                        ALL_Sprites.add(bar1)
                        ALL_Sprites.add(bar2)
                        pause_text.move_center(full(pause_text.rect.center))
                        restart_text.move_center(full(restart_text.rect.center))
                        score1_text.move_center(full(score1_text.rect.center))
                        score2_text.move_center(full(score2_text.rect.center))
                        number_text.move_center(full(number_text.rect.center))

                        restart = True

            # 松开按键事件，flag = 0
            elif event.type == KEYUP:
                if event.key == K_w and bar1.move_flag == 1:
                    bar1.move_flag = 0

                if event.key == K_s and bar1.move_flag == -1:
                    bar1.move_flag = 0

                if event.key == K_UP and bar2.move_flag == 1:
                    bar2.move_flag = 0

                if event.key == K_DOWN and bar2.move_flag == -1:
                    bar2.move_flag = 0

        # 检测碰撞
        for each in ALL_Sprites:
            if each == ball1:
                continue
            if ball1.hit(each):
                if not each.hit_flag:
                    each.hit(ball1)
                    nope_sound.play()
                each.hit_flag = True
            else:
                each.hit_flag = False

        # ball到达左右边界则相应加分，进入结算画面
        if ball1.rect.left < 0 or ball1.rect.right > width:
            # 到达左边，p2加分
            if ball1.rect.left < 0:
                print("--P2得分")
                score2 += 1
                score2_text.change_text("P2 : %s" % str(score2))
            # 到达右边，p1加分
            elif ball1.rect.right > width:
                print("--P1得分")
                score1 += 1
                score1_text.change_text("P1 : %s" % str(score1))
            # 音乐淡出，播放音效
            laugh_sound.play()
            restart = True

        # 重新开始
        if restart:
            # 重置位置
            ball1.reset()
            bar1.reset()
            bar2.reset()
            # 音乐淡出
            pygame.mixer.music.fadeout(1000)
            # 倒计时文字显示刷新
            for i in [3, 2, 1]:
                # 设置restart文字和321倒数文字
                number_text.change_text(str(i))
                # 刷新画面
                screen.fill(BLACK)
                # 画bar1，bar2和ball
                for each in ALL_Sprites:
                    each.blit()
                score1_text.blit()
                score2_text.blit()
                number_text.blit()
                restart_text.blit()
                pygame.display.flip()
                # 延时1s，使倒数数字之间间隔为1s
                pygame.time.delay(1000)
                # 重新播放音乐
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()
            restart = False
        # 暂停
        while pause:
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                # 退出事件
                if event.type == QUIT:
                    running = False
                    pause = False
                # 按键事件
                elif event.type == KEYDOWN:
                    # 按ESCAPE退出
                    if event.key == K_ESCAPE:
                        print("--退出游戏")
                        running = False
                        pause = False
                    elif event.key == K_SPACE:
                        print("--解除暂停")
                        pause = False
                        pygame.mixer.music.unpause()
                    elif event.key == K_RETURN:
                        print("--重置游戏")
                        restart = True
                        pause = False
                        score1 = 0
                        score2 = 0
                        score1_text.change_text("P1 : %s" % str(score1))
                        score2_text.change_text("P2 : %s" % str(score2))
            pause_text.blit()
            score1_text.blit()
            score2_text.blit()
            pygame.display.flip()
            clock.tick(10)

        # 画面刷新
        # 背景刷黑
        screen.fill(BLACK)
        # 画bar1，bar2和ball
        for each in ALL_Sprites:
            each.blit()
        # 更新所有对象，并显示
        ALL_Sprites.update()
        pygame.display.flip()
        # 帧数设置
        clock.tick(100)

    # 退出
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':

    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()


def full(a, fullscreen=True):
    if fullscreen:
        a = int(a[0] * PROPOTION[0]), int(a[1] * PROPOTION[1])
    else:
        a = int(a[0] / PROPOTION[0]), int(a[1] / PROPOTION[1])
    return a

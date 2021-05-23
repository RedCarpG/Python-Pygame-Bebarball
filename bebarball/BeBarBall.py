""" """
# ------------------------- Import ------------------------- 
import traceback

import pygame
import os
import sys
from pygame.locals import *
from enum import Enum

from bin.bbb_sound import load_sound, load_music
from bin.bbb_myfont import load_font, MyFont
from bin.bbb_items import Ball, Bar
from bin.bbb_local import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

# ------------------------- Init ------------------------- 
# Init Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("BeBarBall")
pygame.mouse.set_visible(False)
# Clock
clock = pygame.time.Clock()
# Init screen
screen = pygame.display.set_mode(SIZE)

# Load Music
load_music("bg.ogg", MAIN_VOLUME)
pygame.mixer.music.play()
# Load Sound
laugh_sound = load_sound("laugh.wav", MAIN_VOLUME)
nope_sound = load_sound("nope.wav", MAIN_VOLUME * 2)
soundGroup = [nope_sound, laugh_sound]
# Load Font
score_font = load_font("arial.ttf", 36)
count_font = load_font("arialbd.ttf", 60)
pause_font = load_font("arialbd.ttf", 70)

SPITES_GROUP = pygame.sprite.Group()
TEXT_GROUP = list()

FULL_SCREEN = False
MUTE = False
ENUM_STATE = Enum('State', ('Entrance', 'Normal', 'Pause', 'Restart'))


def exit_game():
    # 退出
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()


def entrance():
    global screen

    # wait_flag入场界面
    width = screen.get_rect().width
    height = screen.get_rect().height
    screen.fill(COLOR_WAIT_SCREEN)

    wait_flag_font = load_font("arialbd.ttf", 30)
    title_font = load_font("arialbd.ttf", 150)

    start_text = MyFont(screen, wait_flag_font, "Press Any Key To Start",
                        (width // 2, 3 * height // 4), color=GRAY)
    title_text = MyFont(screen, title_font, "BeBarBall", (width // 2, height // 2), color=WHITE)

    TEXT_GROUP.append(start_text)
    TEXT_GROUP.append(title_text)

    start_text.blit()
    title_text.blit()
    pygame.display.flip()

    wait_flag = True
    # wait for signal
    while wait_flag:
        # 全部事件
        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                print("-- Exit")
                exit_game()
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    exit_game()
                elif event.key == K_F11:
                    pygame.display.toggle_fullscreen()
                    start_text.blit()
                    title_text.blit()
                    pygame.display.flip()
                else:
                    wait_flag = False

        global clock
        clock.tick(100)
        # 帧数设置
    TEXT_GROUP.remove(start_text)
    TEXT_GROUP.remove(title_text)
    return 1


def enter_state_normal():
    for each in TEXT_GROUP:
        each.set_visible(False)
    return ENUM_STATE.Normal


def enter_state_restart():
    # 音乐淡出
    pygame.mixer.music.fadeout(1000)
    for each in SPITES_GROUP:
        each.reset()
    for index, each in enumerate(TEXT_GROUP):
        if index < 2:
            each.set_visible(False)
        else:
            each.set_visible(True)
    return ENUM_STATE.Restart


def enter_state_pause():
    pygame.mixer.music.pause()
    for index, each in enumerate(TEXT_GROUP):
        if index < 2:
            each.set_visible(True)
        else:
            each.set_visible(False)

    for each_text in TEXT_GROUP:
        each_text.blit()
    pygame.display.flip()
    return ENUM_STATE.Pause


def main():
    global screen
    volume = 0

    state = ENUM_STATE.Normal
    """ Entrance Screen """
    entrance()
    """ Main Screen """
    width = screen.get_rect().width
    height = screen.get_rect().height


    # 对象
    bar1 = Bar(screen)
    bar2 = Bar(screen)
    ball1 = Ball(screen)
    # 全部对象加入SPITES_GROUP
    SPITES_GROUP.add(bar1)
    SPITES_GROUP.add(bar2)
    SPITES_GROUP.add(ball1)
    # 分数、字体
    score1 = 0
    score2 = 0
    pause_text = MyFont(screen, pause_font, "PAUSE", color=GRAY, visible=False)
    score1_text = MyFont(screen, score_font, "P1 : %s" % str(score1), visible=False)
    score2_text = MyFont(screen, score_font, "P2 : %s" % str(score2), visible=False)
    number_text = MyFont(screen, score_font, " ", visible=False)
    restart_text = MyFont(screen, count_font, "Restart", visible=False)

    w1 = width // 2
    w2 = width // 4
    h1 = height // 2
    h2 = height // 4
    pause_text.move_center((w1, h1))
    restart_text.move_center((w1, h2))
    score1_text.move_center((w2, h1))
    score2_text.move_center((3 * w2, h1))
    number_text.move_center((w1, 2 * height // 5))

    TEXT_GROUP.append(pause_text)
    TEXT_GROUP.append(restart_text)
    TEXT_GROUP.append(score1_text)
    TEXT_GROUP.append(score2_text)
    TEXT_GROUP.append(number_text)

    # 主循环
    flag_exit = False
    while not flag_exit:
        """ Get events """
        events = pygame.event.get()
        # Global event
        for event in events:
            # 退出事件
            if event.type == QUIT:
                print("--退出")
                exit_game()
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    exit_game()
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
                    pygame.display.toggle_fullscreen()

        """ Normal states"""
        if state == ENUM_STATE.Normal:
            for event in events:
                # 按键事件
                if event.type == KEYDOWN:
                    # 方向键（w,s），（up,down）控制bar
                    if event.key == K_w:
                        bar1.move_flag = 1
                    elif event.key == K_s:
                        bar1.move_flag = -1
                    elif event.key == K_UP:
                        bar2.move_flag = 1
                    elif event.key == K_DOWN:
                        bar2.move_flag = -1

                    elif event.key == K_SPACE:
                        print("-- Pause")
                        state = enter_state_pause()
                    elif event.key == K_RETURN:
                        print("-- 重置游戏")
                        state = enter_state_restart()
                        score1 = 0
                        score2 = 0
                        score1_text.change_text("P1 : %s" % str(score1))
                        score2_text.change_text("P2 : %s" % str(score2))

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
            for each in SPITES_GROUP:
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
                state = enter_state_restart()

        """ Restart states"""
        if state == ENUM_STATE.Restart:
            # 倒计时文字显示刷新
            for i in [3, 2, 1]:
                # 设置restart文字和321倒数文字
                number_text.change_text(str(i))
                # 刷新画面
                screen.fill(BLACK)
                # 画bar1，bar2和ball
                for each in SPITES_GROUP:
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
            state = enter_state_normal()

        """ Pause states"""
        if state == ENUM_STATE.Pause:
            enter_state_pause()
            for event in events:
                # 按键事件
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        print("--解除暂停")
                        state = enter_state_normal()
                        pygame.mixer.music.unpause()
                    elif event.key == K_RETURN:
                        print("--重置游戏")
                        state = enter_state_restart()
                        score1 = 0
                        score2 = 0
                        score1_text.change_text("P1 : %s" % str(score1))
                        score2_text.change_text("P2 : %s" % str(score2))
            clock.tick(10)

        # 画面刷新
        # 背景刷黑
        screen.fill(BLACK)
        # 画bar1，bar2和ball
        for each in SPITES_GROUP:
            each.blit()
        # 更新所有对象，并显示
        SPITES_GROUP.update()
        pygame.display.flip()
        # 帧数设置
        clock.tick(100)

    # 退出
    exit_game()


if __name__ == '__main__':

    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

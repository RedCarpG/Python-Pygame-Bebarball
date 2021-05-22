import traceback

import pygame
import sys
from pygame.locals import *
from enum import Enum

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

from bin.bbb_sound import load_sound, load_music
from bin.bbb_myfont import load_font, MyFont
from bin.bbb_items import Ball, Bar, BeBarBallSprite
from bin.bbb_local import *
import bin.bbb_local
from bin.bbb_entrance import entrance
# Init Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
# Clock
clock = pygame.time.Clock()
# Init screen
screen = pygame.display.set_mode(SIZE)
screen.fill(BLACK)
pygame.display.set_caption("BeBarBall")
pygame.mouse.set_visible(False)
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
FULL_SCREEN = False
MUTE = False


def full_cal(a):
    global FULL_SCREEN
    if FULL_SCREEN:
        a = int(a[0] * SCALE[0]), int(a[1] * SCALE[1])
    else:
        a = int(a[0] / SCALE[0]), int(a[1] / SCALE[1])
    return a


def main():
    global screen
    volume = 0
    width = screen.get_rect().width
    height = screen.get_rect().height

    enum_state = Enum('State', ('Normal', 'Pause', 'Restart'))
    state = enum_state.Normal

    entrance(screen, clock)

    # 对象
    bar1 = Bar(screen)
    bar2 = Bar(screen)
    ball1 = Ball(screen)
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
    w1 = width // 2
    w2 = width // 4
    h1 = height // 2
    h2 = height // 4
    pause_text.move_center((w1, h1))
    restart_text.move_center((w1, h2))
    score1_text.move_center((w2, h1))
    score2_text.move_center((3 * w2, h1))
    number_text.move_center((w1, 2 * height // 5))
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
                flag_exit = True
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    flag_exit = True
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
                    global FULL_SCREEN
                    FULL_SCREEN = not FULL_SCREEN
                    # Make full screen
                    if FULL_SCREEN:
                        print("--进入全屏")
                        screen = pygame.display.set_mode(FULL_SIZE, FULLSCREEN | HWSURFACE)
                    # Exit Full screen
                    else:
                        print("--退出全屏")
                        screen = pygame.display.set_mode(SIZE)
                    width = screen.get_rect().width
                    height = screen.get_rect().height
                    print(FULL_SCREEN)
                    for each in ALL_Sprites:
                        each.to_full_screen(full_cal, FULL_SCREEN)

                    pause_text.move_center(full_cal(pause_text.rect.center))
                    restart_text.move_center(full_cal(restart_text.rect.center))
                    score1_text.move_center(full_cal(score1_text.rect.center))
                    score2_text.move_center(full_cal(score2_text.rect.center))
                    number_text.move_center(full_cal(number_text.rect.center))


        """ Normal states"""
        if state == enum_state.Normal:
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
                        state = enum_state.Pause
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
                state = enum_state.Restart

        """ Restart states"""
        if state == enum_state.Restart:
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
            state = enum_state.Normal

        """ Pause states"""
        if state == enum_state.Pause:
            pygame.mixer.music.pause()

            for event in events:
                # 按键事件
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        print("--解除暂停")
                        state = enum_state.Normal
                        pygame.mixer.music.unpause()
                    elif event.key == K_RETURN:
                        print("--重置游戏")
                        state = enum_state.Restart
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

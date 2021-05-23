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
from bin.bbb_items import Ball, Bar, BeBarBallSprite
from bin.bbb_local import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

# ------------------------- Init ------------------------- 


def exit_game():
    # 退出
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()


class BeBarBall(object):

    # Clock
    CLOCK = pygame.time.Clock()
    # Init SCREEN
    SCREEN = pygame.display.set_mode(SIZE)
    # wait_flag入场界面
    WIDTH = SCREEN.get_rect().width
    HEIGHT = SCREEN.get_rect().height
    
    VOLUME = 0
    MUTE = False

    def __init__(self):
        # Init Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("BeBarBall")
        pygame.mouse.set_visible(False)
        
        # Load Music
        load_music("bg.ogg", MAIN_VOLUME)
        pygame.mixer.music.play()
        # Load Sound
        self.laugh_sound = load_sound("laugh.wav", MAIN_VOLUME)
        self.nope_sound = load_sound("nope.wav", MAIN_VOLUME * 2)
        self.sound_group = [self.nope_sound, self.laugh_sound]
        # Load Font
        self.score_font = load_font("arial.ttf", 36)
        self.count_font = load_font("arialbd.ttf", 60)
        self.pause_font = load_font("arialbd.ttf", 70)
        
        self.sprite_group = pygame.sprite.Group()
        self.text_group = list()
        
    def run_entrance(self):
        self.SCREEN.fill(COLOR_WAIT_SCREEN)
    
        wait_flag_font = load_font("arialbd.ttf", 30)
        title_font = load_font("arialbd.ttf", 150)
    
        start_text = MyFont(self.SCREEN, wait_flag_font, "Press Any Key To Start",
                            (self.WIDTH // 2, 3 * self.HEIGHT // 4), color=GRAY)
        title_text = MyFont(self.SCREEN, title_font, "BeBarBall", (self.WIDTH // 2, self.HEIGHT // 2), color=WHITE)
    
        self.text_group.append(start_text)
        self.text_group.append(title_text)
    
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
    
            self.CLOCK.tick(100)
            # 帧数设置
        self.text_group.remove(start_text)
        self.text_group.remove(title_text)
    
    def run_game(self):
        enum_states = Enum('State', ('Entrance', 'Normal', 'Pause', 'Restart'))

        def enter_state_normal():
            for each in self.text_group:
                each.set_visible(False)
            return enum_states.Normal

        def enter_state_restart():
            # 音乐淡出
            pygame.mixer.music.fadeout(1000)
            for each in self.sprite_group:
                each.reset()
            for index, each_text in enumerate(self.text_group):
                if index < 2:
                    each_text.set_visible(False)
                else:
                    each_text.set_visible(True)
            return enum_states.Restart

        def enter_state_pause():
            pygame.mixer.music.pause()
            for index, each in enumerate(self.text_group):
                if index < 2:
                    each.set_visible(True)
                else:
                    each.set_visible(False)
                each.blit()
            pygame.display.flip()
            return enum_states.Pause

        state = enum_states.Normal

        # Object
        bar1 = Bar(self.SCREEN)
        bar2 = Bar(self.SCREEN)
        ball1 = Ball(self.SCREEN)
        self.sprite_group.add(bar1)
        self.sprite_group.add(bar2)
        self.sprite_group.add(ball1)
        # Text
        score1 = 0
        score2 = 0
        pause_text = MyFont(self.SCREEN, self.pause_font, "PAUSE", color=GRAY, visible=False)
        score1_text = MyFont(self.SCREEN, self.score_font, "P1 : %s" % str(score1), visible=False)
        score2_text = MyFont(self.SCREEN, self.score_font, "P2 : %s" % str(score2), visible=False)
        number_text = MyFont(self.SCREEN, self.score_font, " ", visible=False)
        restart_text = MyFont(self.SCREEN, self.count_font, "Restart", visible=False)

        w1 = self.WIDTH // 2
        w2 = self.WIDTH // 4
        h1 = self.HEIGHT // 2
        h2 = self.HEIGHT // 4
        pause_text.move_center((w1, h1))
        restart_text.move_center((w1, h2))
        score1_text.move_center((w2, h1))
        score2_text.move_center((3 * w2, h1))
        number_text.move_center((w1, 2 * self.HEIGHT // 5))

        self.text_group.append(pause_text)
        self.text_group.append(restart_text)
        self.text_group.append(score1_text)
        self.text_group.append(score2_text)
        self.text_group.append(number_text)
        
        self.VOLUME = 0
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
                        if self.VOLUME > - MAIN_VOLUME:
                            print("--音量降低：", self.VOLUME + MAIN_VOLUME)
                            self.VOLUME -= 0.1
                            pygame.mixer.music.set_volume(MAIN_VOLUME + self.VOLUME)
                            for each_sprite in self.sound_group:
                                each_sprite.set_volume(MAIN_VOLUME + self.VOLUME)
                    elif event.key == K_EQUALS:
                        if self.VOLUME < MAIN_VOLUME:
                            print("--音量增加：", self.VOLUME + MAIN_VOLUME)
                            self.VOLUME += 0.1
                            pygame.mixer.music.set_volume(MAIN_VOLUME + self.VOLUME)
                            for each_sprite in self.sound_group:
                                each_sprite.set_volume(MAIN_VOLUME + self.VOLUME)

                    elif event.key == K_F11:
                        pygame.display.toggle_fullscreen()

            """ Normal states"""
            if state == enum_states.Normal:
                # Player button event
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
                # Collision test
                for each_sprite in self.sprite_group:
                    if each_sprite == ball1:
                        continue
                    if ball1.hit(each_sprite):
                        if not each_sprite.hit_flag:
                            each_sprite.hit(ball1)
                            self.nope_sound.play()
                        each_sprite.hit_flag = True
                    else:
                        each_sprite.hit_flag = False
                # Win condition
                if ball1.rect.left < 0 or ball1.rect.right > self.WIDTH:
                    # 到达左边，p2加分
                    if ball1.rect.left < 0:
                        print("--P2得分")
                        score2 += 1
                        score2_text.change_text("P2 : %s" % str(score2))
                    # 到达右边，p1加分
                    elif ball1.rect.right > self.WIDTH:
                        print("--P1得分")
                        score1 += 1
                        score1_text.change_text("P1 : %s" % str(score1))
                    # 音乐淡出，播放音效
                    self.laugh_sound.play()
                    state = enter_state_restart()
            """ Restart states"""
            if state == enum_states.Restart:
                # 倒计时文字显示刷新
                for i in [3, 2, 1]:
                    # 设置restart文字和321倒数文字
                    number_text.change_text(str(i))
                    # 刷新画面
                    self.SCREEN.fill(BLACK)
                    # 画bar1，bar2和ball
                    for each_sprite in self.sprite_group:
                        each_sprite.blit()
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
            if state == enum_states.Pause:
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
                self.CLOCK.tick(10)

            # Screen blit
            self.SCREEN.fill(BLACK)
            # Sprites
            for each_sprite in self.sprite_group:
                each_sprite.blit()
            # Update items
            self.sprite_group.update()
            pygame.display.flip()
            # Frame rate
            self.CLOCK.tick(100)


def main():
    # Game
    game = BeBarBall()
    game.run_entrance()
    game.run_game()
    # Exit
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

"""
Main script
@author RedCarpG
"""
# ------------------------- Import ------------------------- 
import pygame
import sys
from pygame.locals import *
from enum import Enum
from random import randint

from bin.bbb_sound import load_sound, load_music
from bin.bbb_myfont import load_font, MyFont
from bin.bbb_items import Ball, Bar
from bin.bbb_local import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

# ------------------------- Init ------------------------- 


def exit_game():
    """
    System Exit
    @return: None
    """
    # Exit
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()


class BeBarBall(object):
    """
    Class for main game procedure
    """
    # Clock
    CLOCK = pygame.time.Clock()
    # Init SCREEN
    SCREEN = pygame.display.set_mode(SIZE)
    WIDTH = SCREEN.get_rect().width
    HEIGHT = SCREEN.get_rect().height
    # Volume
    VOLUME = 0
    MUTE = False

    COUNT_EVENT = pygame.USEREVENT + 1
    COUNTS = 3

    def __init__(self):
        """
        Init pygame & load resources
        """
        # Init Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("BeBarBall")
        pygame.mouse.set_visible(False)

        # Load Icon
        icon = pygame.image.load("src/bebarball.ico")
        pygame.display.set_icon(icon)
        # Load Music
        load_music("bg.ogg", MAIN_VOLUME)
        pygame.mixer.music.play()
        # Load Sound
        self.lose_sound1 = load_sound("lose1.wav", MAIN_VOLUME)
        self.lose_sound2 = load_sound("lose2.wav", MAIN_VOLUME)
        self.lose_sound3 = load_sound("lose3.wav", MAIN_VOLUME)
        self.nope_sound1 = load_sound("nope1.wav", MAIN_VOLUME * 5)
        self.nope_sound2 = load_sound("nope2.mp3", MAIN_VOLUME)
        # Load Font
        self.score_font = load_font("arial.ttf", 36)
        self.count_font = load_font("arialbd.ttf", 60)
        self.pause_font = load_font("arialbd.ttf", 70)
        # Groups
        self.nope_sound_group = [self.nope_sound1, self.nope_sound2]
        self.lose_sound_group = [self.lose_sound1, self.lose_sound2, self.lose_sound3]
        self.sound_group = [self.nope_sound1, self.nope_sound2, self.lose_sound1, self.lose_sound2, self.lose_sound3]
        self.sprite_group = pygame.sprite.Group()
        self.text_group = list()
        
    def run_entrance(self):
        """
        Entrance procedure
        @return: None
        """
        self.SCREEN.fill(COLOR_WAIT_SCREEN)
    
        start_font = load_font("arial.ttf", 30)
        title_font = load_font("arialbd.ttf", 150)
    
        start_text = MyFont(self.SCREEN, start_font, "Press Any Key To Start",
                            (self.WIDTH // 2, 3 * self.HEIGHT // 4), color=GRAY)
        title_text = MyFont(self.SCREEN, title_font, "BeBarBall", (self.WIDTH // 2, self.HEIGHT // 2), color=WHITE)
    
        self.text_group.append(start_text)
        self.text_group.append(title_text)
    
        start_text.blit()
        title_text.blit()
        pygame.display.flip()

        ''' Waiting for trigger '''
        wait_flag = True
        while wait_flag:
            ''' Trigger events '''
            for event in pygame.event.get():
                # Exit
                if event.type == QUIT:
                    print("-- Exit Game")
                    exit_game()
                    return False
                # Button press event
                elif event.type == KEYDOWN:
                    # 按ESCAPE退出
                    if event.key == K_ESCAPE:
                        print("-- Exit Game")
                        exit_game()
                        return False
                    elif event.key == K_F11:
                        pygame.display.toggle_fullscreen()
                        start_text.blit()
                        title_text.blit()
                        pygame.display.flip()
                    else:
                        wait_flag = False
            # Frame rate
            self.CLOCK.tick(100)
        self.text_group.remove(start_text)
        self.text_group.remove(title_text)
        return True

    def run_game(self):
        """
        Main game
        @return: None
        """
        class EnumStates(Enum):
            Entrance = 0
            Normal = 1
            Pause = 2
            Restart = 3
        state = EnumStates.Normal

        # Enter function for Normal state
        def enter_state_normal():
            for each in self.text_group:
                each.set_visible(False)
            return EnumStates.Normal

        # Enter function for Restart state
        def enter_state_restart():
            BeBarBall.COUNTS = 3
            number_text.change_text(str(BeBarBall.COUNTS))
            # Count Event
            pygame.time.set_timer(self.COUNT_EVENT, 1000)
            # Music fade
            pygame.mixer.music.fadeout(1000)
            # Reset objects
            for each in self.sprite_group:
                each.reset()
            # Blit restart text
            for index, each_text in enumerate(self.text_group):
                if index < 1:
                    each_text.set_visible(False)
                else:
                    each_text.set_visible(True)
            return EnumStates.Restart

        # Enter function for Pause state
        def enter_state_pause():
            # Pause music
            pygame.mixer.music.pause()
            # Blit pause text
            for index, each in enumerate(self.text_group):
                if index < 1:
                    each.set_visible(True)
                else:
                    each.set_visible(False)
                each.blit()
            pygame.display.flip()
            return EnumStates.Pause

        # Objects
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
        number_text = MyFont(self.SCREEN, self.score_font, "", visible=False)
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

        # Main loop
        flag_exit = False
        while not flag_exit:
            """ Events """
            # ---------------- Global event ----------------
            events = pygame.event.get()
            for event in events:
                # --- Exit Event
                if event.type == QUIT:
                    print("-- Exit")
                    # flag_exit = True
                    exit_game()
                    return 0
                # =--- Button press Events
                elif event.type == KEYDOWN:
                    # ‘Escape’ Button
                    if event.key == K_ESCAPE:
                        print("-- Exit")
                        # flag_exit = True
                        exit_game()
                        return 0
                    # ‘-’ Button
                    elif event.key == K_MINUS:
                        if self.VOLUME > - MAIN_VOLUME:
                            print("-- Volume down：", self.VOLUME + MAIN_VOLUME)
                            self.VOLUME -= 0.1
                            pygame.mixer.music.set_volume(MAIN_VOLUME + self.VOLUME)
                            for each_sprite in self.sound_group:
                                each_sprite.set_volume(MAIN_VOLUME + self.VOLUME)
                    # ‘=’ Button
                    elif event.key == K_EQUALS:
                        if self.VOLUME < MAIN_VOLUME:
                            print("-- Volume up：", self.VOLUME + MAIN_VOLUME)
                            self.VOLUME += 0.1
                            pygame.mixer.music.set_volume(MAIN_VOLUME + self.VOLUME)
                            for each_sprite in self.sound_group:
                                each_sprite.set_volume(MAIN_VOLUME + self.VOLUME)
                    # 'F11' Button
                    elif event.key == K_F11:
                        pygame.display.toggle_fullscreen()
            """ States """
            # ---------------- Normal states ----------------
            if state == EnumStates.Normal:
                # -------- Player button event --------
                for event in events:
                    # --- Button press Events
                    if event.type == KEYDOWN:
                        # """ Direction buttons (w,s) & (up,down) to move <Bar>s """
                        # 'w' Button
                        if event.key == K_w:
                            bar1.move_flag = 1
                        # 's' Button
                        elif event.key == K_s:
                            bar1.move_flag = -1
                        # 'up' Button
                        elif event.key == K_UP:
                            bar2.move_flag = 1
                        # 'down' Button
                        elif event.key == K_DOWN:
                            bar2.move_flag = -1
                        # """ (space) button to pause game """
                        # 'space' Button
                        elif event.key == K_SPACE:
                            print("-- Pause Game")
                            state = enter_state_pause()
                        # """ (return) button to restart """
                        # 'return' Button
                        elif event.key == K_RETURN:
                            print("-- Restart Game")
                            state = enter_state_restart()
                            score1 = 0
                            score2 = 0
                            score1_text.change_text("P1 : %s" % str(score1))
                            score2_text.change_text("P2 : %s" % str(score2))
                    # --- Button release Events
                    elif event.type == KEYUP:
                        # """ Release direction buttons (w,s) & (up,down) to stop <Bar>s """
                        # 'w' button
                        if event.key == K_w and bar1.move_flag == 1:
                            bar1.move_flag = 0
                        # 's' button
                        if event.key == K_s and bar1.move_flag == -1:
                            bar1.move_flag = 0
                        # 'up' button
                        if event.key == K_UP and bar2.move_flag == 1:
                            bar2.move_flag = 0
                        # 'down' button
                        if event.key == K_DOWN and bar2.move_flag == -1:
                            bar2.move_flag = 0
                # -------- Collision test --------
                for each_sprite in self.sprite_group:
                    if each_sprite == ball1:
                        continue
                    # """ If the ball hit the bars """
                    if ball1.hit(each_sprite):
                        if not each_sprite.hit_flag:
                            each_sprite.hit(ball1)
                            self.nope_sound_group[randint(0, len(self.nope_sound_group)-1)].play()
                        each_sprite.hit_flag = True
                    else:
                        each_sprite.hit_flag = False
                # -------- Win condition --------
                if ball1.rect.left < 0 or ball1.rect.right > self.WIDTH:
                    # Ball reaches Left, p2 score
                    if ball1.rect.left < 0:
                        print("-- P2 Score")
                        score2 += 1
                        score2_text.change_text("P2 : %s" % str(score2))
                    # Ball reaches Right, p1 score
                    elif ball1.rect.right > self.WIDTH:
                        print("-- P1 Score")
                        score1 += 1
                        score1_text.change_text("P1 : %s" % str(score1))
                    # Play sound
                    self.lose_sound_group[randint(0, len(self.lose_sound_group)-1)].play()
                    state = enter_state_restart()
                # -------- Update items --------
                self.sprite_group.update()
            # ----------------  Pause states ----------------
            elif state == EnumStates.Pause:
                # -------- Player button event --------
                for event in events:
                    # --- Button press Events
                    if event.type == KEYDOWN:
                        # 'space' button
                        if event.key == K_SPACE:
                            print("-- Resume Game")
                            pygame.mixer.music.unpause()
                            state = enter_state_normal()
                        # 'return' button
                        elif event.key == K_RETURN:
                            print("-- Restart Game")
                            score1 = 0
                            score2 = 0
                            score1_text.change_text("P1 : %s" % str(score1))
                            score2_text.change_text("P2 : %s" % str(score2))
                            state = enter_state_restart()
                self.CLOCK.tick(1000)
            # ----------------  Restart states ----------------
            elif state == EnumStates.Restart:
                # -------- Count event --------
                for event in events:
                    if event.type == self.COUNT_EVENT:
                        BeBarBall.COUNTS -= 1
                        number_text.change_text(str(BeBarBall.COUNTS))
                        if BeBarBall.COUNTS == 0:
                            BeBarBall.COUNTS = 3
                            pygame.mixer.music.rewind()
                            pygame.mixer.music.play()
                            state = enter_state_normal()
            """ Blit objects """
            # Screen blit
            self.SCREEN.fill(BLACK)
            # Sprites
            for each_sprite in self.sprite_group:
                each_sprite.blit()
            # Texts
            for each_text in self.text_group:
                each_text.blit()
            pygame.display.flip()

            # Frame rate
            self.CLOCK.tick(100)


def main():
    # Game
    game = BeBarBall()
    if game.run_entrance():
        game.run_game()
    # Exit
    exit_game()


if __name__ == '__main__':
    """
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
    """
    main()

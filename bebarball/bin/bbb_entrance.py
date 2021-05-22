import pygame
from pygame.locals import *
from .bbb_local import *
from .bbb_myfont import MyFont, load_font


def entrance(screen, clock):
    # wait_flag入场界面
    width = screen.get_rect().width
    height = screen.get_rect().height
    screen.fill(COLOR_WAIT_SCREEN)

    wait_flag_font = load_font("arialbd.ttf", 30)
    title_font = load_font("arialbd.ttf", 150)
    wait_flag_text = MyFont(screen, wait_flag_font, "Press Any Key To wait_flag", (width // 2, 3 * height // 4), color=GRAY)
    title_text = MyFont(screen, title_font, "BeBarBall", (width // 2, height // 2), color=WHITE)
    wait_flag_text.blit()
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
                running = False
                wait_flag = False
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    print("--退出")
                    running = False
                    wait_flag = False
                elif event.key == K_F11:
                    pass
                else:
                    wait_flag = False
                    # 帧数设置
        clock.tick(10)

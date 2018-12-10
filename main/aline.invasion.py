# AUTHOR : YYQLK
import pygame
from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import Game_Stats
from button import Button

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #创建一个飞船
    ship = Ship(screen,ai_settings)
    #创建一个游戏统计信息的实例
    stats = Game_Stats(ai_settings)

    #外星人编组
    aliens = Group()
    #子弹编组
    bullets = Group()
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #创建Play按钮
    play_button = Button(screen, "play")
    #开始游戏的主循环
    while True:

        #监听键盘和鼠标事件
        gf.check_event(ship, ai_settings, screen, bullets, stats, play_button, aliens, ai_settings)
        if stats.game_active:
            #更新飞船位置
            ship.update()
            #更新子弹位置并删除消失的子弹
            gf.update_bullets(bullets,aliens)
            #移动外星人
            gf.update_aliens(stats, ai_settings, bullets,aliens, ship,screen)
        #更新屏幕上的图像，并切换到新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button)

run_game()

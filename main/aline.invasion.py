# AUTHOR : YYQLK
import pygame
from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #创建一个飞船
    ship = Ship(screen,ai_settings)
    #外星人编组
    aliens = Group()
    #子弹编组
    bullets = Group()

    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #开始游戏的主循环
    while True:

        #监听键盘和鼠标事件
        gf.check_event(ship, ai_settings, screen, bullets)
        #更新飞船位置
        ship.update()
        #更新子弹位置并删除消失的子弹
        gf.update_bullets(bullets)
        #移动外星人
        # gf.update_aliens(ai_settings,aliens)
        #更新屏幕上的图像，并切换到新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens)

run_game()

# AUTHOR : YYQLK
import sys
from bullet import Bullet
import pygame
from alien import Alien
from time import sleep


def fire_bullet(bullets,ai_setting, screen, ship):
    if len(bullets) < ai_setting.bullets_allowed:
        # 创建一颗子弹，并将它加入到编组bullets中
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def check_keydown_event(event,ship,ai_setting,screen,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_setting, screen, ship)

def check_paly_button(stats, play_button, mouse_x, mouse_y,aliens, bullets, ship, ai_settings, screen):
    '''单击play时开始游戏'''
    if play_button.rect.collidepoint(mouse_x,mouse_y)\
            and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        #隐藏光标
        pygame.mouse.set_visible(False)
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放再屏幕顶端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def check_keyup_event(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_event(ship,ai_setting, screen, bullets, stats, play_button, aliens, ai_settings):
    # 监听键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 左右移动飞船
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ship, ai_setting, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_paly_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, ai_settings, screen)


def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可以容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x


def get_number_aliens_y(ai_settings, ship_height, alien_height):
    '''计算屏幕能容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height)- ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    '''创建一个外星人获取其rect，然后添加到aliens中'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)
    alien.x = alien.rect.x


def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    number_aliens_x = get_number_aliens_x(ai_settings,alien_width)
    number_rows = get_number_aliens_y(ai_settings, ship_height,
                                      alien_height)

    #创建一群外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    '''检查外星人到达边缘采取相应措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            # alien.rect.y += ai_settings.fleet_drop_speed
            change_fleet_direction(ai_settings,aliens)
            # ai_settings.fleet_direction *= -1
            break

def check_fleet_bottom(screen, stats, aliens, bullets, ai_settings, ship,):
    '''检查外星人到达屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(stats, aliens, bullets, ai_settings, ship, screen)


def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(stats, ai_settings, bullets,aliens, ship,screen):
    '''更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(stats, aliens, bullets, ai_settings, ship, screen)

def update_bullets(bullets,aliens):
    '''更新子弹的位置,并删除消失的子弹，检查子弹和外星人的碰撞'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #检查是否有子弹击中了外星人
    #如果击中了，就删除相应的外星人和子弹
    collision = pygame.sprite.groupcollide(bullets,aliens,True,True)

def ship_hit(stats, aliens, bullets, ai_settings, ship, screen):
    '''相应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        #将ship_left减1
        stats.ships_left -=1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放再屏幕顶端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环都是重绘
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    # 让最近回执的屏幕可见
    pygame.display.flip()

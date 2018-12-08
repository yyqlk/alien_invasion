# AUTHOR : YYQLK
import sys
from bullet import Bullet
import pygame
from alien import Alien


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



def update_bullets(bullets):
    '''更新子弹的位置'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_keyup_event(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_event(ship,ai_setting, screen, bullets):
    # 监听键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 左右移动飞船
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ship, ai_setting, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


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
    print(alien.rect)


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
    print(alien.rect)


def check_fleet_edges(ai_settings, aliens):
    '''检查外星人到达边缘采取相应措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    '''更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()


def update_screen(ai_settings, screen, ship, bullets, aliens):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环都是重绘
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近回执的屏幕可见
    pygame.display.flip()

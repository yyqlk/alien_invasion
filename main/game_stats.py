# AUTHOR : YYQLK
class Game_Stats():
    '''跟踪游戏的统计信息'''
    def __init__(self,ai_settings):
        self.ai_setting = ai_settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        '''初始化游戏运行期间可能变化的统计信息'''
        self.ships_left = self.ai_setting.ship_limit

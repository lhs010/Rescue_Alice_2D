import pygame
import sys
import level
import media
import tools

window_width = 570
window_height = 400
progress_file_path = './static/level_progress.json'


class Manager:

    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))

    def main(self):
        # 主页面
        pygame.display.set_caption("拯救爱丽丝")
        self.main_draw()

    # 主界面绘制
    def main_draw(self):
        # 绘制主界面
        media.GameBackground().main(self.screen)
        # 绘制主背景音乐
        media.Music().main()
        # 绘制主标题
        tools.drawText(self.screen, "拯救爱丽丝", 150, 100, 50, (255, 255, 155))
        # 刷新界面
        pygame.display.flip()
        # 读取进度文件不存在则创建
        progress_info = ""
        try:
            with open(progress_file_path, "r") as f:
                progress_info = f.read()
        except FileNotFoundError:
            with open(progress_file_path, 'w') as file:
                file.write("")  # 创建一个空文件
        # 等待玩家输入
        if progress_info == "":
            tools.waitPlayerInput(self.screen, "按下S键开始游戏", pygame.K_s)
        else:
            # 绘制提示文字
            tools.drawText(self.screen, "按下S键继续游戏", 300, 320, 15, (255, 255, 255))
            tools.drawText(self.screen, "按下D键开始新游戏", 300, 350, 15, (255, 255, 255))
            pygame.display.flip()
            # 等待玩家输入
            input_key = None
            wait_input = True
            while wait_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and (event.key in  [pygame.K_s,pygame.K_d]):
                        input_key = event.key
                        # 清空事件队列
                        pygame.event.clear()
                        # 清空事件队列
                        pygame.event.clear()
                        wait_input = False
                        break
            if input_key == pygame.K_d:
                # 清空进度文件
                with open(progress_file_path, 'w') as file:
                    file.write("")
        self.game_start()
        # 刷新界面
        pygame.display.flip()
        return

    def game_start(self):
        # 开始游戏
        pygame.display.flip()
        # 加载关卡
        level.GameLevel().level_1(self.screen)
        level.GameLevel().level_2(self.screen)
        return

    def game_quit(self):
        # 退出游戏
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    manager = Manager()
    manager.main()

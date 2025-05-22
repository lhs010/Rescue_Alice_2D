import pygame

# 游戏背景类
class GameBackground(object):

    def __init__(self):
        import main
        self.window_width = main.window_width
        self.window_height = main.window_height

    def main(self, screen):
        # 绘制主背景图片
        bgi = pygame.image.load("./static/level/main_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (self.window_width, self.window_height))
        screen.blit(bgi, (0, 0))

    def level_1(self, screen):
        # 关卡1背景图片
        bgi = pygame.image.load("./static/level/level_1_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (self.window_width, self.window_height))
        screen.blit(bgi, (0, 0))

    def level_1_plot(self, screen):
        # 关卡1剧情背景图片
        bgi = pygame.image.load("./static/level/level_1_plot.jpg")
        bgi = pygame.transform.scale(bgi, (self.window_width, self.window_height))
        screen.blit(bgi, (0, 0))

    def level_2(self, screen):
        # 关卡2背景图片
        bgi = pygame.image.load("./static/level/level_2_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (self.window_width, self.window_height))
        screen.blit(bgi, (0, 0))

    def level_2_plot(self, screen):
        # 关卡2剧情背景图片
        bgi = pygame.image.load("./static/level/level_2_plot.jpg")
        bgi = pygame.transform.scale(bgi, (self.window_width, self.window_height))
        screen.blit(bgi, (0, 0))


class Music(object):

    def main(self):
        # 主背景音乐
        pygame.mixer.music.load("./static/music/bgm.ogg")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def level(self):
        # 关卡背景音乐
        pygame.mixer.music.load("./static/music/level_bgm.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def plot(self):
        # 剧情背景音乐
        pygame.mixer.music.load("./static/music/plot_bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def pass_level(self):
        # 通关音效
        pygame.mixer.music.load("./static/music/bgm.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

    def hurt(self):
        # 受伤音效
        pygame.mixer.music.load("./static/music/hurt.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

    def death(self):
        # 死亡音效
        pygame.mixer.music.load("./static/music/death.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

    def up(self):
        # 升级音效
        pygame.mixer.music.load("./static/music/up.ogg")
        pygame.mixer.music.play()

# 平台类
class Platform(object):
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 长平台类
class LongPlatform:
    def __init__(self, x, y, length, image):
        self.x = x
        self.y = y
        self.length = length  # 瓦片数量
        self.tile_width, self.tile_height = image.get_size()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        for i in range(self.length):
            screen.blit(self.image, (self.x + i * self.tile_width, self.y))

import pygame
import sys
import random
import json

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
        GameBackground().main(self.screen)
        # 绘制主背景音乐
        Music().main()
        # 绘制主标题
        drawText(self.screen, "拯救爱丽丝", 150, 100, 50, (255, 255, 155))
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
            waitPlayerInput(self.screen, "按下S键开始游戏", pygame.K_s)
        else:
            # 绘制提示文字
            drawText(self.screen, "按下S键继续游戏", 300, 320, 15, (255, 255, 255))
            drawText(self.screen, "按下D键开始新游戏", 300, 350, 15, (255, 255, 255))
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
                progress_info = ""
        self.game_start(progress_info)
        # 刷新界面
        pygame.display.flip()
        return

    def game_start(self, progress_info=""):
        # 开始游戏
        pygame.display.flip()
        # 初始化玩家对象
        playerObj = Player()
        if progress_info != "":
            playerObj = self.load_progress(playerObj, progress_info)
        # 加载关卡
        GameLevel().level_1(self.screen, playerObj)
        GameLevel().level_2(self.screen, playerObj)
        return

    def game_quit(self):
        # 退出游戏
        pygame.quit()
        sys.exit()
        
    def load_progress(self, playerObj, progress_info):
        # 载入进度
        progress_info = json.loads(progress_info)
        # 玩家速度
        playerObj.player_speed = progress_info["player_speed"]
        # 玩家等级
        playerObj.player_level = progress_info["player_level"]
        # 玩家经验
        playerObj.player_exp = progress_info["player_exp"]
        # 玩家生命值
        playerObj.player_hp = progress_info["player_hp"]
        # 玩家攻击力
        playerObj.player_attack = progress_info["player_attack"]
        # 每次升级需要经验
        playerObj.player_exp_needed = progress_info["player_exp_needed"]
        # 当前关卡
        playerObj.current_level = progress_info["current_level"]
        return playerObj

def drawText(screen, text, x, y, textHeight=30, fontColor=(255, 255, 255), backgroudColor=None):
    # 通过字体文件获得字体对象 参数1 字体文件 参数2 字体大小
    font_obj = pygame.font.Font('./static/baddf.ttf', textHeight)
    # 1文字 2是否抗锯齿 3文字颜色 4背景颜色
    text_obj = font_obj.render(text, True, fontColor, backgroudColor)  # 配置要显示的文字
    # 获取要显示的对象rect
    text_rect = text_obj.get_rect()
    # 设置显示对象的坐标
    text_rect.topleft = (x, y)
    # 绘制字 到指定区域 参数1时文字对象 参数2是矩形对象
    screen.blit(text_obj, text_rect)
    return


def drawTextCenter(screen, text, textHeight=30, fontColor=(255, 255, 255), backgroudColor=None):
    # 打字机音效
    type_sound = pygame.mixer.Sound("./static/typewriter.mp3")
    # 初始显示的空字符串
    display_text = ""

    # 逐字显示
    line_height = 30  # 行高
    current_line = ""  # 当前行文本
    skip = False  # 是否跳过逐字显示
    for char in text:
        # 提示用户按下空格跳过
        drawText(screen, "按下空格跳过...", 300, 350, textHeight, fontColor, backgroudColor)
        pygame.display.flip()
        # 检测事件
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                skip = True
        if skip:
            # 直接渲染全部文本
            lines = text.split('\n')
            for i, line in enumerate(lines):
                drawText(screen, line, 50, 50 + i * line_height, textHeight, fontColor, backgroudColor)
            pygame.display.flip()
            break

        # 播放打字音效
        type_sound.play()
        # 添加一个字符
        display_text += char
        current_line += char

        # 处理换行
        if char == '\n':
            current_line = ""
            continue

        # 绘制文本（按行绘制）
        lines = display_text.split('\n')
        for i, line in enumerate(lines):
            drawText(screen, line, 50, 50 + i * line_height, textHeight, fontColor, backgroudColor)
            pygame.display.flip()

        # 刷新界面
        pygame.display.flip()
        # 控制显示速度（单位：毫秒）
        pygame.time.delay(100)
        # 随机延迟，模拟真实打字机效果
        pygame.time.delay(random.randint(0, 100))


def waitPlayerInput(screen, text="", eventKey=pygame.K_s):
    # 绘制提示文字
    if text != "":
        drawText(screen, text, 300, 350, 15, (255, 255, 255))
        pygame.display.flip()
    # 等待玩家输入
    wait_input = True
    while wait_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == eventKey:
                # 清空事件队列
                pygame.event.clear()
                wait_input = False
                break
    return


class GameLevel(object):
        
    def platform_1_image(self):
        bgi = pygame.image.load("./static/platform_1.png").convert_alpha()
        return bgi

    def platform_2_image(self):
        bgi = pygame.image.load("./static/platform_2.png").convert_alpha()
        return bgi
    
    def pass_level(self,screen, playerObj):
        # 播放通关音效
        Music().pass_level()
        # 显示下一关入口
        image = pygame.image.load("./static/y.png")
        image = pygame.transform.scale(image, (80, 80))
        screen.blit(image, (430, 220))
        drawText(screen, "向前进入下一关", 380, 180, 20)
        if playerObj.x >= 520:
            # 保存关卡进度
            playerObj.current_level += 1
            playerObj.save_level_progress()
            return True
        return False

    def level_1(self, screen, playerObj):
        if playerObj.current_level != 1:
            return
        clock = pygame.time.Clock()
        # 绘制背景# 绘制剧情音乐
        Music().plot()
        # 绘制剧情背景
        GameBackground().level_1_plot(screen)
        # 游戏文字
        text = GameText().level_1()
        # 绘制剧情摘要
        drawTextCenter(screen, text, 20, (255, 255, 255))
        # 等待用户输入
        waitPlayerInput(screen, "", pygame.K_s)
        # 绘制关卡音乐
        Music().level()
        # 绘制NPC
        npc_image = Role().npc_1()
        # 是否与npc互动
        is_npc_interactive = False
        # 重置玩家位置
        playerObj.reset_player_pos()
        # npc位置
        npc_x = window_width
        npc_y = 310
        # 初始化游戏平台
        platforms = [
            Platform(0, 380, window_width, 20, self.platform_1_image())
        ]
        # 绘制敌人
        enemies = [
            Enemy(450, 300, "left", 1, 1),
        ]
        pygame.display.flip()
        # 游戏开始
        game_over = False
        while not game_over:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and playerObj.on_ground:
                        playerObj.vel_y = playerObj.jump_power
                    elif event.key == pygame.K_a:
                        playerObj.attack()
            # 绘制背景
            GameBackground().level_1(screen)
            # 绘制平台
            for platform in platforms:
                platform.draw(screen)
            # 玩家移动
            playerObj.player_move(screen)
            # 更新玩家碰撞
            playerObj.update_collision(platforms)
            # 绘制玩家面板
            playerObj.player_info(screen)
            # 绘制玩家
            playerObj.draw(screen)
            # 绘制敌人
            for enemy in enemies:
                if enemy.is_dead:
                    enemies.remove(enemy)
                    continue
                else:
                    enemy.attack(screen, playerObj)  # 非阻塞逐帧更新动画
                    if enemy.speed != 0:
                        enemy.move(screen, platforms)
            # 绘制玩家攻击
            for target in playerObj.remote_attack_targets:
                if target.is_alive:
                    target.draw(screen)
                    target.update(screen, platforms,enemies,playerObj)
                else:
                    playerObj.remote_attack_targets.remove(target)
            # 玩家升级检测
            playerObj.player_level_up(screen)
            if is_npc_interactive:
                game_over = self.pass_level(screen, playerObj)
            elif enemies is None or len(enemies) == 0:
                # 绘制NPC从右边滑出
                if npc_x > 450:
                    screen.blit(pygame.transform.flip(npc_image, True, False), (npc_x, npc_y))
                    npc_x -= 3
                else:
                    # 绘制NPC
                    screen.blit(pygame.transform.flip(npc_image, True, False), (npc_x, npc_y))
                    # 玩家和NPC互动检测
                    npc_rect = npc_image.get_rect(topleft=(npc_x, npc_y))
                    if npc_rect.colliderect(playerObj.rect):
                        pygame.image.save(screen, "./static/temp.jpg")
                        # 绘制交互提示
                        drawText(screen, "按'F'键与NPC互动", 200, 150, 20, (255, 255, 255))
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_f]:
                            is_npc_interactive = True
                            sbgi = pygame.image.load("./static/temp.jpg")
                            sbgi = pygame.transform.scale(sbgi, (window_width, window_height))
                            screen.blit(sbgi, (0, 0))
                            # 主视图加灰色半透明蒙层
                            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                            overlay.fill((0, 0, 0, 128))  # 半透明
                            screen.blit(overlay, (0, 0))
                            # 截取并保存屏幕
                            pygame.image.save(screen, "./static/temp.jpg")
                            text_list = [
                                ["npc", "你好弗兰克!"],
                                ["npc", "我等你很久了"],
                                ["player", "你是什么人？"],
                                ["npc", "别担心，我不是那个天网组织的人"],
                                ["npc", "我叫布利斯，也是一名生物科学家"],
                                ["npc", "我知道所有发生在你身上的事"],
                                ["npc", "我会帮助你救回你的家人"],
                                ["player", "你为什么帮我？你有什么目的？"],
                                ["npc", "因为我的家人也被那帮畜生抓走了"],
                                ["npc", "我帮你事实上也是在帮我自己，请你相信我"],
                                ["player", "好吧，我可以相信你，那现在你有什么线索吗？"],
                                ["npc", "不好意思，目前还没有"],
                                ["npc", "不过你可以去13区看看，说不定会有线索"],
                                ["player", "好吧，我马上去"],
                                ["npc", "那先再见了，我们很快会再见的"],
                                ["player", "嗯嗯"],
                            ]
                            npc_big_image = pygame.transform.scale(npc_image, (300, 350))
                            player_big_image = pygame.transform.scale(playerObj.player_image, (300, 300))
                            for text in text_list:
                                # 清空事件队列
                                pygame.event.clear()
                                if text[0] == "player":
                                    screen.blit(player_big_image, (-100, 50))
                                else:
                                    screen.blit(pygame.transform.flip(npc_big_image, True, False), (330, 100))
                                drawText(screen, text[1], 150, 200, 15, (255, 255, 255))
                                # 等待用户按下任意键
                                waitPlayerInput(screen, "按'F'键继续...", pygame.K_f)
                                # 渲染快照背景图，用于清除本次交互内容
                                sbgi = pygame.image.load("./static/temp.jpg")
                                sbgi = pygame.transform.scale(sbgi, (window_width, window_height))
                                screen.blit(sbgi, (0, 0))
                            # 玩家获得经验
                            playerObj.player_exp += 100
            # 更新显示
            pygame.display.flip()
            # 控制帧率
            clock.tick(60)
        return

    def level_2(self, scrren, playerObj):
        pass


class GameBackground(object):

    def main(self, screen):
        # 绘制主背景图片
        bgi = pygame.image.load("./static/main_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (window_width, window_height))
        screen.blit(bgi, (0, 0))

    def level_1(self, screen):
        # 关卡1背景图片
        bgi = pygame.image.load("./static/level_1_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (window_width, window_height))
        screen.blit(bgi, (0, 0))

    def level_1_plot(self, screen):
        # 关卡1剧情背景图片
        bgi = pygame.image.load("./static/level_1_plot.jpg")
        bgi = pygame.transform.scale(bgi, (window_width, window_height))
        screen.blit(bgi, (0, 0))

    def level_2(self, screen):
        # 关卡2背景图片
        bgi = pygame.image.load("./static/level_2_bgi.jpg")
        bgi = pygame.transform.scale(bgi, (window_width, window_height))
        screen.blit(bgi, (0, 0))

    def level_2_plot(self, screen):
        # 关卡2剧情背景图片
        bgi = pygame.image.load("./static/level_2_plot.jpg")
        bgi = pygame.transform.scale(bgi, (window_width, window_height))
        screen.blit(bgi, (0, 0))


class Music(object):

    def main(self):
        # 主背景音乐
        pygame.mixer.music.load("./static/bgm.ogg")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def level(self):
        # 关卡背景音乐
        pygame.mixer.music.load("./static/level_bgm.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def plot(self):
        # 剧情背景音乐
        pygame.mixer.music.load("./static/plot_bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def pass_level(self):
        # 通关音效
        pygame.mixer.music.load("./static/pass_level.ogg")
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.5)


class Player(object):

    def __init__(self):
        # 玩家位置
        self.x = -20
        self.y = 230
        # 玩家速度
        self.player_speed = 5
        # 玩家宽度
        self.width = 80
        # 玩家高度
        self.height = 80
        # 玩家朝向
        self.player_direction = "right"
        # 玩家状态
        self.player_state = "idle"
        # 玩家动作
        self.player_action = "idle"
        # 玩家等级
        self.player_level = 1
        # 玩家经验
        self.player_exp = 0
        # 玩家生命值
        self.player_hp = 100
        # 玩家攻击力
        self.player_attack = 10
        # 攻击频率
        self.attack_frequency = 0.5
        # 上次攻击时间
        self.last_attack_time = 0
        # 远程攻击对象列表
        self.remote_attack_targets = []
        # 每次升级需要经验
        self.player_exp_needed = 100
        # 玩家移动总距离
        self.total_distance = 0
        # 玩家图片
        self.player_image = Role().role_1((self.width, self.height))
        # 创建用于碰撞检测的矩形区域
        self.rect = self.player_image.get_rect(topleft=(self.x, self.y))
        # 玩家跳跃
        self.vel_y = 0
        # 玩家跳跃力
        self.jump_power = -12
        # 玩家重力
        self.gravity = 0.5
        # 玩家是否在地面上
        self.on_ground = False
        # 当前关卡
        self.current_level = 1

    # 玩家详情信息
    def player_info(self, screen):
        # 玩家面板
        drawText(screen, "等级: " + str(self.player_level), 10, 10, 10, (255, 255, 255))
        drawText(screen, "经验: " + str(self.player_exp) + "/" + str(self.player_exp_needed), 10, 20, 10,
                 (255, 255, 255))
        drawText(screen, "血量: " + str(int(self.player_hp)), 10, 30, 10, (255, 255, 255))
        drawText(screen, "攻击力: " + str(int(self.player_attack)), 10, 40, 10, (255, 255, 255))
        drawText(screen, "位置: [" + str(self.x) + "," + str(self.y) + "]", 10, 50, 10, (255, 255, 255))

    # 玩家升级
    def player_level_up(self, screen):
        # 玩家升级检测
        if self.player_exp >= self.player_exp_needed:
            # 主视图加灰色半透明蒙层
            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 半透明
            screen.blit(overlay, (0, 0))
            # 显示升级信息
            drawText(screen, "等级提升!", 200, 50, 30, (255, 255, 0))
            drawText(screen, "等级: " + str(self.player_level) + " -> " + str(self.player_level + 1), 200, 90, 20,
                     (0, 255, 255))
            drawText(screen, "血量: " + str(int(self.player_hp)) + " -> " + str(
                self.player_hp + int(self.player_hp * self.player_level * 0.05)), 200, 110, 20, (0, 255, 255))
            drawText(screen, "攻击力: " + str(int(self.player_attack)) + " -> " + str(
                self.player_attack + int(self.player_attack * self.player_level * 0.2)), 200, 130, 20, (0, 255, 255))
            # 更新玩家信息
            self.player_level += 1
            self.player_exp = self.player_exp - self.player_exp_needed
            self.player_exp_needed += self.player_exp_needed * self.player_level * 0.5
            self.player_hp += self.player_hp * self.player_level * 0.05
            self.player_attack += self.player_attack * self.player_level * 0.2
            # 播放升级音效
            pygame.mixer.music.load("./static/up.ogg")
            pygame.mixer.music.play()
            # 等待用户输入
            waitPlayerInput(screen, "按'F'键继续...", pygame.K_f)
        return

    # 玩家攻击
    def attack(self):
        # 攻击频率控制
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_frequency * 1000:
            x = self.x + 60
            y = self.y + 20
            if self.player_direction == "left":
                x = self.x - 10
            self.remote_attack_targets.append(Fireball(x, y, self.player_direction, self.player_attack))
            self.last_attack_time = current_time
        return

    # 玩家移动
    def player_move(self,screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.player_speed
            self.total_distance -= self.player_speed
            self.player_direction = "left"
            self.player_state = "walk"
            self.rect.x = self.x
        if keys[pygame.K_RIGHT]:
            self.x += self.player_speed
            self.total_distance += self.player_speed
            self.player_direction = "right"
            self.player_state = "walk"
            self.rect.x = self.x
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.player_state = "jump"
            self.player_action = "jump"
        if keys[pygame.K_DOWN] and self.on_ground:
            # 下蹲时不可以跳跃
            self.jump_power = 0
            width = self.width + 20
            height = self.height - 30
            self.player_state = "crouch"
            self.player_action = "crouch"
            self.player_image = Role().role_1((width, height))
            self.rect = self.player_image.get_rect(topleft=(self.x, self.y))
        if not keys[pygame.K_DOWN] and self.on_ground:
            # 恢复跳跃
            self.jump_power = -12
            self.player_state = "walk"
            self.player_action = "walk"
            self.player_image = Role().role_1((self.width, self.height))
            self.rect = self.player_image.get_rect(topleft=(self.x, self.y))
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player_state = "idle"
        # 规定玩家边界
        if self.x < -20:
            self.x = -20
        if self.x > 520:
            self.x = 520
        if self.y > 430:
            self.player_hurt(screen,"跌落",35)
        if self.y < 0:
            self.y = 0
        return

    # 玩家重置位置
    def reset_player_pos(self):
        self.x = -20
        self.y = 230
        self.rect.x = self.x  # 更新矩形位置
        self.rect.y = self.y
        self.player_direction = "right"
        self.player_state = "idle"
        self.player_action = "idle"

    # 玩家更新碰撞
    def update_collision(self, platforms):
        self.vel_y += self.gravity
        self.y += self.vel_y
        self.rect.y = self.y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom >= platform.rect.top and self.rect.bottom <= platform.rect.top + 10:
                    self.y = platform.rect.top - self.rect.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.rect.y = self.y
                elif self.vel_y < 0 and self.rect.top <= platform.rect.bottom and self.rect.top >= platform.rect.bottom - 10:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                    self.rect.y = self.y
                elif self.rect.right >= platform.rect.left and self.rect.right <= platform.rect.left + 10:
                    self.x = platform.rect.left - self.rect.width
                    self.rect.x = self.x
                elif self.rect.left <= platform.rect.right and self.rect.left >= platform.rect.right - 10:
                    self.x = platform.rect.right
                    self.rect.x = self.x
                elif self.rect.bottom >= platform.rect.top and self.rect.top <= platform.rect.bottom:
                    self.on_ground = True
                    self.y = platform.rect.top - self.rect.height
                    self.vel_y = 0
                    self.rect.y = self.y
        return

    # 玩家绘制
    def draw(self, screen):
        if self.player_direction == "right":
            screen.blit(self.player_image, (self.x, self.y))
        elif self.player_direction == "left":
            screen.blit(pygame.transform.flip(self.player_image, True, False), (self.x, self.y))
        return

    # 玩家扣血
    def player_hurt(self, screen,type="跌落",damage=1):
        if type == "跌落":
            # 重置玩家位置
            self.reset_player_pos()
        self.player_hp -= damage
        # 受伤音效
        pygame.mixer.music.load("./static/hurt.mp3")
        pygame.mixer.music.play()
        # 扣血动画
        for i in range(10):
            self.player_image.set_alpha(128)
            self.draw(screen)
            pygame.display.flip()
        # 恢复透明度
        self.player_image.set_alpha(255)
        self.draw(screen)
        pygame.display.flip()
        if self.player_hp <= 0:
            self.player_death(screen)
        return

    # 玩家死亡
    def player_death(self, screen):
        # 玩家死亡
        self.player_hp = 0
        # 渲染玩家面板
        self.player_info(screen)
        # 主视图加灰色半透明蒙层
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明
        screen.blit(overlay, (0, 0))
        # 显示死亡信息
        drawText(screen, "你已死亡!", 200, 50, 30, (255, 0, 0))
        # 等待用户输入
        waitPlayerInput(screen, "按'F'键回到主界面...", pygame.K_f)
        # 播放死亡音效
        pygame.mixer.music.load("./static/death.mp3")
        pygame.mixer.music.play()
        # 保存关卡进度
        self.save_level_progress()
        # 回到主界面
        manager = Manager()
        manager.main()
        return

    def save_level_progress(self):
        # 保存关卡进度
        info = {
            # 玩家速度
            "player_speed" : self.player_speed,
            # 玩家等级
            "player_level" : self.player_level,
            # 玩家经验
            "player_exp" : self.player_exp,
            # 玩家生命值
            "player_hp" : self.player_hp,
            # 玩家攻击力
            "player_attack" : self.player_attack,
            # 每次升级需要经验
            "player_exp_needed" : self.player_exp_needed,
            # 当前关卡
            "current_level" : self.current_level
        }
        with open(progress_file_path, "r+") as f:
            f.truncate(0)  # 清空文件内容
            f.write(str(json.dumps(info)))
        return

# 敌人类
class Enemy(object):
    def __init__(self, x, y, direction="left", type=0, level=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = None
        self.rect = None
        # 宽度
        self.width = 0
        # 高度
        self.height = 0
        # 速度
        self.speed = 0
        # 速度copy 用来恢复速度
        self.speed_copy = 0
        # 生命
        self.hp = 0
        # 攻击力
        self.enemy_attack = 0
        # 攻击频率
        self.attack_frequency = 0
        # 攻击距离
        self.attack_distance = 0
        # 攻击方向
        self.attack_direction = "left"
        # 攻击类型
        self.attack_type = ""
        # 攻击音效
        self.attack_sound = None
        # 上次攻击时间
        self.last_attack_time = 0
        # 移动最大距离
        self.move_distance = 0
        # 已经移动距离
        self.moved_distance_total = 0
        # 死亡掉落经验
        self.exp = 0
        # 远程攻击对象
        self.remote_attack_obj = None
        # 行走图片
        self.walking_images = []
        # 攻击图片
        self.attack_images = []
        # 是否已死亡
        self.is_dead = False
        # 是否正在攻击
        self.is_attacking = False          
        # 攻击动画帧
        self.attack_frame= 0
        # 当前攻击动画帧
        self.current_attack_frame = 0      
        # 每帧动画间隔（毫秒）
        self.attack_animation_speed = 50
        # 上次动画更新时间
        self.last_attack_frame_time = 0    
        # 新增动画控制属性
        self.current_walk_frame = 0
        # 上次更新时间
        self.last_walk_frame_time = 0
        # 行走动画速度（毫秒每帧）
        self.walk_animation_speed = 100  # 毫秒每帧
        # 根据类型初始化敌人特征
        self.init_enemy(type, level)

    def init_enemy(self, type=0, level=1):
        # 随机生成敌人类型
        if type == 0:
            enemy_type = random.randint(1, 3)
        else:
            enemy_type = type
        if enemy_type == 1:
            # 近战小兵
            self.width = 80
            self.height = 80
            self.speed = 3
            self.speed_copy = 3
            self.hp = int(20 + 10 * level * 0.35)
            self.enemy_attack = int(10 + 10 * level * 0.15)
            self.attack_frequency = 3
            self.attack_distance = 10
            self.attack_type = "近战"
            self.move_distance = random.randint(150, 200)
            self.attack_sound = pygame.mixer.Sound("./static/enemy/1/attack.ogg")
            self.exp = int(10 + 10 * level * 0.2)
            self.attack_images = [pygame.transform.scale(pygame.image.load("./static/enemy/1/attacking_"+str(i)+".png").convert_alpha(), (self.width, self.height)) for i in range(1, 9)]
            self.walking_images = [pygame.transform.scale(pygame.image.load("./static/enemy/1/walking_"+str(i)+".png").convert_alpha(), (self.width, self.height)) for i in range(1, 10)]
            self.attack_frame = 5
            self.update_image(self.walking_images[-1])
        if enemy_type == 2:
            # 远程小兵
            pass
        if enemy_type == 3:
            # 复合攻击小兵
            pass
        return        

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update_image(self,image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def attack(self, screen, playerObj):
        # 限制攻击频率
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_attack_time) < self.attack_frequency * 1000:
            return
        if self.attack_type == "近战":
            # 修正攻击区域
            attack_hitbox = pygame.Rect(
                self.x - self.attack_distance if self.direction == "left" else self.x + self.width,
                self.y,
                self.attack_distance,
                self.height
            )
            # 调试绘制攻击区域
            # pygame.draw.rect(screen, (255,0,0), attack_hitbox, 1)
            # 检测玩家是否在攻击范围内
            if attack_hitbox.colliderect(playerObj.rect) or self.is_attacking:
                # 如果未在攻击状态，初始化攻击
                if not self.is_attacking:
                    self.speed = 0  # 停止移动
                    # 时间停顿 模拟攻击前摇
                    pygame.time.delay(100)
                    self.is_attacking = True
                    self.current_attack_frame = 0
                    self.last_attack_frame_time = current_time
                    self.attack_sound.play()
                # 更新攻击动画帧
                if current_time - self.last_attack_frame_time > self.attack_animation_speed:
                    self.current_attack_frame += 1
                    self.last_attack_frame_time = current_time
                    # 播放到最后一帧时结束攻击
                    if self.current_attack_frame >= len(self.attack_images):
                        self.is_attacking = False
                        self.last_attack_time = current_time  # 记录攻击冷却
                        self.speed = self.speed_copy  # 恢复移动速度
                        return
                # 绘制当前攻击帧
                current_image = self.attack_images[self.current_attack_frame]
                if self.direction == "left":
                    current_image = pygame.transform.flip(current_image, True, False)
                screen.blit(current_image, (self.x, self.y))
                self.update_image(current_image)
                # 检测是否击中玩家
                if (self.current_attack_frame-1) == self.attack_frame and attack_hitbox.colliderect(playerObj.rect):
                    playerObj.player_hurt(screen,"攻击", self.enemy_attack)
        return

    def move(self, screen, platforms):
        # 移动
        if self.direction == "left":
            self.x -= self.speed
            self.moved_distance_total += self.speed
        elif self.direction == "right":
            self.x += self.speed
            self.moved_distance_total += self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        # 更新时间驱动的行走动画帧
        current_time = pygame.time.get_ticks()
        if current_time - self.last_walk_frame_time > self.walk_animation_speed:
            self.current_walk_frame = (self.current_walk_frame + 1) % len(self.walking_images)
            self.last_walk_frame_time = current_time
        # 使用当前帧更新图像
        current_image = self.walking_images[self.current_walk_frame]
        if self.direction == "left":
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (self.x, self.y))
        self.update_image(current_image)
        # 检测是否与平台发生碰撞
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # 改变方向
                if self.direction == "left":
                    self.direction = "right"
                elif self.direction == "right":
                    self.direction = "left"
                # 重置移动距离
                self.moved_distance_total = 0
                # 重置移动最大距离
                self.move_distance = random.randint(50, 150)
                break
        # 判断是否到达屏幕边界或移动距离是否超过最大距离
        if (self.x <= 0 or self.x >= window_width - self.width) or (self.moved_distance_total >= self.move_distance):
            # 改变方向
            if self.direction == "left":
                self.direction = "right"
            elif self.direction == "right":
                self.direction = "left"
            # 重置移动距离
            self.moved_distance_total = 0
            # 重置移动最大距离
            self.move_distance = random.randint(50, 150)
        return
    
    def enemy_hurt(self, screen, damage):
        # 扣血
        self.hp -= damage
        # 扣血动画
        for _ in range(10):
            self.image.set_alpha(128)
            self.draw(screen)
        # 恢复透明度
        self.image.set_alpha(255)
        self.draw(screen)
        if self.hp <= 0:
            # 死亡
            self.enemy_death(screen)
        return
    
    def enemy_death(self, screen):
        # 清除敌人
        self.image.set_alpha(0)
        self.draw(screen)
        # 死亡音效
        pygame.mixer.Sound("./static/death.mp3").play()
        self.is_dead = True
        return

# 火球攻击类
class Fireball(object):
    def __init__(self, x, y, direction="right", player_attack=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load("./static/fireball/bullet.png").convert_alpha(), (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        # 速度
        self.speed = 10
        # 伤害
        self.damage = int(0.45 * player_attack)
        # 攻击最大距离
        self.attack_distance = 350
        # 已经攻击距离
        self.attacked_distance_total = 0
        # 攻击范围
        self.attack_range = 35
        # 是否存活
        self.is_alive = True
        # 攻击音效
        pygame.mixer.Sound("./static/fireball/attack.ogg").play()
        
    def draw(self, screen):
        if self.direction == "left":
            screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
    
    def update(self,screen,platforms, enemys, playObject):
        if self.direction == "right":
            self.x += self.speed
            self.attacked_distance_total += self.speed
        elif self.direction == "left":
            self.x -= self.speed
            self.attacked_distance_total += self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        if self.attacked_distance_total >= self.attack_distance:
            # 爆炸
            self.explosion(screen)
        # 检测是否与平台发生碰撞
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # 爆炸
                self.explosion(screen)
        # 检测火球是否碰撞到敌人
        for enemy in enemys:
            if self.rect.colliderect(enemy.rect):
                # 爆炸
                self.explosion(screen)
                # 检测爆炸是否碰撞到敌人
                if self.rect.colliderect(enemy.rect):
                    # 敌人受伤
                    enemy.enemy_hurt(screen, self.damage)
                    if enemy.is_dead:
                        # 玩家获得经验
                        playObject.player_exp += enemy.exp
        return
        
    def explosion(self,screen):
        # 清除火球
        self.image.set_alpha(0)
        self.draw(screen)
        # 爆炸音效
        pygame.mixer.Sound("./static/fireball/bomb.wav").play()
        # 绘制爆炸动画
        for i in range(1,15):
            # 爆炸动画
            self.image = pygame.transform.scale(pygame.image.load("./static/fireball/"+str(i)+".png").convert_alpha(), (self.attack_range, self.attack_range))
            self.image.set_alpha(128)
            screen.blit(self.image, (self.x, self.y))
            # 清除爆炸动画
            self.image.set_alpha(0)
            screen.blit(self.image, (self.x, self.y))
        self.is_alive = False
        return

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


class Role(object):

    def role_1(self, size=(80, 80)):
        # 玩家图片
        player_image = pygame.image.load("./static/role_1.gif").convert_alpha()
        player_image = pygame.transform.scale(player_image, size)
        return player_image

    def npc_1(self, size=(80, 80)):
        # npc角色图片
        npc_image = pygame.image.load("./static/npc_1.gif").convert_alpha()
        npc_image = pygame.transform.scale(npc_image, size)
        return npc_image


class GameText(object):
    def level_1(self):
        text = "剧情摘要\n你是一名生物学家名字为弗兰克,\n由于你曝光了一所名为天网生物\n实验室研究的一项邪恶研究导致\n你的女友爱丽丝被天网组织抓走了\n你发誓一定要救回你的女友！\n\n\n按下S键继续..."
        return text

    def level_2(self):
        text = "经过几个市区后你来到了13区,\n街上似乎一个人都没有安静的\n有些可怕,等等那是什么？\n不远处的一个黑影引起了你的注意。\n你觉得过去看看...\n\n\n按下S键继续..."
        return text


if __name__ == '__main__':
    manager = Manager()
    manager.main()

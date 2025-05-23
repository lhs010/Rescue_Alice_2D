import pygame
import player
import media
import tools
import enemy as Enemy

# 关卡类
class GameLevel(object):

    def __init__(self):
        # 初始化玩家对象
        self.playerObj = player.Player()
        # 加载进度
        self.playerObj.load_progress()
        import main
        self.window_width = main.window_width
        self.window_height = main.window_height

        
    def platform_1_image(self):
        bgi = pygame.image.load("./static/platform_1.png").convert_alpha()
        return bgi

    def platform_2_image(self):
        bgi = pygame.image.load("./static/platform_2.png").convert_alpha()
        return bgi
    
    def pass_level(self,screen):
        # 播放通关音效
        media.Music().pass_level()
        # 显示下一关入口
        image = pygame.image.load("./static/y.png")
        image = pygame.transform.scale(image, (80, 80))
        screen.blit(image, (430, 220))
        tools.drawText(screen, "向前进入下一关", 380, 180, 20)
        if self.playerObj.x >= 520:
            # 保存关卡进度
            self.playerObj.current_level += 1
            self.playerObj.save_level_progress()
            return True
        return False

    def level_1(self, screen):
        if self.playerObj.current_level != 1:
            return
        clock = pygame.time.Clock()
        # 绘制背景# 绘制剧情音乐
        media.Music().plot()
        # 绘制剧情背景
        media.GameBackground().level_1_plot(screen)
        # 游戏文字
        text = GameText().level_1()
        # 绘制剧情摘要
        tools.drawTextCenter(screen, text, 20, (255, 255, 255))
        # 等待用户输入
        tools.waitPlayerInput(screen, "", pygame.K_s)
        # 绘制关卡音乐
        media.Music().level()
        # 绘制NPC
        npc_image = player.Role().npc_1()
        # 是否与npc互动
        is_npc_interactive = False
        # 重置玩家位置
        self.playerObj.reset_player_pos()
        # npc位置
        npc_x = self.window_width
        npc_y = 310
        # 初始化游戏平台
        platforms = [
            media.Platform(0, 380, self.window_width, 20, self.platform_1_image())
        ]
        # 绘制敌人
        enemies = [
            Enemy.Enemy(450, 300, "left", 1, 1),
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
                    if event.key == pygame.K_SPACE and self.playerObj.on_ground:
                        self.playerObj.vel_y = self.playerObj.jump_power
                    elif event.key == pygame.K_a:
                        self.playerObj.attack()
            # 绘制背景
            media.GameBackground().level_1(screen)
            # 绘制平台
            for platform in platforms:
                platform.draw(screen)
            # 玩家移动
            self.playerObj.player_move(screen)
            # 更新玩家碰撞
            self.playerObj.update_collision(platforms)
            # 绘制玩家面板
            self.playerObj.player_info(screen)
            # 绘制玩家
            self.playerObj.draw(screen)
            # 绘制敌人
            for enemy in enemies:
                if enemy.is_dead:
                    enemies.remove(enemy)
                    continue
                else:
                    enemy.attack(screen, self.playerObj)  # 非阻塞逐帧更新动画
                    if enemy.speed != 0:
                        enemy.move(screen, platforms)
            # 绘制玩家攻击
            for target in self.playerObj.remote_attack_targets:
                if target.is_alive:
                    target.draw(screen)
                    target.update(screen, platforms,enemies,self.playerObj)
                else:
                    self.playerObj.remote_attack_targets.remove(target)
            # 玩家升级检测
            self.playerObj.player_level_up(screen)
            if is_npc_interactive:
                game_over = self.pass_level(screen)
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
                    if npc_rect.colliderect(self.playerObj.rect):
                        pygame.image.save(screen, "./static/temp.jpg")
                        # 绘制交互提示
                        tools.drawText(screen, "按'F'键与NPC互动", 200, 150, 20, (255, 255, 255))
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_f]:
                            is_npc_interactive = True
                            sbgi = pygame.image.load("./static/temp.jpg")
                            sbgi = pygame.transform.scale(sbgi, (self.window_width, self.window_height))
                            screen.blit(sbgi, (0, 0))
                            # 主视图加灰色半透明蒙层
                            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
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
                            player_big_image = pygame.transform.scale(self.playerObj.player_image, (300, 300))
                            for text in text_list:
                                # 清空事件队列
                                pygame.event.clear()
                                if text[0] == "player":
                                    screen.blit(player_big_image, (-100, 50))
                                else:
                                    screen.blit(pygame.transform.flip(npc_big_image, True, False), (330, 100))
                                tools.drawText(screen, text[1], 150, 200, 15, (255, 255, 255))
                                # 等待用户按下任意键
                                tools.waitPlayerInput(screen, "按'F'键继续...", pygame.K_f)
                                # 渲染快照背景图，用于清除本次交互内容
                                sbgi = pygame.image.load("./static/temp.jpg")
                                sbgi = pygame.transform.scale(sbgi, (self.window_width, self.window_height))
                                screen.blit(sbgi, (0, 0))
                            # 玩家获得经验
                            self.playerObj.player_exp += 100
            # 更新显示
            pygame.display.flip()
            # 控制帧率
            clock.tick(60)
        return

    def level_2(self, screen):
        pass    


# 文案类
class GameText(object):
    def level_1(self):
        text = "剧情摘要\n你是一名生物学家名字为弗兰克,\n由于你曝光了一所名为天网生物\n实验室研究的一项邪恶研究导致\n你的女友爱丽丝被天网组织抓走了\n你发誓一定要救回你的女友！\n\n\n按下S键继续..."
        return text

    def level_2(self):
        text = "经过几个市区后你来到了13区,\n街上似乎一个人都没有安静的\n有些可怕,等等那是什么？\n不远处的一个黑影引起了你的注意。\n你觉得过去看看...\n\n\n按下S键继续..."
        return text


import pygame
import tools
import json


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
        tools.drawText(screen, "等级: " + str(self.player_level), 10, 10, 10, (255, 255, 255))
        tools.drawText(screen, "经验: " + str(self.player_exp) + "/" + str(self.player_exp_needed), 10, 20, 10, (255, 255, 255))
        tools.drawText(screen, "血量: " + str(int(self.player_hp)), 10, 30, 10, (255, 255, 255))
        tools.drawText(screen, "攻击力: " + str(int(self.player_attack)), 10, 40, 10, (255, 255, 255))
        tools.drawText(screen, "位置: [" + str(self.x) + "," + str(self.y) + "]", 10, 50, 10, (255, 255, 255))

    # 玩家升级
    def player_level_up(self, screen):
        import main
        window_width,window_height = main.window_width,main.window_height
        # 玩家升级检测
        if self.player_exp >= self.player_exp_needed:
            # 主视图加灰色半透明蒙层
            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 半透明
            screen.blit(overlay, (0, 0))
            # 显示升级信息
            tools.drawText(screen, "等级提升!", 200, 50, 30, (255, 255, 0))
            tools.drawText(screen, "等级: " + str(self.player_level) + " -> " + str(self.player_level + 1), 200, 90, 20, (0, 255, 255))
            tools.drawText(screen, "血量: " + str(int(self.player_hp)) + " -> " + str(self.player_hp + int(self.player_hp * self.player_level * 0.05)), 200, 110, 20, (0, 255, 255))
            tools.drawText(screen, "攻击力: " + str(int(self.player_attack)) + " -> " + str(self.player_attack + int(self.player_attack * self.player_level * 0.2)), 200, 130, 20, (0, 255, 255))
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
            tools.waitPlayerInput(screen, "按'F'键继续...", pygame.K_f)
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
        import main
        window_width,window_height = main.window_width,main.window_height
        # 玩家死亡
        self.player_hp = 0
        # 渲染玩家面板
        self.player_info(screen)
        # 主视图加灰色半透明蒙层
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明
        screen.blit(overlay, (0, 0))
        # 显示死亡信息
        tools.drawText(screen, "你已死亡!", 200, 50, 30, (255, 0, 0))
        # 等待用户输入
        tools.waitPlayerInput(screen, "按'F'键回到主界面...", pygame.K_f)
        # 播放死亡音效
        pygame.mixer.music.load("./static/death.mp3")
        pygame.mixer.music.play()
        # 保存关卡进度
        self.save_level_progress()
        # 回到主界面
        manager = main.Manager()
        manager.main()
        return

    def save_level_progress(self):
        import main
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
        with open(main.progress_file_path, "r+") as f:
            f.truncate(0)  # 清空文件内容
            f.write(str(json.dumps(info)))
        return

    def load_progress(self):
        import main
        # 读取进度信息
        progress_info_json = ""
        with open(main.progress_file_path, "r") as f:
            progress_info_json = f.read()
        if progress_info_json == "":
            return
        # 载入进度信息
        progress_info = json.loads(progress_info_json)
        # 玩家速度
        self.player_speed = progress_info["player_speed"]
        # 玩家等级
        self.player_level = progress_info["player_level"]
        # 玩家经验
        self.player_exp = progress_info["player_exp"]
        # 玩家生命值
        self.player_hp = progress_info["player_hp"]
        # 玩家攻击力
        self.player_attack = progress_info["player_attack"]
        # 每次升级需要经验
        self.player_exp_needed = progress_info["player_exp_needed"]
        # 当前关卡
        self.current_level = progress_info["current_level"]
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

# 角色类
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

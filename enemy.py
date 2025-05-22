import pygame
import random
import media

# 敌人类
class Enemy(object):
    def __init__(self, x, y, direction="left", type=0, level=1):
        self.x = x
        self.y = y + 1
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
            self.speed = 1.7
            self.speed_copy = 1.7
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
        import main

        # 移动敌人
        self.x = self.x - self.speed if self.direction == "left" else self.x + self.speed
        self.moved_distance_total += self.speed
    
        # 检测是否站在平台上（精确检测底部接触）
        on_platform = False
        for platform in platforms:
            if self.direction == "left":
                if (self.rect.colliderect(platform.rect)) and platform.rect.topleft[0] <=  self.rect.bottomleft[0]:
                    on_platform = True
                    break
            elif self.direction == "right":
                if (self.rect.colliderect(platform.rect)) and platform.rect.topright[0] >= self.rect.bottomright[0]:
                    on_platform = True
                    break
        # 如果不在平台上，回退并转向
        if not on_platform:
            self.direction = "right" if self.direction == "left" else "left"
            # 移动敌人
            self.x = self.x - self.speed if self.direction == "left" else self.x + self.speed
            self.moved_distance_total = self.speed
            
        # 更新行走动画帧
        current_time = pygame.time.get_ticks()
        if current_time - self.last_walk_frame_time > self.walk_animation_speed:
            self.current_walk_frame = (self.current_walk_frame + 1) % len(self.walking_images)
            self.last_walk_frame_time = current_time

        # 绘制当前帧
        current_image = self.walking_images[self.current_walk_frame]
        if self.direction == "left":
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (self.x, self.y))
        self.update_image(current_image)
        
        # 屏幕边界或移动距离检测
        if (self.x <= 0 or self.x >= main.window_width - self.width) or (self.moved_distance_total >= self.move_distance):
            self.direction = "right" if self.direction == "left" else "left"
            self.moved_distance_total = 0
        return
    
    def enemy_hurt(self, screen, damage):
        # 扣血
        self.hp -= damage
        # 播放受伤音效
        media.Music().hurt()
        if self.hp <= 0:
            # 死亡
            self.enemy_death(screen)
        return
    
    def enemy_death(self, screen):
        # 清除敌人
        self.image.set_alpha(0)
        self.draw(screen)
        # 死亡音效
        media.Music().death()
        self.is_dead = True
        return


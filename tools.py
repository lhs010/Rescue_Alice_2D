import pygame
import random
import sys

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
    type_sound = pygame.mixer.Sound("./static/music/typewriter.mp3")
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

import pygame
import cv2

class PyGameDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pygame Video Display")
        self.window_width, self.window_height = 1280, 720

    def update_display(self, frame):
        if frame is not None:
            # 计算视频的原始宽高比
            original_height, original_width = frame.shape[:2]
            aspect_ratio = original_width / original_height
            
            # 计算视频在窗口上半部分的高度
            target_height = self.window_height // 2
            
            # 根据宽高比计算目标宽度
            target_width = int(target_height * aspect_ratio)
            
            # 调整视频大小，保持宽高比
            frame_resized = cv2.resize(frame, (target_width, target_height))
            
            # 将视频转换为RGB格式并转换为Pygame的Surface对象
            frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB).swapaxes(0, 1))
            
            # 计算视频在窗口上半部分的居中位置
            x_offset = (self.window_width - target_width) // 2
            
            # 将视频绘制到窗口的上半部分并更新显示
            self.screen.blit(frame_surface, (x_offset, 0))
            pygame.display.flip()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        width = max(self.rect.w, txt_surface.get_width() + 10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
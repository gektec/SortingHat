import pygame
import cv2

class PyGameDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Pygame Video Display")

    def update_display(self, frame):
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.screen.blit(frame, (0, 0))
            pygame.display.flip()

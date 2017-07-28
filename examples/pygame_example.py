import sys
sys.path.append("..")
import ecs


FPS = 60
WIDTH = 640
HEIGHT = 480


class Velocity:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Renderable:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()


class ProcessMovement(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

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
        # This goes through ever Entity that has
        # the Velocity and Renderable Component
        for entity, (velocity, renderable) in self.Manager.get_components(
                Velocity, Renderable):
            # Updates the coordinates of Renderable
            renderable.x += velocity.x
            renderable.y += velocity.y
            # This is to keep the Renderable in screen
            renderable.x = max(0, renderable.x)
            renderable.y = max(0, renderable.y)
            renderable.x = min(WIDTH - renderable.width, renderable.x)
            renderable.y = min(HEIGHT - renderable.height, renderable.y)

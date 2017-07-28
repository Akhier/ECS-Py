import sys
sys.path.append("..")
import ecs


FPS = 60
WIDTH = 640
HEIGHT = 480


class Coordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class ProcessMovement(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (coordinate, velocity) in self.Manager.get_components(
                Coordinate, Velocity):
            coordinate.x += velocity.x
            coordinate.y += velocity.y
            print("Current Location: {}".format((coordinate.x, coordinate.y)))

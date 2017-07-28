import sys
sys.path.append("..")
import ecs
import pygame


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
        # The Velocity and Renderable Component
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


class Render(ecs.SystemTemplate):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window
        self.window.fill(self.clear_color)
        # Iterate though all Entities with Renderable
        for entity, renderable in self.Manager.get_component(Renderable):
            self.window.blit(renderable.image, (renderable.x, renderable.y))
        # Flip the framebuffers
        pygame.display.flip()


def run():
    # Initialize Pygame
    pygame.init()
    window = pygame.display.set_mode(WIDTH, HEIGHT)
    pygame.display.set_caption("Dragonheart ECS Pygame example")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)
    # Create the manager the Entity "green" with Components
    manager = ecs.Manager()
    green = manager.new_entity(Velocity())
    manager.add_component_to_entity(Renderable(
        image=pygame.image.load("green_square.png")), green)
    # Create Systems and add them to the manager
    processmovement = ProcessMovement()
    manager.add_system(processmovement)
    render = Render(window)
    manager.add_system(render)

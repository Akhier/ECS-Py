import ecs
import time


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


def main():
    # Creates the Manager
    manager = ecs.Manager()

    # Instantiates the ProcessMovement System and adds it to manager
    processmovement = ProcessMovement()
    manager.add_system(processmovement)

    # Create an Entity with a Component then adds another Component
    entity = manager.new_entity(Coordinate(x=0, y=0))
    manager.add_component_to_entity(Velocity(x=1, y=2), entity)

    # Basic Main Loop
    try:
        while True:
            # Call manager.process() to run all the systems
            manager.process()
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    print("example - press ctrl+C to quit")
    main()

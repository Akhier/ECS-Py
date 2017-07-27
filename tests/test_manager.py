import ecs


def make_entities(manager, num):
    for _ in range(num // 2):
        unit_a = manager.make_entities()
        manager.add_component_to_entity(unit_a, compA())
        manager.add_component_to_entity(unit_a, compB())
        unit_b = manager.make_entities()
        manager.add_component_to_entity(unit_b, compB())
        manager.add_component_to_entity(unit_b, compC())

class compA:
    def __init__(self):
        self.a = -1
        self.b = 1

class compB:
    def __init__(self):
        self.t = True
        self.f = False

class compC:
    def __init__(self):
        self.l = 'left'
        self.r = 'right'

class sysA(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class sysB(ecs.SystemTemplate)
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class sysC(ecs.SystemTemplate)
    def __init__(self):
        super().__init__()

    def process(self):
        pass

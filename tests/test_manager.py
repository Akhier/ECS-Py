import sys
sys.path.append("..")
import ecs
import pytest


@pytest.fixture
def manager():
    return ecs.Manager()

@pytest.fixture
def get_populated_manager():
    populated_manager = ecs.Manager()
    make_entities(populated_manager, 1000)
    return populated_manager

def test_manager_creation(manager):
    assert type(manager) == ecs.Manager
    assert type(manager._next_entity_id) == int
    assert type(manager._entities) == dict
    assert type(manager._components) == dict
    assert type(manager._systems) == list

def test_new_entity(manager):
    entityA = manager.new_entity()
    entityB = manager.new_entity()
    assert type(entityA) and type(entityB) == int
    assert entityA < entityB

###############################
# Helper Function and Classes #
###############################

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

class sysB(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

class sysC(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()

    def process(self):
        pass

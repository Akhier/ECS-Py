import sys
sys.path.append("..")
import ecs
import pytest
import types


@pytest.fixture
def manager():
    return ecs.Manager()


@pytest.fixture
def populated_manager():
    new_populated_manager = ecs.Manager()
    make_entities(new_populated_manager, 1000)
    return new_populated_manager


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


def test_new_entity_with_components(manager):
    entityA = manager.new_entity(compA())
    entityB = manager.new_entity(compB(), compC())
    assert manager.has_component(entityA, compA) is True
    assert manager.has_component(entityA, compB) is False
    assert manager.has_component(entityB, compA) is False
    assert manager.has_component(entityB, compB) is True
    assert manager.has_component(entityB, compC) is True


def test_remove_entity_with_immediate_true(manager):
    entityA = manager.new_entity(compA)
    entityB = manager.new_entity()
    assert entityB == 2
    manager.remove_entity(entityA, immediate=True)
    manager.remove_entity(entityB, immediate=True)
    with pytest.raises(KeyError):
        manager.get_all_components_from_entity(entityA)
        manager.get_all_components_from_entity(entityB)
        manager.remove_entity(999, immediate=True)


def test_remove_entity_default(manager):
    entityA = manager.new_entity(compA)
    entityB = manager.new_entity()
    assert entityB == 2
    manager.remove_entity(entityA)
    manager.remove_entity(entityB)
    assert manager.has_component(entityA, compA) is False
    manager.add_component_to_entity(compA(), entityB)
    assert manager.has_component(entityB, compA) is True
    manager.process()
    with pytest.raises(KeyError):
        manager.get_all_components_from_entity(entityA)
        manager.get_all_components_from_entity(entityB)


def test_get_component_from_entity(manager):
    entityA = manager.new_entity(compA())
    assert isinstance(manager.get_component_from_entity(compA, entityA), compA)
    with pytest.raises(KeyError):
        manager.get_component_from_entity(entityA, compB)


def test_get_all_components_from_entity(manager):
    compa = compA()
    entityA = manager.new_entity(compa, compB(), compC())
    all_components = manager.get_all_components_from_entity(entityA)
    assert type(all_components) == tuple
    assert len(all_components) == 3
    assert compa in all_components
    with pytest.raises(KeyError):
        manager.get_all_components_from_entity(999)


def test_has_component(manager):
    entityA = manager.new_entity(compA())
    assert manager.has_component(entityA, compA) is True
    assert manager.has_component(entityA, compB) is False


def test_get_component(populated_manager):
    assert isinstance(populated_manager.get_component(
        compA), types.GeneratorType)
    for entity, component in populated_manager.get_component(compA):
        assert type(entity) == int
        assert type(component) == compA


def test_get_components(populated_manager):
    assert isinstance(populated_manager.get_components(
        compA, compB), types.GeneratorType)
    for entity, components in populated_manager.get_components(compA, compB):
        assert type(entity) == int
        assert type(components) == list
        assert len(components) == 2
    for entity, (a, b) in populated_manager.get_components(compA, compB):
        assert type(a) == compA
        assert type(b) == compB


def test_clear_database(populated_manager):
    populated_manager.clear_database()
    assert len(populated_manager._entities) == 0
    assert len(populated_manager._components) == 0
    assert len(populated_manager._systems) == 0
    assert populated_manager._next_entity_id == 0


def test_add_system(populated_manager):
    assert len(populated_manager._systems) == 0
    systemA = sysA()
    assert isinstance(systemA, ecs.SystemTemplate)
    populated_manager.add_system(systemA)
    assert len(populated_manager._systems) == 1
    assert isinstance(populated_manager._systems[0], ecs.SystemTemplate)


def test_remove_system(populated_manager):
    systemA = sysA()
    populated_manager.add_system(systemA)
    populated_manager.remove_system(sysB)
    assert len(populated_manager._systems) == 1
    populated_manager.remove_system(sysA)
    assert len(populated_manager._systems) == 0


###############################
# Helper Function and Classes #
###############################


def make_entities(manager, num):
    for _ in range(num // 2):
        unit_a = manager.new_entity()
        manager.add_component_to_entity(unit_a, compA())
        manager.add_component_to_entity(unit_a, compB())
        unit_b = manager.new_entity()
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
        self.L = 'left'
        self.R = 'right'


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

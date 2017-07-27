import ecs


class Manager:
    def __init__(self):
        """A Manager keeps track of all Entities, Components, and Systems

        A Manager contains the 'database'  for all entity/component connections
        as well as call the process function for Systems that are
        assigned to it.
        """
        self._systems = []
        self._next_entity_id = 0
        self._components = {}
        self._entities = {}
        self._dead_entities = set()

    def clear_database(self):
        """Clears all Components and Entities from the Manager

        Also resets the entity id count
        """
        self._components.clear()
        self._entities.clear()
        self._dead_entities.clear()
        self._next_entity_id = 0

    def add_system(self, system_instance):
        """Add a System instance to the Manager

        :param system_instance: An instance of a System that
        is a subclass of SystemTemplate
        """
        assert issubclass(system_instance.__class__, ecs.SystemTemplate)
        system_instance.Manager = self
        self._systems.append(system_instance)

    def remove_system(self, system_type):
        """Removes a System type from the Manager

        :param system_type: The System class type to be removed
        """
        for system in self._systems:
            if type(system) == system_type:
                system.Manager = None
                self._systems.remove(system)

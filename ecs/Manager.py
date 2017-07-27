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

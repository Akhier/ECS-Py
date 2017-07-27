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
        """Removes a System class type from the Manager

        :param system_type: The System class type to be removed
        """
        for system in self._systems:
            if type(system) == system_type:
                system.Manager = None
                self._systems.remove(system)

    def new_entity(self, *components):
        """Creates an Entity

        :param components: Optional components to add to the new Entity
        :return: The ID of the new Entity
        """
        self._next_entity_id += 1
        for component in components:
            self.add_component(self._next_entity_id, component)
        return self._next_entity_id

    def remove_entity(self, entity, immediate=False):
        """Removes an Entity from the Manager

        By default this method only adds the entity to the list of dead
        Entities which is taken care of when Manager.process gets called.
        If immediate however is set to true it will remove the entity
        at that time.

        Raises a KeyError if the entity is not in the database
        :param entity: ID of the entity to delete
        :param immediate: When True entity is removed immediatly
        """
        if immediate:
            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)
                if not self._components[component_type]:
                    del self._components[component_type]
            del self._entities[entity]
        else:
            self._dead_entities.add(entity)

    def get_component_from_entity(self, component_type, entity):
        """Get component instance of specified type from given entity

        Raises KeyError if either Entity or Component type does not exist
        :param component_type: The class type of the Component you want to get
        :param entity: ID of the entity to get the component from
        :return: The component instance that was requested from given entity
        """
        return self._entities[entity][component_type]

    def get_all_components_from_entity(self, entity):
        """Get all components attached to given entity

        Meant to be used for saving the state or transfering
        an entity to another manager

        Raises KeyError if Entity does not exist
        :param entity: ID of the entity to get the components from
        """
        return tuple(self._entities[entity].values())

    def has_component(self, entity, component_type):
        """Check if an entity has a specific component type

        :param entity: ID of the entity to check
        :param component_type: The type of the component to check for
        :return: True if entity has a component of given type,
        else False
        """
        return component_type in self._entities[entity]

    def add_component_to_entity(self, component_instance, entity):
        """Add a component onto the given entity

        If the component to add already exists on the entity the old
        component will be replaced

        :param component_instance: A component instance
        :param entity: ID of the entity to add to
        """
        component_type = type(component_instance)
        if component_type not in self._components:
            self._components[component_type].set()
        self._components[component_type].add(entity)
        if entity not in self._entities:
            self._entities[entity] = {}
        self._entities[entity][component_type].add(component_instance)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![Build Status](https://travis-ci.org/Akhier/ECS-Py.svg?branch=master)](https://travis-ci.org/Akhier/ECS-Py)

# ECS-Py
---
ECS-Py is my implimentation of a basic Entity Component System (ECS).

#### Structure
---
 * **Manager**
 The Manager is were everything is stored and what does most of the work. Everything from creating new Entities and attaching components to them up to clearing all the data. This is were all the methods you will need to call to use ECS-Py will reside. One thing to note is you are not limited to only one Manager. You could for instance if making a dungeon exploring game have each dungeon level be held by it's own Manager.

 * **Entities**
 Following the purist route these are simply a number. You don't even really use them directly. All they are used for is to identify what belongs to what.

 * **Components**
 These are classes if only because I have coded some of the methods so they have to be. While I can't enfource it the purist way of using them is to have them only contain data. No actual code beyond declaring the variables needed should be happening here. I was actually tempted to use named tuples for this and might at some point change to that. Only my inexperiance with named tuples stopped me. An example of what this would look like:
```python
class Health:
    def __init__(self, maxhp):
        self.maxhp = maxhp
        self.currenthp = maxhp
```
 * **Systems**
 This is were all the action happens. If you made a game the HP would be a component while the System would be the one to modify it when you get hit. In ECS-Py the only restrictions is that your Systems have to be a classes that inherits from SystemTemplate. The reason for this is that the Manager processes you Systems by calling their process method and using a template like this makes sure you have one. An example of the HP modifing System could look like this:
```python
class LowerHealth(ecs.SystemTemplate):
    def __init__(self):
        super().__init__()
    def process(self):
        for entity, (health, damage) in self.manager.get_components(Health, Damage):
            health.currenthp += damage.amount
            self.manager.remove_component_from_entity(Damage, entity)
```
 #### Using it
 ---
 To use ECS-Py in your code you will just need to put the ecs folder in the root folder of your project. After that the first step is you need a Manager. This is simple enough
```python
manager = ecs.Manager()
```
Next we create some Systems and add them to our manager
```python
lowerhealth = LowerHealth()
manager.add_system(lowerhealth)
```
With a system in place we will next add an entity with a component. After that we will add another component to it
```python
entity = manager.new_entity(Health(10))
manager.add_compontent_to_entity(Damage(3), entity)
```
Finally we can process everything with the manager
```python
manager.process()
```
#### Examples
---
In the examples folder there is current two examples. The first runs with just the console while the second uses pygame and lets you move a green square around a screen.
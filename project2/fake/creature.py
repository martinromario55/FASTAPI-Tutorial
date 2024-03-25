from model.creature import Creature

_creatures = [
    Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman"
    ),
    Creature(
        name="Bigfoot",
        country="US",
        area="*",
        description="Yeti's Cousin Eddie",
        aka="Sasquatch"
    ),
]

def get_all() -> list[Creature]:
    '''Return all creatures'''
    return _creatures

def get_one(name: str) -> Creature | None:
    '''Return a creature by name'''
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None

def create(creature: Creature) -> Creature:
    '''Add a creature'''
    return creature

def modify(creature: Creature) -> Creature:
    '''Partially modify a creature'''
    return creature

def replace(creature: Creature) -> Creature:
    '''Completely replace a creature'''
    return creature

def delete(name: str) -> bool:
    '''Delete a creature; return None if it existed'''
    return None
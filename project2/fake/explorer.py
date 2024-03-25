from model.explorer import Explorer

# fake data
_explorers = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    ),
    Explorer(
        name="Noah Weiser",
        country="DE",
        description="Myopic machete man",
    ),
]

def get_all() -> list[Explorer]:
    '''Return all explorers'''
    return _explorers

def get_one(name: str) -> Explorer | None:
    '''Return an explorer by name'''
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None

def create(explorer: Explorer) -> Explorer:
    '''Add an Explorer'''
    return explorer

def modify(explorer: Explorer) -> Explorer:
    '''Partially modify an explorer'''
    return explorer

def replace(explorer: Explorer) -> Explorer:
    '''Completely replace an explorer'''
    return explorer

def delete(name: str) -> bool:
    '''Delete an explorer; return None if it existed'''
    return None
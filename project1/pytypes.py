from typing import Any, Union
from dataclasses import dataclass

# Variables
responses: dict[str, Any] = {"Marco": "Polo", "answer": 42}

responses2: dict[str, Union[str, int]] = {"Marco": "Polo", "answer": 42}

responses3: dict[str, str | int] = {
    "Marco": "Polo",
    "answer": 42,
}

# Classes
@dataclass
class CreatureDataClass():
    name: str
    country: str
    area: str
    description: str
    aka: str
    
dataclass_thing = CreatureDataClass(
    "yeti",
    "CN",
    "Himalayas",
    "Hirsute Himalayan",
    "Abominable Snowman"
)
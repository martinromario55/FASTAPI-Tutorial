from pydantic import BaseModel, constr

class Creature(BaseModel):
    name: constr(min_length=2)
    country: str
    area: str
    description: str
    aka: str
    
thing = Creature(
    name="i",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman"
)

print("Name is", thing.name)
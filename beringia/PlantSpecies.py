from .Plant import Plant
from .BeringiaUtilities import generate_id

import random


class PlantSpecies:
    def __init__(self, name=None, competitiveness=5, productivity=5, seedDispersalRate = 0.1):
        self.name = name
        self.competitiveness = competitiveness
        self.productivity = productivity
        self.id = generate_id(prefix='PS')
        self.isNullPlant = False
        self.seedDispersalRate = seedDispersalRate #Proportion of seeds that disperse to neighboring microhabitats.

    def __str__(self):
        """String representation of the Plant."""
        body = f"PlantSpeciesId: {self.id} Plant Stats {self.competitiveness}/{self.productivity}"
        return body

    def __repr__(self):
        """Representation of the Plant for debugging and object recreation."""
        return f"PlantSpecies(id= {self.id}', name='{self.name}', competitiveness={self.competitiveness}, productivity={self.productivity})\n"


    def set_self_as_null_plant(self):
        self.competitiveness = 0
        self.productivity = 0
        self.isNullPlant = True
        
    def set_attributes(self, competitiveness=random.randint(0, 10), productivity=random.randint(0, 10)):
        self.competitiveness = competitiveness
        self.productivity = productivity
        
    def set_name(self, name):
        self.name = name

    def evaluateSeedSurvival(self, seedCount):
        # This is a place holder for a function that will allow some species to have more persistent seed banks.
        return 0 

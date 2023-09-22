from Plant import Plant
from BeringiaUtilities import generate_id
from PlantSpeciesLibrary import PlantSpeciesLibrary


import random
import string

class PlantFactory:
    def __init__(self, psl = None):
        if (psl == None):
            self.plantSpeciesLibrary = PlantSpeciesLibrary()
        else:
            self.plantSpeciesLibrary = psl

    def create_plant(self, competitiveness=5, productivity=5, species_key = None):
        if (species_key):
            plantSpecies = self.plantSpeciesLibrary.get_species_by_id(species_key)
            newPlant = Plant(plantSpecies.competitiveness, plantSpecies.productivity)
            newPlant.species = plantSpecies
            newPlant.speciesName = plantSpecies.name
            return newPlant
        return Plant(competitiveness, productivity)
        
    def create_null_plant(self):
        id = self.plantSpeciesLibrary.primary_null_species.id
        return self.create_plant(species_key=self.plantSpeciesLibrary.primary_null_species.id)



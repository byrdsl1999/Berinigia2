from PlantSpecies import PlantSpecies
from PlantSpeciesLibrary import PlantSpeciesLibrary
from PlantNameGenerator import PlantNameGenerator

class PlantSpeciesFactory:
    def __init__(self, psl = None):
        if (psl == None):
            self.plantSpeciesLibrary = PlantSpeciesLibrary()
        else:
            self.plantSpeciesLibrary = psl
        self.create_null_species()
    
    def create_species(self, name=None, competitiveness=5, productivity=5):
        if name is None:
            name = PlantNameGenerator.makeName()
        newSpecies = PlantSpecies(name, competitiveness, productivity)
        self.plantSpeciesLibrary.add_species(newSpecies)
        return newSpecies
    
    def create_null_species(self):
        newSpecies = PlantSpecies('Bare Ground', 0, 0)
        newSpecies.isNullPlant = True
        self.plantSpeciesLibrary.add_species(newSpecies)
        return newSpecies

    def getPlantSpeciesLibrary(self):
        return self.plantSpeciesLibrary
from PlantFactory import PlantFactory
from BeringiaUtilities import generate_id
from collections import Counter


class Patch():
    def __init__(self, pf = PlantFactory()):
        self.plant_factory = pf
        self.plantSpeciesLibrary = self.plant_factory.plantSpeciesLibrary
        self.currentPlant = None
        self.currentPlantSpecies = None
        self.plantHistory = []
        self.id = generate_id(prefix='PA')
        self.insertNullPlant()
        self.seedProduction = Counter()
        self.seedsToGerminate = Counter()

    def __str__(self):
        body = f'PatchId: {self.id} {self.currentPlantSpecies}'
        return body

    def insertNewPlant(self, speciesId):
        if (self.currentPlant != None):
            if (self.currentPlant.species.isNullPlant != True):
                self.plantHistory.append(self.currentPlant)
        newPlant = self.plant_factory.create_plant(species_key=speciesId)
        self.currentPlant.die()
        self.currentPlant = newPlant
        self.currentPlantSpecies = newPlant.species

    def insertNewPlantRaw(self, newPlant):
        if (self.currentPlant != None):
            if (self.currentPlant.species.isNullPlant != True):
                self.plantHistory.append(self.currentPlant)
        self.currentPlant = newPlant
        self.currentPlantSpecies = newPlant.species

    def insertNullPlant(self):
        nullPlant = self.plant_factory.create_null_plant()
        self.insertNewPlantRaw(nullPlant)

    def removeCurrentPlant(self):
        if (self.currentPlant != None or self.currentPlant.species.isNullPlant != True):
            self.plantHistory.append(self.currentPlant)
        self.currentPlant = self.plant_factory.create_null_plant()

    def makeSeeds(self):
        localPlantSeedCounter = self.currentPlant.produceSeeds()
        self.seedProduction[self.currentPlantSpecies.id] = localPlantSeedCounter
        return self.seedProduction
    
    def germinateSeeds(self):
        bestSpeciesId = self.currentPlant.species.id

        bestSpecies = self.plantSpeciesLibrary.get_species_by_id(bestSpeciesId)
        bestCompetitiveness = bestSpecies.competitiveness
        for newSpeciesId in self.seedsToGerminate.keys():
            newSpecies = self.plantSpeciesLibrary.get_species_by_id(newSpeciesId)
            newCompetitiveness = newSpecies.competitiveness

            if newCompetitiveness > bestCompetitiveness:
                bestSpeciesId = newSpeciesId
                bestCompetitiveness = newCompetitiveness

        if self.currentPlant.id != bestSpeciesId:
            self.insertNewPlant(bestSpeciesId)
            return True
        return False
        
    def exterminateSeeds(self):
        self.seedProduction = Counter()
        for speciesId in self.seedsToGerminate.keys():
            currentSeedCount = self.seedsToGerminate[speciesId]
            newSeedCount = self.plantSpeciesLibrary.get_species_by_id(speciesId).evaluateSeedSurvival(currentSeedCount)
            self.seedsToGerminate[speciesId] = newSeedCount
        
    def disturb(self):
        self.currentPlant.die()
        self.insertNullPlant()
        
from Patch import Patch
from PlantFactory import PlantFactory
from PlantSpeciesLibrary import PlantSpeciesLibrary
from collections import Counter
from BeringiaUtilities import split_counter
from random import sample
from soil import Geology
import statistics

from constants import FEATURES_SWITCH



class Microhabitat:
    def __init__(self, size=10, pf = None, psl = None):
        self.size = size
        self.patches = list()
        self.seeds = Counter()
        self.seedsForExport = Counter()
        self.population = Counter()
        self.medianCompetitiveness = 0
        self.neighbors = list()
        self.on_fire = False
        
        if FEATURES_SWITCH['geology']:
            self.geology = Geology()

        
        if (psl == None and pf == None):
            self.plantSpeciesLibrary = PlantSpeciesLibrary()
            self.plant_factory = PlantFactory(psl=self.plantSpeciesLibrary)
            
        elif (psl == None and pf != None):
            self.plant_factory = pf
            if (self.plant_factory.plantSpeciesLibrary != None):
                self.plantSpeciesLibrary = self.plant_factory.plantSpeciesLibrary
                print(self.plantSpeciesLibrary)
                print(self.plantSpeciesLibrary.primary_null_species)
            else:
                self.plantSpeciesLibrary = PlantSpeciesLibrary()
                self.plant_factory.plantSpeciesLibrary = self.plantSpeciesLibrary

        elif (psl != None and pf == None):
            print('C happened')
            self.plantSpeciesLibrary = psl
            self.plant_factory = PlantFactory(psl=self.plantSpeciesLibrary)

        elif (psl != None and pf != None):
            print('D happened')
            self.plantSpeciesLibrary = psl
            self.plant_factory = pf
            
            
        self._createPatches()


    def __str__(self):
        """String representation of the Microhabitat."""
        patch_info =  "\n".join([f"Patch {i}: {patch}" for i, patch in enumerate(self.patches)])
        return f"Microhabitat - Size: {self.size}\n{patch_info}"
        
    def _createPatches(self):
        for _ in range(self.size):
            self.patches.append(Patch(self.plant_factory))

    
    def insertPlant(self, locationIndex, speciesId):
        self.patches[locationIndex].insertNewPlant(speciesId)
    
    def getPatch(self, locationIndex):
        return self.patches[locationIndex]

    def pass_time(self):
        self.runSeedLifeCycle()

    def runSeedLifeCycle(self):
        self.getSeedProduction()
        self.distributeSeeds()
        for patch in self.patches:
            patch.germinateSeeds()
            patch.exterminateSeeds()
        self.getPopCount()
        
        self.medianCompetitiveness = statistics.median([patch.currentPlant.species.competitiveness for patch in self.patches])
        print ('median: ' + str(self.medianCompetitiveness))


    def getSeedProduction(self):
        for patch in self.patches:
            self.seeds += patch.makeSeeds()
        
    def distributeSeeds(self):
        seedAllotments = split_counter(self.seeds, self.size)
        for i, patch in enumerate(self.patches):
            if not seedAllotments[i]:
                continue
            else: 
                patch.seedsToGerminate += seedAllotments[i]

    def germinateSeeds(self):
        for patch in self.patches:
            patch.germinateSeeds()
        
    def exterminateSeeds(self):
        for patch in self.patches:
            patch.exterminateSeeds()
        

    def getPopCount(self):
        patchSpecies = list()
        for patch in self.patches:
            patchSpecies.append(patch.currentPlantSpecies)
        self.population = Counter(patchSpecies)
        self.displayPopCount()
        self.calculateMedianCompetitivenessFromPopCount()
        
    def displayPopCount(self):
        name_count_counter = Counter({plant.name: count for plant, count in self.population.items()})
        print ('Population: ' + str(name_count_counter))
        return name_count_counter
        
    def runDisturbance(self, magnitude = 1.0, type = 'fire'):
        size = int(self.size * magnitude)
        if size > len(self.patches):
            size = len(self.patches)
        patchesToDisturb = sample(self.patches, k=size)
        for patch in patchesToDisturb:
            patch.disturb()

    def calculateMedianCompetitivenessFromPopCount(self):
        # Initialize variables
        middle_index = self.size // 2

        #Create sorted list
        sorted_data = sorted(self.population.items(), key=lambda item: item[0].competitiveness)
        competitiveness_values = []
        for plant, count in sorted_data:
            competitiveness_values.extend([plant.competitiveness] * count)

        # Calculate the median
        if self.size % 2 == 1:
            # Odd number of values, median is the middle value
            median = competitiveness_values[middle_index]
        else:
            # Even number of values, median is the average of the two middle values
            middle1 = competitiveness_values[middle_index - 1]
            middle2 = competitiveness_values[middle_index]
            median = (middle1 + middle2) / 2.0
        
        self.medianCompetitiveness = median
        return median
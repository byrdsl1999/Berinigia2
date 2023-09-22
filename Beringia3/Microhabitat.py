from Patch import Patch
from PlantFactory import PlantFactory
from collections import Counter
from BeringiaUtilities import split_counter


class Microhabitat:
    def __init__(self, size=10, pf = PlantFactory()):
        self.size = size
        self.patches = list()
        self.plant_factory = pf
        for _ in range(size):
            self.patches.append(Patch(pf))
        self.seeds = Counter()
        self.seedsForExport = Counter()
        self.population = Counter()

    def __str__(self):
        """String representation of the Microhabitat."""
        patch_info =  "\n".join([f"Patch {i}: {patch}" for i, patch in enumerate(self.patches)])
        return f"Microhabitat - Size: {self.size}\n{patch_info}"
    
    def insertPlant(self, locationIndex, speciesId):
        self.patches[locationIndex].insertNewPlant(speciesId)
    
    def getPatch(self, locationIndex):
        return self.patches[locationIndex]

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
        
    def runSeedLifeCycle(self):
        self.getSeedProduction()
        self.distributeSeeds()
        for patch in self.patches:
            patch.germinateSeeds()
            patch.exterminateSeeds()
        self.getPopCount()

    def getPopCount(self):
        patchSpecies = list()
        for patch in self.patches:
            patchSpecies.append(patch.currentPlantSpecies.name)
        self.population = Counter(patchSpecies)
        print ('Population: ' + str(self.population))
from .BeringiaUtilities import generate_id, stochastic_round

class Plant:
    def __init__(self, competitiveness=5, productivity=5):
        self.competitiveness = competitiveness
        self.productivity = productivity
        self.speciesName = None
        self.species = None
        self.health = 1
        self.alive = True
        self.id = generate_id(prefix='PL')
        
    def __str__(self):
        plant_info = str(self.competitiveness) + "/" + str(self.productivity)
        return f"PlantID:{self.id} "

    def makeSelfNullPlant(self):
        self.competitiveness = 0
        self.productivity = 0

    def setPlantSpecies(self, species):
        self.species = species
        return self.getAttributesFromSpecies(self)

    def getAttributesFromSpecies(self):
        if self.species:
            self.competitiveness = self.species.competitveness
            self.productivity = self.species.productivity
            self.speciesName = self.species.name
            return True
        return False

    def produceSeeds(self):
        seedcount = 0
        if self.alive:
            production = self.health * self.productivity
            seedcount = stochastic_round(production)
        return seedcount

    def die(self):
        self.health = 0.0
        self.alive = False
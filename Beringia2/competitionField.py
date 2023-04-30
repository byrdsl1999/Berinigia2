import random

class Field:
	def __init__(self, size: int = 100):
		self.size = size
		self.sites = []
		for i in range(self.size):
			self.addSiteToMap()
		self.plantTypes = dict()
			
	def __str__(self):
		return f"{self.sites}"

	def addSiteToMap(self):
		self.sites.append(SiteFactory.createSite())
		
	def addPlantToSite(self, siteId, plantId):
		print (siteId)
		print (plantId)
		tmp = self.sites[siteId]
		print (tmp)
		self.sites[siteId].setPlant(self.plantTypes[plantId])

class PlantType:
	def __init__(self, id, name, competitiveness: int = 1, seedProductivity: int = 10, dispersalRatio: float = 0.2):
		self.id = id
		self.name = name
		self.competitiveness = competitiveness
		self.seedProductivity = seedProductivity
		self.dispersalRatio = dispersalRatio # The proportion of seeds that move to neighboring regions.
		
	def __str__(self):
		return f"{self.competitiveness}"

	def getSeedProduction(self):	
		return self.seedProductivity
	
	def isMoreProductive(self, plant):
		return plant.competitiveness > self.competitiveness

class PlantFactory:
	def __init__(self, plant_types):
		self.plant_types = plant_types

	def createPlant(self, id): #createPlantType?
		if id not in self.plant_types:
			raise ValueError(f"Plant type with id {id} not found")

		plant_type = self.plant_types[id]
		plant = PlantType(*plant_type[1:])
		return plant
		
	def createPlantNull(self):
		return PlantType(0, 'nothing', 0, 0, 0)

class Site:
	def __init__(self):
		self.plantId = 0
		self.plant = None
		self.seeds = []
		
	def __str__(self):
		return f"{self.plantId}"
		
	def clearPlant(self):
		self.plantId = 0
		
	def setPlant(self, plant):
		self.plant = plant
		self.plantId = plant.id
	
	def setPlantId(self, plantId):
		self.plantId = plantId #TODO add competition check
		
class SiteFactory:
	def __init__(self):
		self.name = 'site factory object'
		
	@staticmethod
	def createSite():
			return Site()


shrub_types = [
	{'id': 1, 'name': 'Boxwood', 'competitiveness': 1, 'seedProductivity': 10, 'dispersalRatio': 0.2}
]

shrub_types = {
	1: (1, 'Boxwood', 1, 10, 0.2),
	2: (2, 'Forsythia', 2, 8, 0.2),
	3: (3, 'Hydrangea', 3, 6, 0.2),
	4: (4, 'Lilac', 4, 7, 0.2),
	5: (5, 'Privet', 5, 9, 0.2),
	6: (6, 'Holly', 6, 6, 0.2),
	7: (7, 'Azalea', 7, 5, 0.2),
	8: (8, 'Rhododendron', 8, 8, 0.2),
	9: (9, 'Juniper', 9, 5, 0.2),
	10: (10, 'Rose', 10, 9, 0.2)
}

tree_types = {
	1: (1, 'Oak', 1, 15, 0.2),
	2: (2, 'Maple', 2, 11, 0.2),
	3: (3, 'Pine', 3, 8, 0.2),
	4: (4, 'Cherry', 4, 9, 0.2),
	5: (5, 'Dogwood', 5, 14, 0.2),
	6: (6, 'Birch', 6, 10, 0.2),
	7: (7, 'Willow', 7, 7, 0.2),
	8: (8, 'Redwood', 8, 17, 0.2),
	9: (9, 'Magnolia', 9, 12, 0.2),
	10: (10,'Ash', 10, 9, 0.2)
}

grass_types = {
	1: (1, 'Bermuda', 1, 8, 0.2),
	2: (2, 'Zoysia', 2, 9, 0.2),
	3: (3, 'Fescue', 3, 5, 0.2),
	4: (4, 'Bluegrass', 4, 6, 0.2),
	5: (5, 'Rye', 5, 7, 0.2),
	6: (6, 'St. Augustine', 6, 7, 0.2),
	7: (7, 'Buffalo', 7, 4, 0.2),
	8: (8, 'Kentucky Blue', 8, 9, 0.2),
	9: (9, 'Centipede', 9, 3, 0.2),
	10: (10,'Bahia', 10, 6, 0.2)
}




#shrub = shrub_factory.createPlant(1)
#tree = tree_factory.createPlant(3)
#grass = grass_factory.createPlant(5)


def main():
	shrub_factory = PlantFactory(shrub_types)
	tree_factory = PlantFactory(tree_types)
	grass_factory = PlantFactory(grass_types)
	
	site_factory = SiteFactory()
	
	grasses = []
	
	f = Field()

	
	print (grass_types.keys())
	for key in grass_types.keys():
		newPlantType = grass_factory.createPlant(key)
		grasses.append(grass_factory.createPlant)
		f.plantTypes[key] = newPlantType
	
	f.addPlantToSite(random.randint(0,100), random.randint(0,10))
	
	for i in f.sites:
		print (i)


if __name__ == '__main__':
	main()
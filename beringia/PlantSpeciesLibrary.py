from .PlantSpecies import PlantSpecies

class PlantSpeciesLibrary:
    def __init__(self):
        self.primary_library = {}
        self.name_library = {}
        self.null_species = {}
        self.primary_null_species = None
        
        nullSpecies = self.create_null_species()
        self.add_species(nullSpecies)

    def add_species(self, species: PlantSpecies):
        if species.id not in self.primary_library:
            self.primary_library[species.id] = species
            self.name_library[species.name] = species
            if (species.isNullPlant):
                self.null_species[species.id] = species
                if (self.primary_null_species == None): 
                    self.primary_null_species = species

    
    
    def get_species_by_id(self, species_id):
        return self.primary_library.get(species_id)
    
    def get_species_by_name(self, species_name):
        return self.name_library.get(species_name)

    def get_all_species(self):
        return list(self.primary_library.values())
    
    def create_null_species(self): 
        newSpecies = PlantSpecies('Bare Ground', 0, 0)
        newSpecies.isNullPlant = True
        return newSpecies

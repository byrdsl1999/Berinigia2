from PlantSpecies import PlantSpecies
from PlantSpeciesLibrary import PlantSpeciesLibrary
from PlantNameGenerator import PlantNameGenerator

import xml.etree.ElementTree as ET
import json

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
    
    
    def import_species_from_xml(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for species_elem in root.findall('species'):
                name = species_elem.find('name').text
                competitiveness = int(species_elem.find('competitiveness').text)
                productivity = float(species_elem.find('productivity').text)

                new_species = self.create_species(name, competitiveness, productivity)
                # You can add additional processing here if needed

            print("Species imported successfully from XML.")
        except Exception as e:
            print(f"Error importing species from XML: {e}")

        return self.plantSpeciesLibrary
    
    def export_species_to_xml(self, xml_file):
        try:
            root = ET.Element("species_data")

            for species in self.plantSpeciesLibrary.species:
                species_elem = ET.SubElement(root, "species")
                name_elem = ET.SubElement(species_elem, "name")
                name_elem.text = species.name
                competitiveness_elem = ET.SubElement(species_elem, "competitiveness")
                competitiveness_elem.text = str(species.competitiveness)
                productivity_elem = ET.SubElement(species_elem, "productivity")
                productivity_elem.text = str(species.productivity)

            tree = ET.ElementTree(root)
            tree.write(xml_file)

            print(f"Species data exported to {xml_file}.")
        except Exception as e:
            print(f"Error exporting species data to XML: {e}")
            
    def export_species_to_json(self, json_file):
        try:
            species_list = []

            for species in self.plantSpeciesLibrary.species:
                species_data = {
                    "name": species.name,
                    "competitiveness": species.competitiveness,
                    "productivity": species.productivity
                }
                species_list.append(species_data)

            with open(json_file, 'w') as file:
                json.dump(species_list, file, indent=4)

            print(f"Species data exported to {json_file}.")
        except Exception as e:
            print(f"Error exporting species data to JSON: {e}")
            
    def import_species_from_json(self, json_file):
        try:
            with open(json_file, 'r') as file:
                species_list = json.load(file)

            for species_data in species_list:
                name = species_data.get("name")
                competitiveness = species_data.get("competitiveness")
                productivity = species_data.get("productivity")
                self.create_species(name, competitiveness, productivity)

            print(f"Species data imported from {json_file}.")
        except Exception as e:
            print(f"Error importing species data from JSON: {e}")
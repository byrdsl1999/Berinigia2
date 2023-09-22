# Imports
import Microhabitat as mh
from PlantFactory import PlantFactory
from PlantSpeciesFactory import PlantSpeciesFactory
from PlantSpeciesLibrary import PlantSpeciesLibrary
from time import sleep, time
from Calculator import Calculator
from BeringiaUtilities import stochastic_round

import math

CYCLECOUNT = 12
PAUSETIME = .01

def main():
    # Your main program logic goes here
    print ('This works B')
    
    calc = Calculator()

    psl = initializePlantSpeciesLibrary()
    psf = initializePlantSpeciesFactory(psl)
    pf = initializePlantFactory(psl)
    
    nullSpecies = psf.create_null_species()

    microhabitat = mh.Microhabitat(size = 100, pf = pf)
    print ('This works C')

    print (f'null species: {nullSpecies}')
    print (f'is null:  {nullSpecies.isNullPlant}')
    speciesList = []
    '''speciesList.append(psf.create_species(competitiveness=9, productivity=2))
    speciesList.append(psf.create_species(competitiveness=8, productivity=3))
    speciesList.append(psf.create_species(competitiveness=7, productivity=4))
    speciesList.append(psf.create_species(competitiveness=6, productivity=5))
    speciesList.append(psf.create_species(competitiveness=5, productivity=6))
    speciesList.append(psf.create_species(competitiveness=4, productivity=7))
    speciesList.append(psf.create_species(competitiveness=3, productivity=8))
    speciesList.append(psf.create_species(competitiveness=2, productivity=9))
    speciesList.append(psf.create_species(competitiveness=1, productivity=10))
    speciesList.append(psf.create_species(competitiveness=10, productivity=1))'''
    speciesList.append(psf.create_species(name = 'a', competitiveness=8, productivity=3))
    speciesList.append(psf.create_species(name = 'b', competitiveness=5, productivity=6))
    speciesList.append(psf.create_species(name = 'c', competitiveness=3, productivity=8))
    speciesList.append(psf.create_species(name = 'd', competitiveness=10, productivity=1))
    speciesList.append(psf.create_species(name = 'e', competitiveness=11, productivity=0.5))
    speciesList.append(psf.create_species(name = 'f', competitiveness=12, productivity=0.2))
    speciesList.append(psf.create_species(name = 'g', competitiveness=13, productivity=0.1))
    speciesList.append(psf.create_species(name = 'h', competitiveness=14, productivity=0.01))

    for i, sp in enumerate(speciesList):
        print (sp)
        microhabitat.insertPlant(i, sp.id)
    
    print (microhabitat)
    sleep(2)
    
    for i in range(CYCLECOUNT):
        print (i)
        microhabitat.runSeedLifeCycle()
        calc.species_counts = microhabitat.population
        print(f"richness: {calc.richness()}")
        print(f"Shannon Diversity Index: {calc.shannon_diversity_index()}")
        print(f"Simpson's Diversity Index: {calc.simpsons_diversity_index()}")
        print(f"Pielou's Evenness Index: {calc.pielous_evenness_index()}")

        #print (microhabitat)


        sleep(PAUSETIME)
    
    tote = 0
    for i in range (100):
        each = stochastic_round(43.7)
        tote += each
        print (each)
    print ('end ' + str(tote))




def initializePlantSpeciesLibrary():
    psl = PlantSpeciesLibrary()
    return psl

def initializePlantSpeciesFactory(psl = None):
    psf = PlantSpeciesFactory(psl)
    return psf

def initializePlantFactory(psl = None):
    pf = PlantFactory(psl)    
    return pf



# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
    



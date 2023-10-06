# Imports
import Microhabitat as mh
from PlantFactory import PlantFactory
from PlantSpeciesFactory import PlantSpeciesFactory
from PlantSpeciesLibrary import PlantSpeciesLibrary
from time import sleep, time
from Calculator import Calculator
from BeringiaUtilities import stochastic_round

import math

CYCLECOUNT = 200
PAUSETIME = .0

def main():
    
    #branch1()
    branch2()


def branch1():
    
    
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
    speciesList.append(psf.create_species(competitiveness=9, productivity=2))
    speciesList.append(psf.create_species(competitiveness=8, productivity=3))
    speciesList.append(psf.create_species(competitiveness=7, productivity=4))
    speciesList.append(psf.create_species(competitiveness=6, productivity=5))
    speciesList.append(psf.create_species(competitiveness=5, productivity=6))
    speciesList.append(psf.create_species(competitiveness=4, productivity=7))
    speciesList.append(psf.create_species(competitiveness=3, productivity=8))
    speciesList.append(psf.create_species(competitiveness=2, productivity=9))
    speciesList.append(psf.create_species(competitiveness=1, productivity=10))
    speciesList.append(psf.create_species(competitiveness=10, productivity=1))
    
    '''speciesList.append(psf.create_species(name = 'a', competitiveness=3, productivity=8))
    speciesList.append(psf.create_species(name = 'b', competitiveness=5, productivity=6))
    speciesList.append(psf.create_species(name = 'c', competitiveness=8, productivity=3))
    speciesList.append(psf.create_species(name = 'd', competitiveness=10, productivity=1))
    speciesList.append(psf.create_species(name = 'e', competitiveness=11, productivity=0.5))
    speciesList.append(psf.create_species(name = 'f0', competitiveness=12, productivity=0.2))
    speciesList.append(psf.create_species(name = 'f1', competitiveness=12.1, productivity=0.18))
    speciesList.append(psf.create_species(name = 'f2', competitiveness=12.2, productivity=0.16))
    speciesList.append(psf.create_species(name = 'f3', competitiveness=12.3, productivity=0.14))
    speciesList.append(psf.create_species(name = 'g', competitiveness=13, productivity=0.1))
    speciesList.append(psf.create_species(name = 'h', competitiveness=14, productivity=0.05))'''

    for i, sp in enumerate(speciesList):
        print (sp)
        microhabitat.insertPlant(i, sp.id)
    
    print (microhabitat)
    sleep(2)
    
    for i in range(CYCLECOUNT):
        print (i)
        microhabitat.runSeedLifeCycle()
        calc.species_counts = microhabitat.population
        #print(f"richness: {calc.richness()}")
        print(f"Shannon Diversity Index: {calc.shannon_diversity_index()}")
        #print(f"Simpson's Diversity Index: {calc.simpsons_diversity_index()}")
        #print(f"Pielou's Evenness Index: {calc.pielous_evenness_index()}")

        #print (microhabitat)


        sleep(PAUSETIME)
    


def branch2():
    microhabitat = mh.Microhabitat(size = 100)
    psf = initializePlantSpeciesFactory(microhabitat.plantSpeciesLibrary)
    calc = Calculator()


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
    
    speciesList.append(psf.create_species(name = 'a', competitiveness=1, productivity=8))
    speciesList.append(psf.create_species(name = 'b', competitiveness=2, productivity=5))
    speciesList.append(psf.create_species(name = 'c', competitiveness=3, productivity=3))
    speciesList.append(psf.create_species(name = 'd', competitiveness=4, productivity=1))
    speciesList.append(psf.create_species(name = 'e', competitiveness=5, productivity=0.5))
    speciesList.append(psf.create_species(name = 'f0', competitiveness=6, productivity=0.2))
    speciesList.append(psf.create_species(name = 'f1', competitiveness=7, productivity=0.18))
    speciesList.append(psf.create_species(name = 'f2', competitiveness=8, productivity=0.16))
    speciesList.append(psf.create_species(name = 'f3', competitiveness=9, productivity=0.14))
    speciesList.append(psf.create_species(name = 'g', competitiveness=10, productivity=0.1))
    speciesList.append(psf.create_species(name = 'h', competitiveness=11, productivity=0.05))

    
    for i, sp in enumerate(speciesList):
        print (sp)
        microhabitat.insertPlant(i, sp.id)
    
    print (microhabitat)
    sleep(2)
    
    DISTURBANCE_FREQUENCY = 15
    counter = 0

    for i in range(CYCLECOUNT):
        if counter == DISTURBANCE_FREQUENCY:
            print('DISTURBING')
            microhabitat.runDisturbance(magnitude= 0.7)
            counter = 0
        microhabitat.runSeedLifeCycle()
        
        calc.species_counts = microhabitat.population
        #print(f"richness: {calc.richness()}")
        #print(f"Shannon Diversity Index: {calc.shannon_diversity_index()}")
        #print(f"Simpson's Diversity Index: {calc.simpsons_diversity_index()}")
        #print(f"Pielou's Evenness Index: {calc.pielous_evenness_index()}")

        #print (microhabitat)

    
        counter += 1


        sleep(PAUSETIME)
    #print([plant.speciesName for plant in microhabitat.patches[20].plantHistory])
    #print([plant.speciesName for plant in microhabitat.patches[40].plantHistory])
    #print([plant.speciesName for plant in microhabitat.patches[60].plantHistory])



def initializePlantSpeciesLibrary():
    psl = PlantSpeciesLibrary()
    return psl

def initializePlantSpeciesFactory(psl = None):
    psf = PlantSpeciesFactory(psl)
    psf.create_null_species()
    return psf

def initializePlantFactory(psl = None):
    pf = PlantFactory(psl)    
    return pf



# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
    



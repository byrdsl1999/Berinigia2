# Imports
from beringia.region import Region
import beringia.Microhabitat as mh
from beringia.PlantFactory import PlantFactory
from beringia.PlantSpeciesFactory import PlantSpeciesFactory
from beringia.PlantSpeciesLibrary import PlantSpeciesLibrary
from time import sleep, time
from beringia.Calculator import Calculator
from beringia.BeringiaUtilities import stochastic_round

import math

CYCLECOUNT = 30
PAUSETIME = .0

def main():
    
    #branch1()
    #branch2()
    branch3()


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

def branch3():
    r = Region(xdim=30, ydim=20)
    print(r)
    r.verbose = True
    
    '''speciesList = []
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's1', competitiveness=1, productivity=0.3))
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's2', competitiveness=2, productivity=0.241))
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's3', competitiveness=3, productivity=0.193))
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's4', competitiveness=4, productivity=0.155))
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's5', competitiveness=5, productivity=0.125))
    speciesList.append(r.plantSpeciesFactory.create_species(name = 's6', competitiveness=6, productivity=0.1))'''
    
    psf = r.plantSpeciesFactory
    
    speciesList =  psf.import_species_from_xml('data/species_data_log.xml').get_all_species()
    
    for i, sp in enumerate(speciesList):
        print (sp)
        print (r.nodes)
        for node in r.nodeValues.values():
            print (node)
            node['locale'].insertPlant(i, sp.id)

    r.show_map()
    r.get_locale(1,1).geology.elevation = 8.0
    print(r.get_locale(1,1).geology.elevation)
    for i in range(CYCLECOUNT):
        r.pass_time()
        r.show_map()
        print(r.get_locale(0,0).population)
    r.get_locale(1,1).on_fire = True
    r.spread_fire()

    for i in range(CYCLECOUNT):
        r.pass_time()
        r.show_map()
        print(r.get_locale(0,0).population)



    print(r.get_locale(1,1).geology.elevation)

    r.show_map()
    print(r.get_locale(0,0).population)
    print(r.get_locale(1,1).population)



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
    



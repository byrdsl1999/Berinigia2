from beringia.Plant import Plant  # Adjust the import path
from beringia.BeringiaUtilities import generate_id, stochastic_round  # Adjust the import path

def test_initialization():
    plant = Plant()
    assert plant.competitiveness == 5
    assert plant.productivity == 5
    assert plant.speciesName is None
    assert plant.species is None
    assert plant.health == 1
    assert plant.alive is True
    assert plant.id.startswith('PL')

def test_make_self_null_plant():
    plant = Plant()
    plant.makeSelfNullPlant()
    assert plant.competitiveness == 0
    assert plant.productivity == 0

def test_set_plant_species():
    plant = Plant()

    class MockSpecies:
        competitiveness = 10
        productivity = 8
        name = "Mock Species"

    result = plant.setPlantSpecies(MockSpecies)
    assert result is True
    assert plant.competitiveness == 10
    assert plant.productivity == 8
    assert plant.speciesName == "Mock Species"

def test_produce_seeds():
    plant = Plant()
    plant.productivity = 10
    seeds = plant.produceSeeds()
    print(seeds)
    assert seeds == 10

    # Test with a different productivity
    plant.productivity = 10
    plant.health = 0.5
    seeds = plant.produceSeeds()
    # Adjust this based on your stochastic_round logic
    assert seeds == 5
    
    # Test with a different health value
    plant.alive = False
    seeds = plant.produceSeeds()
    # Adjust this based on your stochastic_round logic
    assert seeds == 0


def test_die():
    plant = Plant()
    plant.die()
    assert plant.health == 0.0
    assert plant.alive is False
import pytest
from beringia.Microhabitat import Microhabitat

def test_microhabitat_creation():
    mh = Microhabitat()
    assert mh.size == 100
    assert mh.patches
    assert mh.seeds == mh.seedsForExport == mh.population == Counter()
    assert mh.medianCompetitiveness == 0
    assert not mh.neighbors
    assert not mh.on_fire
    if FEATURES_SWITCH['geology']:
        assert mh.geology
    else:
        assert not hasattr(mh, 'geology')

def test_microhabitat_insert_plant():
    mh = Microhabitat()
    mh.insertPlant(0, 1)  # Insert a plant at the first location
    assert mh.getPatch(0).currentPlantSpecies == 1

def test_microhabitat_seed_lifecycle():
    mh = Microhabitat()
    mh.runSeedLifeCycle()
    # Add assertions for seed lifecycle tests

# Add more test cases as needed

if __name__ == "__main__":
    pytest.main()

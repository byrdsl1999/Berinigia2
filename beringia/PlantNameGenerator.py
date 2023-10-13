import random

class PlantNameGenerator():
    GENUS_ROOTS = [
        'acer', 'alba', 'anthem', 'aqua', 'cact', 'citr', 'flor', 'frax', 'herba',
        'hydr', 'lil', 'mal', 'olea', 'pop', 'ros', 'salv', 'solan', 'spir', 'ver'
    ]

    GENUS_SUFFIXES = [
        'oides', 'ensis', 'aceae', 'ana', 'ia', 'ina', 'ata', 'ella', 'aria', 'inae',
        'ica', 'ifolia', 'iforme', 'iflorus', 'ipetalum', 'iphyllum', 'iphytum', 'is', 'isca',
        'odendron', 'odora', 'oida', 'olens', 'olina', 'omorpha', 'ophyta', 'opogon', 'osum',
        'otus', 'oxylon', 'oxyphyllum', 'oxys', 'ula', 'um', 'una', 'unda', 'unum'
    ]

    SPECIES_ROOTS = ['acer', 'aqua', 'carn', 'cerebr', 'flor', 'ign', 'lumin', 'nuc', 'ped', 'sanguin',
            'squam', 'stell', 'tigr', 'vibr', 'albus', 'bell', 'caerule', 'canin', 'capr', 'cord', 
            'coron', 'cris', 'drac', 'equi', 'fer', 'gemin', 'herba', 'lepid', 'magn', 'ov', 'pisc', 
            'porc', 'radi', 'rapt', 'ros', 'serp', 'sol', 'ter', 'umbra', 'ur', 'virid', 'vol', 'xanth', 'zephyr']

    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'

    @staticmethod
    def makeName():
        genus_name = random.choice(PlantNameGenerator.GENUS_ROOTS) + random.choice(PlantNameGenerator.GENUS_SUFFIXES)
        genus_name = genus_name.capitalize()
        species_name = random.choice(PlantNameGenerator.GENUS_ROOTS) + random.choice(PlantNameGenerator.vowels) + random.choice(PlantNameGenerator.consonants)
        full_name = ' '.join([genus_name, species_name])
        return full_name
    
def main():
    name = PlantNameGenerator.makeName()
    print(name)

if __name__ == '__main__':
    main()

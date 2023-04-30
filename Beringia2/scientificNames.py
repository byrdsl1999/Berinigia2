import random

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

roots = ['acer', 'aqua', 'carn', 'cerebr', 'flor', 'ign', 'lumin', 'nuc', 'ped', 'sanguin',
		'squam', 'stell', 'tigr', 'vibr',	'albus', 'bell', 'caerule', 'canin', 'capr', 'cord', 
		'coron', 'cris', 'drac', 'equi',	'fer', 'gemin', 'herba', 'lepid', 'magn', 'ov', 'pisc', 
		'porc', 'radi', 'rapt',	'ros', 'serp', 'sol', 'ter', 'umbra', 'ur', 'virid', 'vol', 'xanth', 'zephyr']

def generate_name():
	root = random.choice(roots)
	name = ''
	for i in range(2):
		if i == 0:
			name += root[0].upper() + root[1:]
		else:
			name += random.choice(vowels)
			name += random.choice(consonants)
	return name

for i in range(10):
	print(generate_name() + ' ' + generate_name())


import random


class BotanicalNameGenerator:
    GENUSES = [
        'acer', 'alba', 'anthem', 'aqua', 'cact', 'citr', 'flor', 'frax', 'herba',
        'hydr', 'lil', 'mal', 'olea', 'pop', 'ros', 'salv', 'solan', 'spir', 'ver'
    ]
    SUFFIXES = [
        'oides', 'ensis', 'aceae', 'ana', 'ia', 'ina', 'ata', 'ella', 'aria', 'inae',
        'ica', 'ifolia', 'iforme', 'iflorus', 'ipetalum', 'iphyllum', 'iphytum', 'is', 'isca',
        'odendron', 'odora', 'oida', 'olens', 'olina', 'omorpha', 'ophyta', 'opogon', 'osum',
        'otus', 'oxylon', 'oxyphyllum', 'oxys', 'ula', 'um', 'una', 'unda', 'unum'
    ]

    @staticmethod
    def generate_name_botanic():
        # Choose a random root and suffix from the lists
        genus_root = random.choice(BotanicalNameGenerator.ROOTS)
        species_suffix = random.choice(BotanicalNameGenerator.SUFFIXES)

        # Combine the root and suffix to form the scientific name
        genus_name = genus_root.capitalize()
        species_name = species_suffix
        scientific_name = genus_name + ' ' + species_name

        return scientific_name


# Example usage
name = BotanicalNameGenerator.generate_name_botanic()
print('Botanical name: ' + name)

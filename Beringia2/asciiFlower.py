import random

def generate_flower(stemLength, leafGap, flowerWidth=7, leavesAlternate=False):
    petals = [['(', ')'], ['{', '}'], ['', '']]
    sepals = ['~', '~', '∫', '≈']
    flowerBases = ['Y', 'T', 'w', 'W']
    stems = ['|', 'I', 'H', '#', 'M', 'W', '8', '||']
    leaves = [['-', '-'], ['\\', '/'], ['/', '\\'], ['o','o'], ['<', '>'], ['^', '^']]

    seeds = ['.', ',', '•', '∆']
    
    plant = ""



    # create flower 
    flower = ""
    petal = random.choice(petals)
    seed = random.choice(seeds)
    flower += " " * ((flowerWidth - 5) // 2) # pad the flower to center it
    flower += petal[0]
    flower += seed * max(1, (flowerWidth-2))
    flower += petal[1]
    flower += "\n"

    plant += flower

    # add flower base
    flowerBase = ""
    flowerBase += " " * ((flowerWidth - 3) // 2) # pad the flower base to center it
    sepal = random.choice(sepals)
    flowerBase += sepal
    flowerBase += random.choice(flowerBases)
    flowerBase += sepal
    flowerBase += "\n"

    plant += flowerBase



    # add stem

    ##create Stem Unit
    leaf = random.choice(leaves)
    stem = random.choice(stems)
    padding = ((flowerWidth - 3) // 2)
    stemUnit = ""
    stemUnit += " " * padding # pad the flower base to center it
    stemUnit += leaf[0]
    stemUnit += stem
    if (not leavesAlternate): 
        stemUnit += leaf[1]
    else:
        stemUnit += "\n"    
        stemUnit += " " * (padding +1)
        stemUnit += stem
        stemUnit += leaf[1]
    stemUnit += "\n"    
    for _ in range(leafGap):
        stemUnit += " " * (padding +1)
        stemUnit += stem
        stemUnit += "\n"    

    ##append Stem units to plant
    for _ in range(stemLength):
        plant += stemUnit

    return plant
	
if __name__ == '__main__':
	print(generate_flower(random.randint(2,6), random.randint(0,3)))
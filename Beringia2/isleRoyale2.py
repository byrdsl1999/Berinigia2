import matplotlib.pyplot as plt

# Set simulation parameters
num_steps = 1000
dt = 1

# Set initial population sizes
moose_population = 50
wolf_population = 5

# Set birth and death rates
moose_birth_rate = 0.05
moose_death_rate = 0.02
wolf_birth_rate = 0.02
wolf_death_rate = 0.05

# Set predation rate
predation_rate = 0.001

# Initialize population lists
moose_population_list = [moose_population]
wolf_population_list = [wolf_population]

# Run simulation
for i in range(num_steps):
    # Calculate birth and death rates for each species
    moose_births = moose_birth_rate * moose_population
    moose_deaths = moose_death_rate * moose_population + predation_rate * wolf_population * moose_population
    wolf_births = wolf_birth_rate * wolf_population
    wolf_deaths = wolf_death_rate * wolf_population - predation_rate * wolf_population * moose_population
    
    # Update population sizes
    moose_population += (moose_births - moose_deaths) * dt
    wolf_population += (wolf_births - wolf_deaths) * dt
    
    # Append current population sizes to population lists
    moose_population_list.append(moose_population)
    wolf_population_list.append(wolf_population)

# Plot population sizes over time
plt.plot(range(num_steps+1), moose_population_list, label="Moose")
plt.plot(range(num_steps+1), wolf_population_list, label="Wolves")
plt.xlabel("Time Steps")
plt.ylabel("Population Size")
plt.title("Isle Royale Moose-Wolf Population Dynamics")
plt.legend()
plt.show()
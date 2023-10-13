# -*- coding: utf-8 -*-
"""fauna.py

TODO:
    Fauna falls into two categories: bulk and unit fauna.
    Bulk Fauna:
        These are not individuals but aggregate masses of creatures in a single locale.
        They are tracked as non-discrete populations, such as insects.
        
        Behaviors:
        - Eating/Consuming resources
            - Plant detritus
            - Fauna detritus
            - Live plants
            - Live unit fauna (e.g., ticks, fleas, parasites)
            - Dead fauna
            - Other bulk fauna
        - Mating
        - Migration
            - Emigration
                - Find emigration target
            - Immigration
        - Death
            - Getting Depredated
            - Starvation
            - Other

    Unit Fauna:
        These are roving creatures tracked individually.
        
        Behaviors:
        - Eating
        - Food detection
        - Seeking food
        - Following prey
        - Evading predators
        - Mating
        - Maintaining home ranges
        - Herb behavior (mobile home range)
    
    Food Web:
    Two types:
    1. A simple food chain: Plants -> Herbivores -> Carnivores
    2. A complex food web

    Beavers:
    Pond building

For more information on docstring formatting, see the 
[Sphinx Napoleon docstring example](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
"""

from beringia_deprecated.feature import Feature
from beringia_deprecated.flora import PlantBulk, Flora
from math import floor
from numpy.random import binomial
from beringia_deprecated.constants import CONT_TO_DISC_FAUNA_CONVERSION
#TODO import detritus object

class FoodWeb(Feature):
    """FoodWeb class docs

    This functions as a container for the various fauna. The main purpose should be for timing their actions, and also
    keeping track of who is eating who. Not yet implemented.

    Args:
        arg (str):

    """
    def __init__(self):
        super(Fauna, self).__init__()


class Fauna(Feature):
    """Fauna class docs

    Args:
        arg (str):

    """
    def __init__(self, location = "hi"):
        super(Fauna, self).__init__(location=location)



class FeedBag(Fauna):
    """FeedBag class docs

    A dummy bulk animal pop with only pop as an attribute. It is used for debugging, so a test population has something
    to feed off of.

    Args:
        population (float):

    """
    def __init__(self, population=1.0, bottomless=False):
        super().__init__()
        self.population = population
        self.cryptocity = 0.0 #                     # Cryptocity rate is how hard a species is to find.(eg a mole may have a cryptocity of 0.8, while a singing bird might be 0.1)
        self.bottomless = bottomless

    def __repr__(self, verbose=False):
        if not verbose:
            return("FeedBag: "+str(self.population))
        else:
            return("FeedBag: "+str(self.population)) #TODO change something more specific

    def _zero_correct_pop(self):
        """_zero_correct_pop docs
        Private method that sets negative population values to zero. Returns False if population is <=0.

        """
        if self.population <= 0.0:
            self.population = 0.0
            return False
        return True

    def _is_feedbag(self):
        return True

    def get_depredated(self, magnitude=0.1, percentage=None):
        """get_depredated docs
        Population experiences predation.
        """
        if self.bottomless:
            magnitude = 0.0
            percentage = 0.0
        if not percentage:
            self.population -= magnitude
        if percentage:
            self.population = self.population * (1.0-percentage)
        return self._zero_correct_pop()


class FeedBagD(Fauna):
    """FeedBag class docs

    A discrete version of the FeedBag object type.

    A dummy bulk animal pop with only pop as an attribute. It is used for debugging, so a test population has something
    to feed off of.

    Args:
        population (float):

    """
    def __init__(self, population=100, bottomless=False):
        super().__init__()
        self.population = population
        self.cryptocity = 0.0 #                     # Cryptocity rate is how hard a species is to find.(eg a mole may have a cryptocity of 0.8, while a singing bird might be 0.1)
        self.bottomless = bottomless

    def __repr__(self, verbose=False):
        if not verbose:
            return("FeedBagD: "+str(self.population))
        else:
            return("FeedBagD: "+str(self.population)) #TODO change something more specific

    def _zero_correct_pop(self):
        """_zero_correct_pop docs
        Private method that sets negative population values to zero. Returns False if population is <=0.

        """
        if self.population < 0:
            self.population = 0
            return False
        return True

    def _is_feedbag(self):
        return True

    def get_depredated(self, magnitude=1, percentage=None):
        """get_depredated docs
        Population experiences predation.
        """
        predation_quantity = 0
        if not percentage:
            predation_quantity = int(magnitude)
        if percentage:
            self.population -= self.population * (1.0-percentage)
            predation_quantity = int(self._zero_correct_pop * percentage)
        self.population -= predation_quantity
        return predation_quantity


class BulkFauna(Fauna):
    """BulkFauna class docs

    A continuous population of a single species contained by a single locale.

    The general principle for bulk populations is that there is a continuous population value. This population attempts
    to feed on some target(which may be another animal population, plant, or detritus(eventually). If the population is
    successful in feeding, then stress should decrease; If not stress should increase by a magnitude proportional to
    magnitude of the failure. The stress level should then produce a response than can include reproducing, dying and
    emigrating.

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):

    """

    def __init__(self, population=1, reproduction_rate=0.04, starvation_rate=0.3, feeding_rate=0.3,
                 emigration_rate=0.1, prey=FeedBag(), location=None, name=None):
        """

        :type prey: feature
        """
        super().__init__(location=location)
        self.name = name
        self.population = population
        self.reproduction_rate = reproduction_rate  # Repro rate is essentially the energy conversion rate. (eg 10 lb grass makes 1 lb beef)
        self.starvation_rate = starvation_rate
        self.feeding_rate = feeding_rate
        self.emigration_rate = emigration_rate
        self.ambient_death_rate = 0.05
        self.stress = 0.0
        self.cryptocity = 0.8 #                     # Cryptocity rate is how hard a species is to find.(eg a mole may have a cryptocity of 0.8, while a singing bird might be 0.1)
        self.stress_responses = {
            'migrate': 0.375,
            'starve': 0.85,
            'reproduce': 0.20
        }
        self.prey = prey
        self.verbose = False


    def __repr__(self):
        if self.name:
            if not self.verbose:
                return(name+" "+str(self.population))
            else:
                return(name+" Pop: "+str(self.population)+" Stress: "+str(self.stress)) #TODO change something more specific
        else:
            if not self.verbose:
                return("Bulk Fauna: "+str(self.population))
            else:
                return("Bulk Fauna Pop: "+str(self.population)+" Stress: "+str(self.stress)) #TODO change something more specific


    def _zero_correct_pop(self):
        """_zero_correct_pop docs
        Private method that sets negative population values to zero. Returns False if population is <=0.

        """
        if self.population <= 0.0:
            self.population = 0.0
            return False
        return True

    def _stress_correct(self):
        """_stress_correct docs
        Private method that sets stress levels be bound by (0, 1) inclusive. Returns False if adjustment made, True otherwise.

        """
        if self.stress <= 0.0:
            self.stress = 0.0
            return False
        if self.stress > 1.0:
            self.stress = 1.0
            return False
        return True

    def pass_turn(self):
        """pass_turn docs
        Run all actions that occur in 1 unit of time.
        """
        self.feed()
        self.stress_response()

    def feed(self, target=None):
        """feed docs
        Target should default to self.prey generally. (ie self.prey should be the thing that this fauna generally feeds
        on)

        TODO Maybe add default target attributes, if the target is something like fauna or detritus?
        """
        if not target:
            target = self.prey
        if isinstance(target, BulkFauna):
            consumption = self.population * self.feeding_rate
            available_food = target.population * (1-target.cryptocity)
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.35
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .25)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " + str(enough_food) + " Method: bulkfauna")
                print("  consumption: " + str(consumption) + "  available food: " + str(available_food))
            return enough_food
        elif isinstance(target, BulkFaunaD):
            consumption_magnitude = self.population * self.feeding_rate * CONT_TO_DISC_FAUNA_CONVERSION
            consumption = floor(consumption_magnitude) + binomial(1, consumption_magnitude % 1)
            available_food = target.population * (1-target.cryptocity)
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.35
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .25)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " +str(enough_food)+" Method: bulkfaunad")
                print("  consumption: "+ str(consumption)+"  available food: "+ str(available_food))
            return enough_food
        elif isinstance(target, Flora):
            consumption = self.population * self.feeding_rate
            available_food = target.state
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.25
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .25)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " + str(enough_food) + " Method: bulkfauna")
                print("  consumption: " + str(consumption) + "  available food: " + str(available_food))
            return enough_food

    def stress_response(self):
        self._stress_correct()
        if self.stress <= self.stress_responses['reproduce']:
            self.reproduce()
        if self.stress > self.stress_responses['starve']:
            self.starve()
        if self.stress > self.stress_responses['migrate']:
            self.emigrate()

    def starve(self, magnitude=1.0):
        starvation_quantity= self.population * self.starvation_rate * magnitude
        self.population -= starvation_quantity
        if self.verbose:
            print(self.__repr__() +" starving: " + str(starvation_quantity))
        return starvation_quantity

    def emigrate(self, magnitude=1.0):
        emigration_quantity = self.population * self.emigration_rate * magnitude
        if emigration_quantity > self.population:
            emigration_quantity = self.population
        self.population -= emigration_quantity
        #TODO self.location.get_neighbors.population += emigration_quantity # TODO pseudocode. Finish this.
        if self.verbose:
            print(self.__repr__() +" emigrating: "+str(emigration_quantity))
        return emigration_quantity

    def reproduce(self, magnitude=1.0):
        growth_quantity = self.population * self.reproduction_rate * magnitude
        self.population += growth_quantity
        if self.verbose:
            print(self.__repr__() +" reproducing: " + str(growth_quantity))
        return growth_quantity

    def get_depredated(self, magnitude=0.1, percentage=None):
        """get_depredated docs
        Population experiences predation.
        """
        if not percentage:
            predation_quantity = magnitude
        if percentage:
            predation_quantity = self.population * (1.0-percentage)
        self.population -= predation_quantity
        if self.verbose:
            print(self.__repr__() +" Preyed upon: " + str(predation_quantity))
        return self._zero_correct_pop()


class BulkFaunaD(Fauna):
    """AnimalBulk class docs

    A continuous population of a single species contained by a single locale.

    The general principle for bulk populations is that there is a continuous population value. This population attempts
    to feed on some target(which may be another animal population, plant, or detritus(eventually). If the population is
    successful in feeding, then stress should decrease; If not stress should increase by a magnitude proportional to
    magnitude of the failure. The stress level should then produce a response than can include reproducing, dying and
    emigrating.

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):

    """
    def __init__(self, population=10, reproduction_rate=0.04, starvation_rate=0.3, feeding_rate=0.3,
                 emigration_rate=0.3, prey=FeedBagD(), location=None, name=None):
        super().__init__(location=location)
        self.name=name
        self.population = population
        self.reproduction_rate = reproduction_rate  # Repro rate is essentially the energy conversion rate. (eg 10 lb grass makes 1 lb beef)
        self.starvation_rate = starvation_rate
        self.feeding_rate = feeding_rate
        self.emigration_rate = emigration_rate
        self.ambient_death_rate = 0.05
        self.stress=0.0
        self.cryptocity = 0.8 #                     # Cryptocity rate is how hard a species is to find.(eg a mole may have a cryptocity of 0.8, while a singing bird might be 0.1)
        self.stress_responses ={
            'migrate': 0.375,
            'starve': 0.75,
            'reproduce': 0.20
        }
        self.prey = prey
        self.verbose = True

    def __repr__(self):
        if self.name:
            if not self.verbose:
                return(name+" "+str(self.population))
            else:
                return(name+" Pop: "+str(self.population)+" Stress: "+str(self.stress)) #TODO change something more specific
        else:
            if not self.verbose:
                return("Bulk Fauna D: "+str(self.population))
            else:
                return("Bulk Fauna D Pop: "+str(self.population)+" Stress: "+str(self.stress)) #TODO change something more specific


    def _zero_correct_pop(self):
        """_zero_correct_pop docs
        Private method that sets negative population values to zero. Returns False if population is <=0.

        """
        if self.population < 0:
            self.population = 0
            return False
        return True

    def _stress_correct(self):
        """_stress_correct docs
        Private method that sets stress levels be bound by (0, 1). Returns False if adjustment made, true otherwise.

        """
        if self.stress <= 0.0:
            self.stress = 0.0
            return False
        if self.stress > 1.0:
            self.stress = 1.0
            return False
        return True

    def _is_feedbag(self):
        return False

    def pass_turn(self):
        """pass_turn docs
        Run all actions that occur in 1 unit of time.
        """
        self.feed()
        self.stress_response()

    def feed(self, target=None): #not rewritten for discrete
        """feed docs
        Target should default to self.prey generally. (ie self.prey should be the thing that this fauna generally feeds
        on)

        TODO Maybe add default target attributes, if the target is something like fauna or detritus?
        """
        if not target:
            target = self.prey
        if isinstance(target, BulkFauna):
            consumption = self.population * self.feeding_rate / CONT_TO_DISC_FAUNA_CONVERSION
            available_food = target.population * (1-target.cryptocity)
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.35
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .5)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " +str(enough_food)+" Method: bulkfauna")
                print("  consumption: "+ str(consumption)+"  available food: "+ str(available_food))
            return enough_food
        elif isinstance(target, BulkFaunaD):
            consumption_magnitude = self.population * self.feeding_rate
            consumption = floor(consumption_magnitude) + binomial(1, consumption_magnitude % 1)
            available_food = target.population * (1-target.cryptocity)
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.35
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .5)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " +str(enough_food)+" Method: bulkfaunad")
                print("  consumption: "+ str(consumption)+"  available food: "+ str(available_food))
            return enough_food
        elif isinstance(target, Flora):
            consumption = self.population * self.feeding_rate / CONT_TO_DISC_FAUNA_CONVERSION
            available_food = target.state
            if available_food >= consumption:
                target.get_depredated(consumption)
                enough_food = True
            else:
                target.get_depredated(available_food)
                enough_food = False
            if enough_food:
                self.stress = self.stress * 0.35
            elif not enough_food:
                self.stress -= ((available_food - consumption)/consumption * .5)   #Please improve this.
            if self.verbose:
                print(self.__repr__() + " feeding: " +str(enough_food)+" Method: flora")
                print("  consumption: "+ str(consumption)+"  available food: "+ str(available_food))
            return enough_food



    def stress_response(self):
        self._stress_correct()
        if self.stress <= self.stress_responses['reproduce']:
            self.reproduce()
        if self.stress > self.stress_responses['starve']:
            self.starve()
        if self.stress > self.stress_responses['migrate']:
            self.emigrate()

    def starve(self, magnitude=1.0):
        starvation_magnitude = self.population * self.starvation_rate * magnitude
        starvation_quantity = floor(starvation_magnitude) + binomial(1, starvation_magnitude%1)
        if starvation_quantity > self.population:
            starvation_quantity = self.population
        self.population -= starvation_quantity
        if self.verbose:
            print(self.__repr__() +" starving: " + str(starvation_magnitude)+" "+str(starvation_quantity))
        return starvation_quantity

    def emigrate(self, magnitude=1.0):
        emigration_magnitude = self.population * self.emigration_rate * magnitude
        emigration_quantity = floor(emigration_magnitude) + binomial(1, emigration_magnitude%1)
        if emigration_quantity > self.population:
            emigration_quantity = self.population
        self.population -= emigration_quantity
        #TODO self.location.get_neighbors.population += emigration_quantity # TODO pseudcode. Finish this.
        if self.verbose:
            print(self.__repr__() +" emigrating: " + str(emigration_magnitude)+" "+str(emigration_quantity))
        return emigration_quantity


    def reproduce(self, magnitude=1.0):
        growth_magnitude = self.population * self.reproduction_rate * magnitude
        growth_quantity = floor(growth_magnitude) + binomial(1, growth_magnitude%1)
        self.population += growth_quantity
        if self.verbose:
            print(self.__repr__() +" reproducing: " + str(growth_magnitude)+" "+str(growth_quantity))
        return growth_quantity

    def get_depredated(self, magnitude=1, percentage=None):
        """get_depredated docs
        Population experiences predation.
        """
        predation_quantity = 0
        if not percentage:
            predation_quantity = int(magnitude)
        if percentage:
            self.population -= self.population * (1.0-percentage)
            predation_quantity = int(self._zero_correct_pop * percentage)
        self.population -= predation_quantity
        if self.verbose:
            print(self.__repr__() +"Preyed upon: " + str(predation_quantity))
        return predation_quantity



class AnimalBulk(Fauna):
    """Deprecated. See BulkFauna

    AnimalBulk class docs

    The general principle for bulk populations is that there is a continuous population value. This population attempts
    to feed on some target(which may be another animal population, plant, or detritus(eventually). If the population is
    successful in feeding, then stress should decrease; If not stress should increase by a magnitude proportional to
    magnitude of the failure. The stress level should then produce a response than can include reproducing, dying and
    emigrating.

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):

    """
    def __init__(self, population=0.0, reproduction_rate=0.01, starvation_rate=0.02, feeding_rate=0.5, emigration_rate=0.1):
        super().__init__()
        self.population = population
        self.reproduction_rate = reproduction_rate  # Repro rate is essentially the energy conversion rate. (eg 10 lb grass makes 1 lb beef)
        self.starvation_rate = starvation_rate
        self.feeding_rate = feeding_rate
        self.emigration_rate = emigration_rate
        self.ambient_death_rate = 0.05
        self.stress=0.0
        self.cryptocity = 0.0 #                     # Cryptocity rate is how hard a species is to find.(eg a mole may have a cryptocity of 0.8, while a singing bird might be 0.1)
        self.stress_response ={
            'migrate': 0.375,
            'starve': 0.75,
            'reproduce': 0.20
        }

    def _zero_correct_pop(self):
        """_zero_correct_pop docs
        Private method that sets negative population values to zero.

        """
        if self.population < 0.0:
            self.population = 0.0

    def pass_turn(self, target=None, sm=1.0, stress_rate=0.05):
        """pass_turn docs

        """
        starvation_threshold = 0.2 #I guess? tune this.
        food_need_satisfied = self.newfeed(target)
        if (1.0-food_need_satisfied) < starvation_threshold:
            self.stress += stress_rate * (food_need_satisfied-starvation_threshold)
        else:
            self.stress -= stress_rate

        if self.stress > self.stress_response['migrate']*sm:
            self.migrate()
        if self.stress > self.stress_response['starve']*sm:
            self.starve()
        if self.stress < self.stress_response['reproduce']*sm:
            self.reproduce()



    def newfeed(self, target=None):
        """feed docs

        Todo:
            * Be able to feed on multiple prey, and select prey. Either at random, in order of prevalence, or order of
                ease of finding.
            * Eat plants.
            * Eat specific animals.
            * Cause the stuff that is being fed on are different classes, this should probably be a feeding that is
                class specific.

        Args:
            target (beringia.feature.Feature):

        Returns:
            float: The thing that this returns.

        """
        consumption_need = self.population * self.feeding_rate
        consumption = 0.0
        available_food = target.population # * target.availability
        if issubclass(type(target), AnimalBulk):
            consumption = min([available_food, consumption_need])
            target.population -= consumption
            target._zero_correct_pop()
        elif issubclass(type(target), PlantBulk):
            pass
        else:
            food = 1.0

        return min([consumption/consumption_need, 1.0])



    def feed(self, target=None):
        """feed docs

        Todo:
            * Be able to feed on multiple prey, and select prey. Either at random, in order of prevalence, or order of
                ease of finding.
            * Eat plants.
            * Eat specific animals.
            * Cause the stuff that is being fed on are different classes, this should probably be a feeding that is
                class specific.

        Args:
            target (beringia.feature.Feature):

        Returns:
            float: The thing that this returns.

        """
        consumption = self.population * self.feeding_rate

        if issubclass(type(target), AnimalBulk):
            target.population -= consumption
            target._zero_correct_pop()
        elif issubclass(type(target), PlantBulk):
            pass
        else:
            food = 1.0

        if consumption < food:
            self.reproduce()
            return consumption
        elif consumption >= food:
            self.starve()
            return food

    def reproduce(self, multiplier=1.0):
        # TODO look up population growth rate functions.
        self.population += self.population * self.reproduction_rate * multiplier

    def starve(self):
        self.population -= self.population * self.starvation_rate + self.starvation_rate
        self._zero_correct_pop()

    def _ambient_death(self):
        self.population = self.population * (1 - self.ambient_death_rate)
        self._zero_correct_pop()

    def depredation(self, predation_rate):
        """depredation docs

        Args:
            predation_rate:

        """
        pass

    def migrate(self):
        """migrate docs
        """
        pass

    def pass_time(self, target=1.0):
        """pass_time docs

        Todo:
            * Again this maybe has problems with typing and the feed method.

        Args:
            target (float):

        """
        self.feed(target)
        self._ambient_death()


class Invertebrates(AnimalBulk):
    """Invertebrates class docs

    Args:
        population (float):
        reproduction_rate (float):
        starvation_rate (float):
        feeding_rate (float):
        fallout_rate (float):

    """
    def __init__(
            self, population=0.0, reproduction_rate=0.01, starvation_rate=0.25, feeding_rate=0.25,
            fallout_rate=0.001
    ):
        super(Invertebrates, self).__init__(
            population=population, reproduction_rate=reproduction_rate, starvation_rate=starvation_rate,
            feeding_rate=feeding_rate
        )
        self.fallout_rate = fallout_rate

    def fallout(self):
        """fallout docs

        """
        self.population += self.fallout_rate

    def pass_time(self, food=1.0):
        """pass_time docs

        Args:
            food (float):

        """
        self.fallout()
        self.feed(food)
        self._zero_correct_pop()
        self._ambient_death()


class InvertDetritivores(Invertebrates):
    """InvertDetritivores class docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.01):
        super(InvertDetritivores, self).__init__(feeding_rate=feeding_rate)


class InvertHerbivores(Invertebrates):
    """InvertHerbivores class docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.01):
        super(InvertHerbivores, self).__init__(feeding_rate=feeding_rate)


class InvertPredators(Invertebrates):
    """InvertPredators class docs

    Args:
        feeding_rate (float):
        fallout_rate (float):

    """
    def __init__(self, feeding_rate=0.15, fallout_rate=0.0001):
        super(InvertPredators, self).__init__(feeding_rate=feeding_rate, fallout_rate=fallout_rate)





class Vertebrates(AnimalBulk):
    """Vertebrates docs

   Args:
       population (float):
       reproduction_rate (float):
       feeding_rate (float):

   """
    def __init__(self, population=0.0, reproduction_rate=0.01, feeding_rate=0.1):
        super(Vertebrates, self).__init__(
            population=population, reproduction_rate=reproduction_rate, feeding_rate=feeding_rate
        )
        self.starvation_rate = 0.1


class Insectivore(Vertebrates):
    """Insectivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.1):
        super(Insectivore, self).__init__(feeding_rate=feeding_rate)


class SmallHerbivore(Vertebrates):
    """SmallHerbivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.1):
        super(SmallHerbivore, self).__init__(feeding_rate=feeding_rate)


class LargeHerbivore(Vertebrates):
    """LargeHerbivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.2):
        super(LargeHerbivore, self).__init__(feeding_rate=feeding_rate)


class SmallPredator(Vertebrates):
    """SmallPredator docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.2):
        super(SmallPredator, self).__init__(feeding_rate=feeding_rate)


class LargePredator(Vertebrates):
    """LargePredator docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.3):
        super(LargePredator, self).__init__(feeding_rate=feeding_rate)


class MediumOmnivore(Vertebrates):
    """MediumOmnivore docs

    Args:
        feeding_rate (float):

    """
    def __init__(self, feeding_rate=0.25):
        super(MediumOmnivore, self).__init__(feeding_rate=feeding_rate)

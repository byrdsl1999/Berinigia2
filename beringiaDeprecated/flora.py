# -*- coding: utf-8 -*-
"""flora.py

    TODO:
        A set of flora systems with evolving complexity.
            X   System 0:
                A basic system with either plant or no plant, then graduates with some probability.
                This is similar to a basic 'matchstick sim'
            X System 1:
                A system with a set number of levels(as presently exists)
                level 1(grasses) graduates to level 2(small shrubs) to 3(large shrubs) etc.
                graduation will occur either as a random probability, or after a set period of time.
            X System 2:
                A system with one continunous flora variable.
                the variable increases with time.
            X System 3:
                As above with logistic growth function.
            System 4: (in progress)
            As above but with geology interactions
            System 5(see https://en.wikipedia.org/wiki/Ecological_succession#/media/File:Forest_succession_depicted_over_time.png):
                A system with several guilds of plants, with shifting dominance.
                Mechanism is probably going to be some form of inhibtion/facilitation.
            System 6:
                Similar to above with individual plant species as members of guilds.
        Introduce:
            Plant water requirements
            Plant nutrient requirements
            Plant Stress
        This is all based on a temperate forest model. I'd really like to get a nice savannah system working.


.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
from scipy import stats
from math import floor
import numpy as np

from beringia.feature import Feature


class Flora(Feature):
    """
    This is the base flora class, which includes all the functions necessary. This particular version does not work
    well. Instead, use one of the other flora systems.

    Flora is housed within a locale, and keeps track of which species are present and in what quantities.

    """
    def __init__(self):
        super(Feature, self).__init__()
        self.state = 0
        self.on_fire = 0

    def __repr__(self, verbose=False):
        if not verbose:
            return("FloraState: "+str(self.state))
        else:
            return("FloraState: "+str(self.state)+"\nFireState: "+str(self.on_fire)) #TODO change something more specific


    def increment_state(self):
        """increment_state docs

        Returns:
            bool:

        """
        self.state+=1

    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < 0.1:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < 0.1:
            self.on_fire = 1
            return True
        return False

    def burn(self):
        """burn docs

        """
        self.state -= 1
        self.on_fire = 0

    def get_depredated(self, magnitude=0, percentage=None, on=False):
        """get_depredated docs
        Population experiences herbivory.

        TODO: Rework. PS: Actually this may be fine for the base class.
        """
        if on:
            if not percentage:
                self.state -= magnitude
            if percentage:
                self.state = self.state * (1.0-percentage)
            return bool(self.state)
        else:
            return bool(self.state)

class FloraSystem0(Flora):
    """The most basic plant system that tracks simply Plants/No Plants state at each location.
    """

    def __init__(self):
        super(Flora, self).__init__()
        self.state = 0
        self.on_fire = 0
        self.STATE_CONSTANTS = {
            0: {'stateIncreaseProb': 0.20, 'stateDecreaseProb': 0.0, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000},
            1: {'stateIncreaseProb': 0.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0015, 'fireSpreadProb': 0.500},
            -1: {'stateIncreaseProb': 1.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.000,
                 'fireSpreadProb': 0.000}
        }


    def increment_state(self):
        """increment_state docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['stateIncreaseProb']:
            self.state += 1
            return True
        elif roll > 1 - self.STATE_CONSTANTS[self.state]['stateDecreaseProb']:
            self.state -= 1
            return True
        return False


    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['fireStartProb']:
            self.on_fire = 1
            return True
        return False


    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['fireSpreadProb']:
            self.on_fire = 1
            return True
        return False


    def burn(self):
        """burn docs

        """
        self.state = -1
        self.on_fire = 0



class FloraSystem1(Flora):
    """A system that categorizes several increasing states, and increments them forward.
    """
    def __init__(self):
        super(Flora, self).__init__()
        self.state = 0
        self.on_fire = 0
        self.STATE_CONSTANTS = {
            0: {'stateIncreaseProb': 0.20, 'stateDecreaseProb': 0, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000},
            1: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.100},
            2: {'stateIncreaseProb': 0.15, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.200},
            3: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.300},
            4: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.450},
            5: {'stateIncreaseProb': 0.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.700},
            -1: {'stateIncreaseProb': 1.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000}
            }


    def increment_state(self):
        """increment_state docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['stateIncreaseProb']:
            self.state += 1
            return True
        elif roll > 1 - self.STATE_CONSTANTS[self.state]['stateDecreaseProb']:
            self.state -= 1
            return True
        return False


    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['fireStartProb']:
            self.on_fire = 1
            return True
        return False


    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.STATE_CONSTANTS[self.state]['fireSpreadProb']:
            self.on_fire = 1
            return True
        return False


    def burn(self):
        """burn docs

        """
        self.state = -1
        self.on_fire = 0


class FloraSystem2(Flora):
    """
    This flora system increases the population of plants in a roughly linear fashion from [0, 10). Fire probabilities
    scale similarly.

    Flora is housed within a locale, and keeps track of which species are present and in what quantities.

    """

    def __init__(self):
        super(Flora, self).__init__()
        self.state = 0.0  #State exists from 0-9 continuous, but should be rounded for display.
        self.on_fire = 0
        self.random_growth = True
        self.herbivory_active = False

    def increment_state(self, rate = 0.05, max= 9.9999):
        """increment_state docs

        Returns:
            bool:

        """
        if not self.random_growth:
            if self.state < max:
                self.state += rate
                if self.state > max:
                    self.state = max
            else:
                self.state = max
        elif self.random_growth:
            if self.state <= max:
                self.state += np.random.normal(rate, rate/5)
                if self.state > max:
                    self.state = max
            else:
                self.state = max

    def _zero_correct_state(self):
        """_zero_correct_pop docs
        Private method that sets negative state values to zero. Returns False if population is <=0.

        """
        if self.state <= 0.0:
            self.state = 0.0
            return False
        return True

    def risk_fire(self, fire_risk=0.0002):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < fire_risk * self.state:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self, fire_spread_prob= 0.05):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.state * fire_spread_prob:
            self.on_fire = 1
            return True
        return False

    def burn(self, fire_damage= 0.9):
        """burn docs

        """
        self.state = self.state * (1-fire_damage)
        self.on_fire = 0

    def get_depredated(self, magnitude=0.0, percentage=None, on=False):
        """get_depredated docs
        Population experiences herbivory.

        TODO: Rework. PS: Actually this may be fine for the base class.
        """
        if on or self.herbivory_active:
            if not percentage:
                self.state -= magnitude
            if percentage:
                self.state = self.state * (1.0-percentage)
            return self._zero_correct_state()
        else:
            return bool(floor(self.state))

class FloraSystem3(Flora):
    """
    This flora system increases plant mass as a logistic function from (0, 10). Fire probabilities
    scale linearly.

    Flora is housed within a locale, and keeps track of which species are present and in what quantities.

    """

    def __init__(self):
        super(Flora, self).__init__()
        self.state = 0.1  #State exists from (0-10) continuous, but should be rounded for display.
        self.on_fire = 0
        self.random_growth = False

    def increment_state(self, rate = 0.05, max= 9.9999):
        """increment_state docs

        Returns:
            bool:

        """
        self.state += rate * self.state * (1 - self.state/max)


    def risk_fire(self, fire_risk=0.0005):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < fire_risk * self.state:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self, fire_spread_prob= 0.08):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.state * fire_spread_prob:
            self.on_fire = 1
            return True
        return False

    def burn(self, fire_damage= 0.9):
        """burn docs

        """
        self.state = self.state * (1-fire_damage)
        self.on_fire = 0


class FloraSystem4(Flora):
    """
    Flora System 4 is system 3 with geology elements introduced
    In progress....
    """

    def __init__(self):
        super(Flora, self).__init__()
        self.state = 0.1  #State exists from (0-10) continuous, but should be rounded for display.
        self.on_fire = 0
        self.random_growth = False


    def increment_state(self, rate = 0.05, max= 9.9999):
        """increment_state docs

        Returns:
            bool:

        """
        self.state += rate * self.state * (1 - self.state/max)


    def risk_fire(self, fire_risk=0.0005):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < fire_risk * self.state:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self, fire_spread_prob= 0.08):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < self.state * fire_spread_prob:
            self.on_fire = 1
            return True
        return False

    def burn(self, fire_damage= 0.9):
        """burn docs

        """
        self.state = self.state * (1-fire_damage)
        self.on_fire = 0


class PlantBulk(Flora):
    """PlantBulk class docs

    Args:
        population (float):
        growth_rate (float):
        feeding_rate (float):

    """
    def __init__(self, population=0.01, growth_rate=0.01, feeding_rate=0.5):
        super(PlantBulk, self).__init__()
        self.population = population
        self.max_pop = 1.0
        self.growth_rate = growth_rate
        self.moisture_preference = 0.7
        self.moisture_tolerance = 0.2
        self.moisture_function = None
        self.nutrient_preference = None
        self.nutrient_tolerance = None

    def grow(self, environment=None):
        """This invocation of this function will cause the population to increment by one step.

        maths:
            Ecological growth should follow a logistic growth function. The slope of which is defined by the equation:
                dP/dt = r * P * (1 - P/K)

            where P = Population, r = growth rate, and K = carrying capacity.

        Args:
            environment (float):

        """
        self.population += self.growth_rate * self.population * (1 - self.population/self.max_pop)

    def calc_max_pop(self, environment):
        """calc_max_pop docs

        Args:
            environment (float):

        """
        if not environment:
            environment = 1.0

        self.max_pop = self.moisture_function.pdf(environment)

    def _calc_tolerance_functions(self):
        self.moisture_function = stats.norm(self.moisture_preference, self.moisture_tolerance)

    @classmethod
    def _sufficient_nutrients(cls, environment=None):
        if environment:
            return False
        else:
            return True

    @classmethod
    def _sufficient_moisture(cls, environment=None):
        if environment:
            return False
        else:
            return True

# TODO: The following is where I would like to end up, but is iceboxed for now.

class Mosses(PlantBulk):
    """Mosses class docs

    """
    def __init__(self):
        super(Mosses, self).__init__()


class Grasses(PlantBulk):
    """Grasses class docs

    """
    def __init__(self):
        super(Grasses, self).__init__()


class Perennials(PlantBulk):
    """Perennials class docs

    """
    def __init__(self):
        super(Perennials, self).__init__()


class Shrubs(PlantBulk):
    """Shrubs class docs

    """
    def __init__(self):
        super(Shrubs, self).__init__()


class SoftWoods(PlantBulk):
    """SoftWoods class docs

    """
    def __init__(self):
        super(SoftWoods, self).__init__()


class HardWoods(PlantBulk):
    """HardWoods class docs

    """
    def __init__(self):
        super(HardWoods, self).__init__()

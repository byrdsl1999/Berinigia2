# -*- coding: utf-8 -*-
"""localebase.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import numpy as np

from beringia.soil import Geology, BorderGeology
from beringia.constants import STATE_CONSTANTS, FEATURES_SWITCH, PLANT_COLOR_KEY
from beringia.flora import Flora, FloraSystem0, FloraSystem1, FloraSystem2, FloraSystem3, FloraSystem4
from beringia.fauna import BulkFauna, Fauna


from math import floor

class Locale_Deprecated(object):
    """A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self):
        self.state = 0
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.on_fire = 0
        self.flora = FloraSystem0()

        if FEATURES_SWITCH['geology']:
            self.geology = Geology()

    def __str__(self):
        if self.on_fire == 0:
            return PLANT_COLOR_KEY[self.state]
        elif self.on_fire == 1:
            return "\033[1;31mf\033[0;37m"

    def __repr__(self):
        return str(self.state)

    def pass_time(self):
        """pass_time doc

        """
        if self.on_fire == 1:
            self.burn()
        self.increment_state()
        self.risk_fire()

    def increment_state(self):
        """increment_state docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['stateIncreaseProb']:
            self.state += 1
            return True
        elif roll > 1-STATE_CONSTANTS[self.state]['stateDecreaseProb']:
            self.state -= 1
            return True
        return False

    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['fireStartProb']:
            self.on_fire = 1
            return True
        return False

    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        roll = np.random.uniform(0, 1)
        if roll < STATE_CONSTANTS[self.state]['fireSpreadProb']:
            self.on_fire = 1
            return True
        return False

    def burn(self):
        """burn docs

        """
        self.state = -1
        self.on_fire = 0


class Locale(object):
    """
    IN PROGRESS. Same as old locale in function. implements flora object.
    A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self, flora_system = 1, fauna_depth=1, location=None, region=None):
        self.flora = self._flora_switch(flora_system)
        self.flora_system = flora_system
        if FEATURES_SWITCH['geology']:
            self.geology = Geology()
        if FEATURES_SWITCH['fauna']:
            self.fauna = []
            for _ in range(fauna_depth):
                self.insert_fauna()
            self.fauna_set_simple_food_chain()
        self.fauna_depth = fauna_depth
        self.state = self.flora.state
        self.on_fire = self.flora.on_fire
        self.location = location        #should be a region?
        self.region = region
        self.is_border=False

    def __str__(self):
        if self.flora_system == 1:
            if self.on_fire == 0:
                return PLANT_COLOR_KEY[self.state]
            elif self.on_fire == 1:
                return "\033[1;31mf\033[0;37m"
        elif self.flora_system == 2 or self.flora_system == 3:
            if self.on_fire == 0:
                return PLANT_COLOR_KEY[int(floor(self.state))]
            elif self.on_fire == 1:
                return "\033[1;31mf\033[0;37m"

    def __repr__(self):
        return str(self.state)

    def _flora_switch(self, system=1):
        switch={
            0:FloraSystem0(),
            1:FloraSystem1(),
            2:FloraSystem2(),
            3:FloraSystem3(),
            4:FloraSystem4()
        }
        return switch.get(system, FloraSystem1())

    def _update_values(self):
        self.state=int(self.flora.state)
        self.on_fire = self.flora.on_fire

    def insert_fauna(self, new_fauna=None, target=None):
        if target==None:
            pass
        if new_fauna==None:
            new_fauna = BulkFauna(location=self)
        self.fauna.append(new_fauna)

    def remove_single_fauna(self):
        self.fauna.pop()


    def fauna_set_simple_food_chain(self):
        if self.fauna:
            self.fauna[0].prey = self.flora
            for i in range (len(self.fauna)-1):
                self.fauna[i+1].prey = self.fauna[i]
            return True
        return False

    def pass_time(self, ticks=1):
        """pass_time doc

        """
        for i in range(ticks):
            if self.flora.on_fire == 1:
                self.flora.burn()
            self.flora.increment_state()
            self.flora.risk_fire()
            self._update_values()
        if self.fauna:
            for taxa in self.fauna:
                taxa.pass_turn()

    def risk_fire(self):
        """risk_fire docs
        Runs the chance that the locale will catch fire spontaneously. If fire is being spread from another locale, then
        the method 'catch_fire' should be used.

        Rolls to catch fire per the particular flora systems risk_fire method.

        Returns:
            bool: True if locale caught fire, False otherwise.

        """
        self.flora.risk_fire()
        self.on_fire=self.flora.on_fire
        return bool(self.on_fire)

    def catch_fire(self):
        """catch_fire docs
        Runs the chance that the locale will catch fire. This method should be run when fire is being spread from another
        locale. If testing to see if an initial fire starts spontaneously, use the 'risk_fire' method.

        Rolls to catch fire per the particular flora systems risk_fire method.

        Returns:
            bool: True if locale caught fire, False otherwise.

        """
        self.flora.catch_fire()
        self.on_fire = self.flora.on_fire
        return bool(self.on_fire)

    def burn(self):
        """burn docs
        This function causes the locale to experience all the effects of burning. (Damage to flora is the only current
        impact, but others may be implemented.
        """
        self.flora.burn()

class Border(Locale):
    """
    A special case of locale. These locales exist as null locales, that are basically inert in function. They should be
    able to receive input as neceesary(eg accretion), but be unaffected. They should have no output. They are not
    intended to be visualized.

    """
    def __init__(self):
        super(Border, self).__init__()
        self.is_border=True
        if FEATURES_SWITCH['geology']:
            self.geology = BorderGeology()


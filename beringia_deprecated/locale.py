# -*- coding: utf-8 -*-
"""locale.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

    TODO:
        Additional Features:
            Make fire external to region.
        Add edge locales.

"""
import numpy as np

from beringia_deprecated.soil import Geology
from beringia_deprecated.constants import COLOR_KEY, STATE_CONSTANTS, FEATURES_SWITCH


class Locale(object):
    """A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self):
        self.state = 0
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.on_fire = 0

        if FEATURES_SWITCH['geology']:
            self.geology = Geology()

    def __str__(self):
        if self.on_fire == 0:
            return COLOR_KEY[self.state]
        elif self.on_fire == 1:
            return '\033[1;31mf\033[0;37m'

    def __repr__(self):
        return str(self.state)

    def pass_time(self):
        """pass_time docs

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


class Border(Locale):
    def __init__(self):
        super(Border, self).__init__()
        self.is_border=True



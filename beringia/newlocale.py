# -*- coding: utf-8 -*-
"""localebase.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
#import numpy as np
import simpy as sp

from beringia.soil import Geology, BorderGeology
from beringia.constants import STATE_CONSTANTS, FEATURES_SWITCH, PLANT_COLOR_KEY
from beringia.flora import FloraSystem0, FloraSystem1, FloraSystem2, FloraSystem3

class Locale(object):
    """
    IN PROGRESS. Same as old locale in function. implements flora object.
    A locale is conceptually a small region which contains a number of biotic and abiotic features which simulate
    a local ecosystem. It has been conceived of initially as a patch of land about 1 acre in size.

    """
    def __init__(self, flora_system = 1):
        self.flora = self._flora_switch(flora_system)
        if FEATURES_SWITCH['geology']:
            self.geology = Geology()
        self.state = self.flora.state
        self.on_fire = self.flora.on_fire

    def __str__(self):
        if self.on_fire == 0:
            return PLANT_COLOR_KEY[self.state]
        elif self.on_fire == 1:
            return "\033[1;31mf\033[0;37m"

    def __repr__(self):
        return str(self.state)

    def _flora_switch(self, system=1):
        switch={
            0:FloraSystem0(),
            1:FloraSystem1(),
            2:FloraSystem2(),
            3:FloraSystem3()
        }
        return switch.get(system, FloraSystem1())

    def _update_values(self):
        self.state=int(self.flora.state)
        self.on_fire = self.flora.on_fire

    def pass_time(self, ticks=1):
        """pass_time doc

        """
        for i in range(ticks):
            if self.flora.on_fire == 1:
                self.flora.burn()
            self.flora.increment_state()
            self.flora.risk_fire()
            self._update_values()

    def risk_fire(self):
        """risk_fire docs

        Returns:
            bool:

        """
        self.flora.risk_fire()

    def catch_fire(self):
        """catch_fire docs

        Returns:
            bool:

        """
        return self.flora.catch_fire()

    def burn(self):
        """burn docs

        """
        self.flora.burn()

class Border(Locale):
    def __init__(self):
        super(Border, self).__init__()
        self.is_border=True
        if FEATURES_SWITCH['geology']:
            self.geology = BorderGeology()

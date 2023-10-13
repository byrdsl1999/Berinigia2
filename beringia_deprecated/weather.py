# -*- coding: utf-8 -*-
"""weather.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import math

import numpy

from beringia_deprecated.feature import Feature


class Weather(Feature):
    """Weather class docs

    Args:
        periodicity (int):

    """
    def __init__(self, periodicity=12):
        super(Weather, self).__init__()
        self.periodicity = periodicity
        self.rain_base = 0.5
        self.rain_boost = 0.5
        self.rain_wet_season_offset = 6
        self.rain_variance = 1.0
        self.sunlight_base = 1.0
        self.sunlight_boost = 0.5
        self.sunlight_offset = 0
        self.sunlight_variance = 1.0

    def rain(self, time=0):
        """rain docs

        Args:
            time (int):

        Returns:
            float:

        """
        seasonal_variation = math.sin(2*math.pi*(time+self.rain_wet_season_offset)/self.periodicity)
        rain_noise = numpy.random.lognormal(-3, self.rain_variance)
        rain_fall = seasonal_variation + rain_noise + self.rain_base
        return rain_fall

    def sunlight(self, time=0):
        """sunlight docs

        Args:
            time (int):

        Returns:
            float:

        """
        seasonal_variation = math.sin(2*math.pi*(time+self.sunlight_offset)/self.periodicity)
        sunlight_noise = numpy.random.lognormal(-3, self.sunlight_variance)
        sunlight = seasonal_variation + sunlight_noise + self.sunlight_base
        return sunlight

    def temp(self, time=0):
        pass

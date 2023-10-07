# -*- coding: utf-8 -*-
"""soil.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Todo:
    * rocks
        surface rocks(decrease growing surface area, but increase precipitation penetration
    * Soil Quality
        Sand/Loam/Clay
        organic matter
    * soil depth X
        erosion X
        accumulation X
        Plants reducing soil erosion
    * soil moisture
    * elevation X
    * hydrology
        standing water
        evaporation
        flow
        erosion

"""
import numpy as np
from feature import Feature



class Geology(Feature):
    """Geology class docs

    Args:
        elevation_base (float):
        soil_depth (float):
        soil_moisture (float):

    """
    def __init__(
        self, elevation_base=np.random.gamma(5, 0.5), soil_depth=np.random.lognormal(0.25, 0), soil_moisture=0.5
    ):
        self.elevation_base = elevation_base
        self.soil_depth = soil_depth
        self.elevation = self._elevation()
        #self.water_content = self.soil_depth * self.soil_moisture
        self.hydrology = Hydrology(water_content= soil_moisture*soil_depth, water_capacity=soil_depth)
        self.soil_moisture = self.hydrology.water_content/self.hydrology.water_capacity
        self.soil_stability = 0.0
        self.basin_elevation = self.elevation   #If a locale is part of a basin, this value is equal to the height of the lowest point constraining the basin(ie, where water would flow out if you filled up the basin.).
        self.outflow_target = None
        self.is_in_basin = False
        self.is_local_minimum = False
        self.aspect = self._calculate_aspect()

    def recalculate_values(self):
        """recalculate_values docs

        """
        self.elevation = self.elevation_base+self.soil_depth
        self.soil_moisture = self.hydrology.water_content/self.hydrology.water_capacity

    def _elevation(self):
        return self.elevation_base+self.soil_depth

    def set_basin_elevation(self, elevation = None):
        if not elevation: elevation = self.elevation
        self.basin_elevation = elevation

    def set_is_in_basin(self, is_in=False):
        self.is_in_basin = is_in

    def get_basin_depth(self):
        if self.is_in_basin:
            return self.basin_elevation - self.elevation
        else:
            0.0



    def _calculate_aspect(self, north_elev=None, south_elev=None, east_elev=None, west_elev=None):
        """Calculate the slope aspect(direction).

        Returns a tuple of north-south and east-west aspect. Positive values represent downward slopes to the north and
        east respectively. Negative values represent slopes to the south and west.

        Units are currently ambiguous. Perhaps % grade.

        """
        if not north_elev:
            north_elev = float(self.elevation)
        if not south_elev:
            south_elev = float(self.elevation)
        if not east_elev:
            east_elev = float(self.elevation)
        if not west_elev:
            west_elev = float(self.elevation)
        self.aspect = (south_elev - north_elev, west_elev - east_elev)
        return (south_elev - north_elev, west_elev - east_elev)

    def erode(self, magnitude=1.0, rate=0.01, slope=0.1, soil_stability=None):
        """erode docs

        Args:
            magnitude (float): The strength of the erosion event(eg large amount vs small amount of rainfall)
            rate (float): A constant for tuning, and timestep size adjustment.
            slope (float): The difference in elevation between two neighboring locales.
            soil_stability (float): The locale's resistance to erosion, reflecting plant presence or other attributes.

        Returns:
            float:

        """
        if not soil_stability: soil_stability = self.soil_stability
        load = magnitude * rate * slope * (1-soil_stability)
        transport = 0.0
        if load > self.soil_depth:
            transport += self.soil_depth
            self.soil_depth = 0
            self.soil_depth += (load-self.soil_depth) * rate
            self.elevation_base -= (load-self.soil_depth) * rate
        else:
            transport += load
            self.soil_depth -= load
        self.recalculate_values()
        return transport

    def accrete(self, load):
        """accrete docs

        Args:
            load (float):

        """
        self.soil_depth += load
        self.recalculate_values()

    def water_input(self, amount):
        excess = self.hydrology.accumulate_water(amount)


    def runoff(self):
        """runoff docs

        """
        pass

class Hydrology(object):
    """Hydrology class docs
    Conceptually we should note that the standard unit for water implemented here is the acre-foot.
    Args:
        water_content (float):
        water_capacity (float):
    """
    def __init__(
            self, water_content=0.5, water_capacity=1.0
    ):
        self.water_content = water_content
        self.water_capacity = water_capacity
        self.water_depth = 0.0
        self.water_elevation = 0.0
        self.max_water_depth=0.0

    def update_capacity(self, new_value):
        self.water_capacity = new_value

    def accumulate_water(self, water_input):
        self.water_content += water_input
        if self.water_content > self.water_capacity:
            return self.handle_excess_water()

    def handle_excess_water(self, outflow=True):
        if outflow:
            return self.runoff()
        else:
            self.standing_water()

    def runoff(self):
        return self.water_content - self.water_capacity

    def standing_water(self, amount):
        self.water_depth += amount

class BorderGeology(Geology):
    """BorderGeology class docs

    This is meant to be a basically non-functional Geology object that will basically sit there inert.

    Args:
        elevation_base (float):
        soil_depth (float):
        soil_moisture (float):

    """
    def __init__(self):
        super(BorderGeology, self).__init__()

    def recalculate_values(self):
        """recalculate_values docs

        """
        self.elevation = self.elevation_base+self.soil_depth
        self.soil_moisture = self.hydrology.water_content/self.hydrology.water_capacity

    def _elevation(self):
        return self.elevation_base+self.soil_depth

    def set_basin_elevation(self, elevation = None):
        if not elevation: elevation = self.elevation
        self.basin_elevation = elevation

    def erode(self, magnitude=0.0, rate=0.00, slope=0.0, soil_stability=None):
        """erode docs

        Args:
            magnitude (float): The strength of the erosion event(eg large amount vs small amount of rainfall)
            rate (float): A constant for tuning, and timestep size adjustment.
            slope (float): The difference in elevation between two neighboring locales.
            soil_stability (float): The locale's resistance to erosion, reflecting plant presence or other attributes.

        Returns:
            float:

        """
        return 0.0

    def accrete(self, load):
        """accrete docs

        Args:
            load (float):

        """
        pass

    def water_input(self, amount):
        pass


    def runoff(self):
        """runoff docs

        """
        pass
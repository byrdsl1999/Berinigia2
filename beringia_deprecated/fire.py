# -*- coding: utf-8 -*-
"""fire.py

This file is deprecated.

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import time

import numpy as np
import networkx as nx

from beringia_deprecated.constants import STATE_CONSTANTS, COLOR_KEY


class MXRegion(object):
    """MXRegion class docs

    Args:
        xdim (int):
        ydim (int):
        grid_type (str):
        colorize (bool):

    """
    def __init__(self, xdim=10, ydim=10, grid_type='2d', colorize=True):
        self.xdim = xdim
        self.ydim = ydim
        self.grid_type = grid_type
        if grid_type == '2d':
            self.space = nx.grid_2d_graph(xdim, ydim)
        elif grid_type == 'hex':
            self.space = nx.hexagonal_lattice_graph(xdim, ydim)
        elif grid_type == 'tri':
            self.space = nx.triangular_lattice_graph(xdim, ydim)
        else:
            # TODO: raise exception? default to 2d?
            self.space = nx.grid_2d_graph(xdim, ydim)
        for node in self.space.nodes:
            self.space.node[node]['locale'] = Locale()
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.time = 0
        self.colorize = colorize

    def __repr__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'NXRegion {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def __str__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'NXRegion {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def show_map(self, do_print=True):
        """show_map docs

        Args:
            do_print (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale(x, y))
                out += '\n'
            out += '\r'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fire_map(self, do_print=True):
        """Display a visual representation of the self.space attribute with fire state layered on if do_print.

        Args:
            do_print (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale(x, y, fire_state=True))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def pass_time(self, count=1):
        """Move forward one time (or count # of) step(s).

        Args:
            count (int):

        """
        for _ in range(count):
            self.time += 1
            for node in self.space.nodes:
                self.space.node[node]['locale'].pass_time()
            self.spread_fire()

    def show_turns(self, count=1, pause=0.5):
        """show_turns docs

        Args:
            count (int):
            pause (float):

        """
        for _ in range(count):
            self.pass_time()
            self.show_map()
            time.sleep(pause)

    def spread_fire(self, slow_burn=False):
        """Scan locales for fire, and if present, cause fire to spread to neighboring regions.

        Todo:
            * add locales_to_burn
        Args:
            slow_burn (bool):

        """
        locales_on_fire = []
        fires_present = False
        for node in self.space.nodes:
            if self.space.node[node]['locale'].on_fire == 1:
                locales_on_fire.append(node)
        if locales_on_fire:
            fires_present = True
        for locale_ in locales_on_fire:
            neighboring_nodes = self.space.neighbors(locale_)
            for node in neighboring_nodes:
                if self.space.node[node]['locale'].on_fire == 0:
                    if self.space.node[node]['locale'].catch_fire():
                        locales_on_fire.append(node)
                        if slow_burn:
                            self.show_map()
                            time.sleep(0.15)
        if fires_present:
            self.show_map()
            time.sleep(0.5)

    def view_locale(self, x, y, fire_state=False):
        """view_locale docs

        Args:
            x (int):
            y (int):
            fire_state (bool):

        Returns:
            beringia.locale.Locale:

        """
        if fire_state:
            return self.space.node[(x, y)]['locale'].on_fire
        else:
            return self.space.node[(x, y)]['locale']


class Region(object):
    """Region class docs

    Args:
        xdim (int):
        ydim (int):

    """
    def __init__(self, xdim=10, ydim=10):
        self.xdim = xdim
        self.ydim = ydim
        self.space = [[Locale() for x in range(self.xdim)] for y in range(self.ydim)]
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.time = 0

    def __repr__(self):
        out = ''
        for line in self.space:
            for item in line:
                out += str(item)
            out += '\n'
        return out

    def __str__(self):
        out = ''
        for line in self.space:
            for item in line:
                out += str(item)
            out += '\n'
        return out

    def show_fire_map(self, do_print=True):
        """show_fire_map docs

        Args:
            do_print (bool):

        Returns:
            str:

        """
        out = ''
        for line in self.space:
            for item in line:
                out += str(item.on_fire)
            out += '\n'
        if do_print:
            print(out)
        else:
            return out

    def pass_time(self, count=1):
        """pass_time docs

        Args:
            count (int):

        """
        for _ in range(count):
            self.time += 1
            for line in self.space:
                for each_locale in line:
                    each_locale.pass_time()
            self.spread_fire()

    def spread_fire(self):
        """spread_fire docs

        Todo:
            * add locales_to_burn

        """
        locales_on_fire = []
        for x in range(self.xdim):
            for y in range(self.ydim):
                if self.space[x][y].on_fire == 1:
                    locales_on_fire.append([x, y])

        for locale_ in locales_on_fire:
            if locale_[0]-1 >= 0 and self.space[locale_[0]-1][locale_[1]].on_fire == 0:
                if self.space[locale_[0]-1][locale_[1]].catch_fire():
                    locales_on_fire.append([locale_[0]-1, locale_[1]])
            if locale_[0]+1 < self.xdim and self.space[locale_[0]+1][locale_[1]].on_fire == 0:
                if self.space[locale_[0]+1][locale_[1]].catch_fire():
                    locales_on_fire.append([locale_[0]+1, locale_[1]])
            if locale_[1]-1 >= 0 and self.space[locale_[0]][locale_[1]-1].on_fire == 0:
                if self.space[locale_[0]][locale_[1]-1].catch_fire():
                    locales_on_fire.append([locale_[0], locale_[1]-1])
            if locale_[1]+1 < self.ydim and self.space[locale_[0]][locale_[1]+1].on_fire == 0:
                if self.space[locale_[0]][locale_[1]+1].catch_fire():
                    locales_on_fire.append([locale_[0]-1, locale_[1]+1])


class Locale(object):
    """Locale class docs

    """
    def __init__(self):
        self.state = 0
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.on_fire = 0

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
        elif roll > 1 - STATE_CONSTANTS[self.state]['stateDecreaseProb']:
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


class Species(object):
    """Species class docs

    """
    def __init__(self):
        pass


class ABiotics(object):
    """ABiotics class docs

    Args:
        soil (float):
        bedrock (float):
        moisture (float):
        nutrients (float):

    """
    def __init__(self, soil=1.0, bedrock=1.0, moisture=1.0, nutrients=1.0):
        super(ABiotics, self).__init__()
        self.soil = soil
        self.bedrock = bedrock
        self.moisture = moisture
        self.nutrients = nutrients

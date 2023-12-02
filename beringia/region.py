# -*- coding: utf-8 -*-
"""region.py

The region object should be tasked with all inter locale interactions. These might include fire spreading, and locales
eroding from ones locale to another. Locales should be able to handle all their actions on their own, but return any
relevant info that the interation requires.

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import time
#import simpy as sp

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from math import floor

from .Microhabitat import Microhabitat, NullMicrohabitat
from .PlantSpeciesLibrary import PlantSpeciesLibrary
from .PlantSpeciesFactory import PlantSpeciesFactory
from .PlantFactory import PlantFactory

from .constants import STATE_CONSTANTS, PLANT_COLOR_KEY, GRAYSCALE_COLOR_KEY

class Region(object):
    """Region class docs

        xdim (int):
        ydim (int):
        grid_type (str):
        colorize (bool):

    """
    def __init__(self, xdim: int = 10, ydim: int = 10, grid_type: str = '2d', flora_system: int = 1, colorize: bool = True, edges: bool = True, slow_burn: bool = False):
        self.xdim = xdim
        self.ydim = ydim
        self.grid_type = grid_type
        if grid_type == '2d':
            self.space = nx.grid_2d_graph(self.xdim, ydim)
        elif grid_type == 'hex':
            self.space = nx.hexagonal_lattice_graph(self.xdim, ydim)
        elif grid_type == 'tri':
            self.space = nx.triangular_lattice_graph(self.xdim, ydim)
        else:
            # TODO: raise exception? default to 2d?
            self.space = nx.grid_2d_graph(self.xdim, ydim)
        self.conversion_rates = {0: 0.2, 1: 0.1, 2: 0.15, 3: 0.05, 4: 0.1, 5: 0}
        self.time = 0
        self.colorize = colorize
        self.slow_burn = slow_burn
        self.constants = STATE_CONSTANTS
        self.verbose = False
        self.basins_current=False
        
        self.plantSpeciesLibrary = PlantSpeciesLibrary()
        self.plantSpeciesFactory = PlantSpeciesFactory(self.plantSpeciesLibrary)
        self.plantFactory = PlantFactory(self.plantSpeciesLibrary)
        
        self.nodeValues = dict()
        for node in self.space.nodes:
            #self.space.nodes[node]['locale'] = Locale(flora_system=flora_system, location=node, region=self)
            self.space.nodes[node]['locale'] = Microhabitat(size=100, pf = self.plantFactory, psl = self.plantSpeciesLibrary)
            self.nodeValues[node] = self.space.nodes[node]


        self.nodes = set([node for node in self.space.nodes])
        if edges:
            self._add_border_nodes()



    #def _scheduler(self):
    #    self.time_env = sp.Environment()


    def __repr__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def __str__(self, verbose=False):
        if not verbose or self.grid_type != '2d':
            return f'region {self.xdim}x{self.ydim}'
        else:
            out = ''
            for x in range(self.xdim):
                for y in range(self.ydim):
                    out += str(self.view_locale())
                out += '\n'
            return out

    def _add_border_nodes(self):
        """"
        Presently border nodes are going to copy the properties of their neighboring nodes.
        :return:
        """
        self.border_nodes = set()
        for i in range(self.xdim):
            self.space.add_node((i, -1))
            self.space.add_edge((i, -1), (i, 0))
            self.border_nodes.add((i, -1))
            self.space.add_node((i, self.ydim))
            self.space.add_edge((i, self.ydim), (i, self.ydim - 1))
            self.border_nodes.add((i, self.ydim))
        for j in range(self.ydim):
            self.space.add_node((-1, j))
            self.space.add_edge((-1, j), (0, j))
            self.border_nodes.add((-1, j))
            self.space.add_node((self.xdim, j))
            self.space.add_edge((self.xdim, j), (self.xdim - 1, j))
            self.border_nodes.add((self.xdim, j))
        for node in self.border_nodes:
            self.space.nodes[node]['locale'] = NullMicrohabitat(size=0, pf = self.plantFactory, psl = self.plantSpeciesLibrary)
            neighbor=[i for i in nx.neighbors(self.space, node)][0]
            self.space.nodes[node]['locale'].geology.elevation_base = self.space.nodes[neighbor]['locale'].geology.elevation_base
            self.space.nodes[node]['locale'].geology.soil_depth = self.space.nodes[neighbor]['locale'].geology.soil_depth
            self.space.nodes[node]['locale'].geology.elevation = self.space.nodes[neighbor]['locale'].geology.elevation


    def show_map(self, do_print=True, show_fire=True, colorize=True):
        """show_map docs

        Args:
            do_print (bool): T/F, should the output be printed(T), or returned as an array(F).
            show_fire (bool):
            colorize (bool):

        Returns:
            str:

        """
        if self.grid_type == '2d':
            if do_print:
                out = ''
                for y in range(self.ydim):
                    for x in range(self.xdim):
                        if self.get_locale(x,y).on_fire == 1 and show_fire:
                            if colorize:
                                out += "\033[1;31mf\033[0;37m"
                            else:
                                out += "f"
                        else:
                            out += str(self.view_locale(x, y, colorize=colorize))
                    out += '\n'
                out += '\r'
                print(out)
            elif not do_print:
                out = ''
                for y in range(self.ydim):
                    for x in range(self.xdim):
                        if self.get_locale(x,y).on_fire == 1 and show_fire:
                            out += "f"
                        else:
                            out += str(self.view_locale(x, y, colorize=colorize))
                    out += '\n'
                out += '\r'
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fire_map(self, do_print=True):
        """Display a visual representation of the self.space attribute with fire state layered on if doPrint.

        Args:
            do_print (bool): T/F, should the output be printed(T), or returned as an array(F).

        Returns:
             str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_locale(x, y, fire_state=True))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_elevation_map(self, do_print=True):
        """show_elevation_map docs

        Args:
            do_print (bool): T/F, should the output be printed(T), or returned as an array(F).

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_elevation(x, y, colorize= True))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def show_fauna_map(self, do_print=True, index=0):
        """show_fauna_map docs

        Args:
            do_print (bool): T/F, should the output be printed(T), or returned as an array(F).
            index (int): The index of which fauna should be displayed/returned.

        Returns:
            str:

        """
        if self.grid_type == '2d':
            out = ''
            for y in range(self.ydim):
                for x in range(self.xdim):
                    out += str(self.view_fauna_pop(x, y, index, colorize=True, ceiling=10.0))
                out += '\n'
            if do_print:
                print(out)
            else:
                return out
        else:
            print('!!! This grid type does not have this feature implemented !!!')

    def get_map_array(self, kind="flora", index=0):
        if self.grid_type != '2d':
            print("Grid type:", self.grid_type, " not supported.")
            return None
        elif self.grid_type == '2d':
            grid = np.zeros((self.xdim, self.ydim))
            for i in range(self.xdim):
                for j in range(self.ydim):
                    if kind == "flora":
                        grid[i, j]=self.get_locale(i, j).state
                    elif kind == "fauna":
                        grid[i, j] = self.get_locale(i, j).fauna[index].population*100
                    elif kind == "elev" or kind == "elevation":
                        grid[i, j] = self.get_locale(i, j).geology.elevation
                    else:
                        grid[i, j]=self.get_locale(i, j).state
                        print("Map type error. Returning default.")  #How should I be handling this?
            return grid

    def show_heat_map(self, kind="flora"):
        array = self.get_map_array(kind)
        plt.imshow(array, cmap="YlGn")
        plt.colorbar()
        plt.show()

    def pass_time(self, count=1, show_heat_map=False):
        """Move forward one time(or count # of) step(s).

        Args:
            count (int):

        """
        if not show_heat_map or count > 50:
            if show_heat_map: print("Count too high. Display hidden")
            for _ in range(count):
                self.time += 1
                for node in self.nodes:
                    self.space.nodes[node]['locale'].pass_time()
                self.spread_fire(show=False)
                self.erode_all(magnitude=0.1)
        if show_heat_map:
            array = self.get_map_array("flora")
            plt.imshow(array, cmap="YlGn")
            plt.colorbar()
            for _ in range(count):
                self.time += 1
                for node in self.nodes:
                    self.space.nodes[node]['locale'].pass_time()
                self.spread_fire(show=False)
                self.erode_all(magnitude=0.1)

                array = self.get_map_array("flora")
                plt.imshow(array, cmap="YlGn")
                plt.draw()
                plt.pause(0.1)

    def show_turns(self, count=1, pause=0.25):
        for _ in range(count):
            self.pass_time()
            self.show_map()
            time.sleep(pause)
            
    def spread_fire_new(self, verbose: bool = False, pause: float = 0.15, show: bool = True):
        locales_on_fire: list[tuple] = self.scan_for_fire(verbose=verbose)
        burnt_locales: set[tuple] = set()
        
        


    def spread_fire(self, verbose=False, pause=0.15, show=True):
        """Scan locales for fire, and if present, cause fire to spread to neighboring regions.

        Todo:
            * add locales_to_burn

        Args:
            slow_burn (bool):

        """
        locales_on_fire = self.scan_for_fire(verbose=verbose)
        for locale_ in locales_on_fire:
            fires_present = True
            neighboring_nodes = self.space.neighbors(locale_)
            if verbose: print("Fire is burning at:", locale_)
            for node in neighboring_nodes:

                if self.space.nodes[node]['locale'].on_fire == 0:
                    # TODO: check probability of spreading fire between nodes.
                    if self.space.nodes[node]['locale'].runDisturbance():
                        locales_on_fire.append(node)

                        if verbose: print("Fire has spread to:", locale_)

                        if self.slow_burn and show:
                            self.show_map()
                            time.sleep(0.02)
        if locales_on_fire and not self.slow_burn and show:
            self.show_map()
            time.sleep(pause*2)
        self.end_fire()

    def scan_for_fire(self, verbose=False):
        locales_on_fire = []
        for node in self.nodes:
            if self.space.nodes[node]['locale'].on_fire == 1:
                locales_on_fire.append(node)
        if verbose: print("Locales initially on fire:", locales_on_fire)
        if locales_on_fire:
            if verbose: print("Fire is present.")
        return locales_on_fire
    
    def end_fire(self):
        for node in self.nodes:
            self.space.nodes[node]['locale'].on_fire == 0
        return True

    def transfer_fire(self, source, target):
        pass

    def insert_new_fauna(self, new_fauna=None, target=None, all_locales=True, target_locale=None, simple_food_chain=True):
        """insert_new_fauna docs

        Args:
            new_fauna (fauna):
            target (feature, or other):
            all_locales (bool):
            target_locale (Locale):
            simple_food_chain (bool)

        Returns:
            (bool): T/F success/failure

        """
        if all_locales:
            for node in self.nodes:
                if simple_food_chain:
                    self.space.nodes[node]['locale'].insert_fauna(new_fauna)
                    self.space.nodes[node]['locale'].fauna_set_simple_food_chain()
                else:
                    self.space.nodes[node]['locale'].insert_fauna(new_fauna, target)
            return True
        elif target_locale:
            if simple_food_chain:
                self.space.nodes[target_locale]['locale'].insert_fauna(new_fauna)
                self.space.nodes[target_locale]['locale'].fauna_set_simple_food_chain()
            else:
                self.space.nodes[target_locale]['locale'].insert_fauna(new_fauna, target)
            return True
        else:
            print("No target locale specified")
            return False

    def view_locale(self, x=0, y=0, fire_state=False, colorize=True):
        """view_locale docs

        Args:
            x (int):
            y (int):
            fire_state (bool):
            colorize (bool):

        Returns:
            beringia.locale.Locale:

        """
        if fire_state:
            return self.space.nodes[(x, y)]['locale'].on_fire
        else:
            if colorize:
                return PLANT_COLOR_KEY[int(floor(self.space.nodes[(x, y)]['locale'].medianCompetitiveness))]
            else:
                return int(floor(self.space.nodes[(x, y)]['locale'].medianCompetitiveness))

    def view_elevation(self, x=0, y=0, colorize=False):
        """view_elevation docs

        Args:
            x (int):
            y (int):
            colorize(bool)

        Returns:
            int:

        """
        if colorize:
            return GRAYSCALE_COLOR_KEY[int(self.space.nodes[(x, y)]['locale'].geology.elevation//1)]
        else:
            return self.space.nodes[(x, y)]['locale'].geology.elevation

    def view_fauna_pop(self, x=0, y=0, index=0, colorize=False, scale_factor=1.0, ceiling=100.0):
        """view_elevation docs

        Args:
            x (int): locale x dim.
            y (int): locale y dim.
            index (int): which fauna element to return. default is the first.
            colorize(bool): whether or not to return output with ascii colorization.

        Returns:
            int: May have ascii colorization.

        """
        if self.space.nodes[(x, y)]['locale'].fauna:
            if colorize:
                return GRAYSCALE_COLOR_KEY[min(ceiling, (int(self.space.nodes[(x, y)]['locale'].fauna[index].population * scale_factor //1)))]
            else:
                return int(self.space.nodes[(x, y)]['locale'].fauna[index].population * scale_factor //1)

    def erode_one(self, node, magnitude=1.0, rate=0.01):
        """This will cause erosion to occur at one location.

        Args:
            node (networkx.Graph.nodes):
            magnitude (float):
            rate (float):

        """
        neighboring_nodes = self.space.neighbors(node)
        lowest_neighbor = node
        for eachNode in neighboring_nodes:
            if self.space.nodes[lowest_neighbor]['locale'].geology.elevation > self.space.nodes[eachNode]['locale'].geology.elevation:
                lowest_neighbor = eachNode

        if lowest_neighbor != node:
            slope = (self.space.nodes[node]['locale'].geology.elevation
                     - self.space.nodes[lowest_neighbor]['locale'].geology.elevation)
        else:
            slope = 0.01
        transport = self.space.nodes[node]['locale'].geology.erode(magnitude, rate, slope)
        self.space.nodes[lowest_neighbor]['locale'].geology.accrete(transport)

        self.basins_current=False

    def erode_all(self, magnitude=1.0, rate=0.01):
        """erode_all docs

        Args:
            magnitude (float):
            rate (float):

        """
        for node in self.nodes:
            self.erode_one(node, magnitude, rate)

    def calculate_aspect(self):
        if self.grid_type == '2d':
            for y in range(self.ydim):
                for x in range(self.xdim):

                    if y == 0:
                        north = self.view_elevation(x,y, colorize=False)
                    else:
                        north = self.view_elevation(x, y-1, colorize=False)

                    if y == self.ydim:
                        south = self.view_elevation(x, y, colorize=False)
                    else:
                        south = self.view_elevation(x, y+1, colorize=False)

                    if x == 0:
                        east = self.view_elevation(x,y, colorize=False)
                    else:
                        east = self.view_elevation(x-1, y, colorize=False)

                    if x == self.xdim:
                        west = self.view_elevation(x,y, colorize=False)
                    else:
                        west = self.view_elevation(x+1, y, colorize=False)

                    print(north, south, east, west)
                    self.space.nodes[(x, y)]['locale'].geology._calculate_aspect(north, south, east, west)

    def randomize_elevation_base(self, mean=5, sd=1.5):
        """randomize_elevation_base docs

        Args:
            mean (int):
            sd (float):

        """
        for node in self.nodes:
            self.space.nodes[node]['locale'].geology.elevation_base = np.random.normal(mean, sd)
            self.space.nodes[node]['locale'].geology.recalculate_values()

    def randomize_elevation_base_cov(self, mean=5, cov=0.4):
        """randomize_elevation_base_cov docs

        Args:
            mean (int):
            cov (float):

        """
        adj_mat = nx.adjacency_matrix(self.space).todense()
        means = [mean for _ in range(self.xdim * self.ydim)]
        elevations = np.random.multivariate_normal(means, (adj_mat*cov))
        for node in enumerate(self.nodes):
            self.space.nodes[node[1]]['locale'].geology.elevation_base = elevations[node[0]]

    def find_basins(self):
        """Find all the basins in the region and update the locales with the elevation of the point of outflow for the
        basin.
        TODO: Maybe we should track all the basins, and then populate them with fish!
        """
        heightMap = self.get_map_array('elev')
        h = []

        row_l = self.xdim
        col_l = self.ydim

        visited = set()

        for i in range(row_l):
            heapq.heappush(h, (heightMap[i][0], i, 0))
            heapq.heappush(h, (heightMap[i][col_l - 1], i, col_l - 1))
            visited.add((i, 0))
            visited.add((i, col_l - 1))
        for j in range(col_l):
            heapq.heappush(h, (heightMap[0][j], 0, j))
            heapq.heappush(h, (heightMap[row_l - 1][j], row_l - 1, j))
            visited.add((0, j))
            visited.add((row_l - 1, j))

        total = 0
        maxi = float('-inf')

        while len(h) > 0:
            height, row, col = heapq.heappop(h)

            maxi = max(maxi, height)

            for dir in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                row1 = row + dir[0]
                col1 = col + dir[1]

                if 0 <= row1 < row_l and 0 <= col1 < col_l and (row1, col1) not in visited:
                    if maxi > heightMap[row1][col1]:
                        self.get_locale(row1, col1).geology.set_is_in_basin(True)
                        self.get_locale(row1, col1).geology.set_basin_elevation(maxi)
                        # TODO determine if local minimum.
                        total += (maxi - heightMap[row1][col1])
                    else:
                        self.get_locale(row1, col1).geology.set_is_in_basin(False)
                        self.get_locale(row1, col1).geology.set_basin_elevation(
                            self.get_locale(row1, col1).geology.elevation)
                    heapq.heappush(h, (heightMap[row1][col1], row1, col1))
                    visited.add((row1, col1))
                    if self.verbose: print(row1, col1, (maxi - heightMap[row1][col1]))

        return bool(total)

    def get_basins(self):
        if not self.basins_current:
            self.find_basins()
        basins=[]
        for y in range(self.ydim):
            for x in range(self.xdim):
                if self.get_locale(x,y).geology.is_in_basin:
                    basins.append(self.get_locale(x,y))
        return basins


    def get_locale(self, x=0, y=0):
        if x> self.xdim or y>self.ydim or x <0 or y <0:
            print("Value out of range.")
            return None
        else:
            return self.space.nodes[(x,y)]['locale']

    def get_neighbors(self, x=0, y=0, depth=1, tiered=False, ids=False, borders=False):
        if x > self.xdim or y > self.ydim or x < 0 or y < 0:
            if self.verbose:
                print("Value out of range.")
            return None
        else:
            explored = set()
            neighbors = []
            new_queue = [self.get_locale(x,y).location]
            for _ in range(depth):
                queue = new_queue
                new_queue = []
                if tiered:
                    tier = []
                for node in queue:
                    if (node[0] < 0 or node[0] > self.xdim or node[1] < 0 or node[1] > self.ydim) and borders is False:
                        pass
                    else:
                        if node not in explored:
                            neighbs = self.space.neighbors(node)
                            neighbs = [n for n in neighbs if n not in explored]     # removing duplicates.
                            if not borders:
                                neighbs = [n for n in neighbs if
                                           not (n[0] < 0 or n[0] > self.xdim or n[1] < 0 or n[1] > self.ydim)]
                            if ids:
                                if tiered:
                                    tier.extend(neighbs)
                                else:
                                    neighbors.extend(neighbs)
                            else:
                                if tiered:
                                    tier.extend([self.get_locale(*locale) for locale in neighbs])
                                else:
                                    neighbors.extend([self.get_locale(*locale) for locale in neighbs])
                            new_queue.extend(neighbs)
                    explored.add(node)
                if tiered:
                    neighbors.append(tier)

        return neighbors


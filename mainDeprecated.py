# -*- coding: utf-8 -*-
"""main.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import beringiaDeprecated.region as reg


class Session(object):
    """The session represents the interface with the region. Most of the actual simulation logic is rooted in region.py.

    """
    def __init__(self):
        self.region = None
        self.main()
        self.xdim = 10
        self.ydim = 10
        self.flora_system = 1

    def main(self):
        self.set_dimensions()
        self.region = reg.Region(self.xdim, self.ydim)
        while True:
            inp = input("enter command('h' for help):")
            if inp in ['exit', 'e']:
                break
            else:
                self.parser(inp)

    #TODO: Make numeric inputs tolerant to incorrect inputs
    #def int_parser(self, inp):
    #    inp = str(inp).lower()
    #    if inp == 'exit':
    #        self.exit()
    #    elif inp

    def parser(self, inp):
        inp = str(inp).lower()
        if inp in ['h', 'help']:
            self.help()
        if inp in ['param', 'parameters']:
            self.set_parameters()
        if inp in ['reset']:
            self.reset()
        if inp in ['e', 'exit']:
            self.exit()
        if inp in ['run', 'r']:
            self.run()
        if inp in ['elev', 'elevation']:
            self.show_elevation()
        if inp in ['slow', 'slow burn']:
            self.toggle_burn()
        if inp in ['flora', 'flora system', 'f']:
            self.set_flora_system()

    @classmethod
    def help(self):
        print("e: exit \nrun: run \nh: help\nreset: reset with a new region.\nelev: Show Elevation Map\nslow: Toggle show fire spread\nFlora: Set flora system")

    @classmethod
    def set_parameters(self):
        print("This function is not yet implemented.")

    def set_dimensions(self):
        self.xdim = int(input("x dimension(10-30 ideal)?"))
        self.ydim = int(input("y dimension?"))

    def reset(self):
        self.set_dimensions()
        self.region = reg.Region(self.xdim, self.ydim, self.flora_system)

    def run(self):
        turns = int(input("how many turns?"))
        self.region.show_turns(turns)

    def show_elevation(self):
        self.region.show_elevation_map()

    def exit(self):
        pass

    def toggle_burn(self):
        if self.region.slow_burn == False:
            self.region.slow_burn = True
        elif self.region.slow_burn == True:
            self.region.slow_burn = False
        else:
            self.region.slow_burn = True
        print('Slow burn set to:', self.region.slow_burn)

    def set_flora_system(self):
        self.flora_system= int(input('Select flora system type(0-4):'))
        self.region = reg.Region(self.xdim, self.ydim, flora_system=self.flora_system)


if __name__ == "__main__":
    Session()

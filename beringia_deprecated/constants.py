# -*- coding: utf-8 -*-
"""constants.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
STATE_CONSTANTS = {
    0: {'stateIncreaseProb': 0.20, 'stateDecreaseProb': 0, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000},
    1: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.100},
    2: {'stateIncreaseProb': 0.15, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.200},
    3: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.300},
    4: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.450},
    5: {'stateIncreaseProb': 0.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.700},
    -1: {'stateIncreaseProb': 1.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000}
}



#TODO look into implementing 'rich' package.
PLANT_COLOR_KEY = {
    0: '\033[1;30;48;5;246m0\033[0;39m',
    1: '\033[1;30;48;5;226m1\033[0;39m',
    2: '\033[1;30;48;5;190m2\033[0;39m',
    3: '\033[1;30;48;5;154m3\033[0;39m',
    4: '\033[1;30;48;5;118m4\033[0;39m',
    5: '\033[1;30;48;5;82m5\033[0;39m',
    6: '\033[1;30;48;5;46m6\033[0;39m',
    7: '\033[1;30;48;5;40m7\033[0;39m',
    8: '\033[1;30;48;5;34m8\033[0;39m',
    9: '\033[1;30;48;5;22m9\033[0;39m',
    -1: 'f'
}

GRAYSCALE_COLOR_KEY = {
    0: '\033[1;37;48;5;252m0\033[0;39m',
    1: '\033[1;30;48;5;250m1\033[0;39m',
    2: '\033[1;30;48;5;248m2\033[0;39m',
    3: '\033[1;30;48;5;246m3\033[0;39m',
    4: '\033[1;30;48;5;244m4\033[0;39m',
    5: '\033[1;30;48;5;242m5\033[0;39m',
    6: '\033[1;30;48;5;240m6\033[0;39m',
    7: '\033[1;30;48;5;238m7\033[0;39m',
    8: '\033[1;30;48;5;236m8\033[0;39m',
    9: '\033[1;30;48;5;234m9\033[0;39m',
    10:'\033[1;30;48;5;234m9\033[0;39m',
    11:'\033[1;30;48;5;234m9\033[0;39m',
    12: '\033[1;30;48;5;234m9\033[0;39m',
    13: '\033[1;30;48;5;234m9\033[0;39m',
    14: '\033[1;30;48;5;234m9\033[0;39m',
    15: '\033[1;30;48;5;234m9\033[0;39m',
}

FIRESCALE_COLOR_KEY = {
    0: '\033[1;30;48;5;15m0\033[0;39m',
    1: '\033[1;30;48;5;226m1\033[0;39m',
    2: '\033[1;30;48;5;220m2\033[0;39m',
    3: '\033[1;30;48;5;214m3\033[0;39m',
    4: '\033[1;30;48;5;208m4\033[0;39m',
    5: '\033[1;30;48;5;202m5\033[0;39m',
    6: '\033[1;30;48;5;196m6\033[0;39m',
    7: '\033[1;30;48;5;160m7\033[0;39m',
    8: '\033[1;30;48;5;124m8\033[0;39m',
    9: '\033[1;30;48;5;88m9\033[0;39m'
}

COLOR_KEY = {
    0: ''
}

FEATURES_SWITCH = {
    'geology': True,
    'fauna': True
}

CONT_TO_DISC_FAUNA_CONVERSION=100
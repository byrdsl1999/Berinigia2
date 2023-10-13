# Beringia

This project is designed to simulate/model the develop forest growth. More features may be added in time.

https://en.wikipedia.org/wiki/Beringia

Current state as of sept 22 2023:
Directories:
/beringiaDeprecated/ contains the core original program that does a sort of fire simulation
/beringiaParts/ contains a bunch of independent/related toy programs. Of note are:
clickGame.py - a first stab at a local interface for the program. Allows you to click on squares.
asciiFlower.py - a program that creates modular ascii flowers. A stupid little thing that I would love to integrate for some janky visualizations of plants.

/beringia/ A new low level ecological model that I'd like to tie in to the core program to replace the locale class. Also ties in species with names. Trying to develop a more mature file structure.
## Installation

```bash
pip install --upgrade -r requirements.txt
```

## Linting

You can check for PEP8 violations by running `flake8`:

```bash
flake8 --max-line-length=120
```

## Documentation

To build these docs:

```bash
cd docs
make html
```


## Usage

Execute main.py. 

"main.py" is currently missing a lot of the more interesting and fun features, but should give you a taste. 
If you want to play around with the innards a bit more paste the contents of "region" into your python console.

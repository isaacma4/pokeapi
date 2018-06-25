# pokeapi
A short program that is used to compare two or more Pokemon and select the Pokemon with the best type advantage. Requires at least Python 3.6 with access to the Internet to access RESTful API from https://pokeapi.co.

## Run before
The dependencies for requests library must be installed before running this app. Do this by running the command below:

    pip install -r requirements.txt

## Usage
Entering any amount of pokemon names or ids into the script will display the Pokemon with the best type advantage, or, in the case of a tie, a Pokemon with the best base stats.

### Example Input #1
    python pokeapp.py charmander squirtle

### Example Output #1
    squirtle

Example Output #1 is correct because Water types have a distinct advantage over Fire types

### Example Input #2
    python pokeapp.py zapdos moltres articuno

### Example Output #2
    zapdos

Example Output #2 is correct because Zapdos and Articuno have a type advantage over all other Pokemon, and Zapdos has better base stats than Articuno--Moltres only has a type advantage over Articuno.

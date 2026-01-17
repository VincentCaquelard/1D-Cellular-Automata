# 1D-Cellular-Automata
An advanced and high-performance Python implementation of 1D Cellular Automata.

## Features
- **Fast Vectorized Updates**: Powered by NumPy for high performance even on massive grids (e.g., 5000x5000).
- **Flexible Neighborhoods**: Support for arbitrary neighborhood radius.
- **Multiple States**: Run CA with 2, 3, 4, or more states.
- **Rule Support**: Standard Wolfram rules, custom rule strings, and totalistic rules.
- **Presets**: Includes several interesting rules discovered by the community.
- **Beautiful Visualizations**: Integrated with Seaborn for a wide variety of color palettes.
- **Animated GIFs**: Export the evolution of your CA as an animation.
- **Gallery Mode**: Automatically generate a collection of random rules to find something interesting.

## Installation
Ensure you have the dependencies installed:
```bash
pip install numpy Pillow seaborn
```

## Usage

### Simple run with the new engine
```bash
python3 main_v2.py --preset rule30 -o rule30.png
```

### Run with a 3-state rule from the original collection
```bash
python3 main_v2.py --preset ice -w 600 -n 400 --palette rocket
```

### Generate an animated GIF
```bash
python3 main_v2.py --preset spaghetti --gif -w 100 -n 100 --duration 50
```

### Generate a gallery of 10 random 4-state rules
```bash
python3 main_v2.py --gallery 10 -s 4 --random_palette -w 200 -n 200
```

### CLI Arguments
- `-w`, `--width`: Grid width (default: 400)
- `-n`, `--iterations`: Number of steps (default: 400)
- `-s`, `--states`: Number of states (default: 2)
- `-r`, `--radius`: Neighborhood radius (default: 1)
- `--rule`: Rule string or integer
- `--totalistic`: Use totalistic rules
- `--preset`: Use one of the built-in presets (`rule30`, `ice`, `emergent`, `spaghetti`, `cool`, `roots`, `gol_like`)
- `-o`, `--out`: Output filename
- `--gif`: Generate a GIF instead of a PNG
- `--init`: Initialization mode (`random`, `center`, `pattern`)
- `--palette`: Seaborn color palette name
- `--gallery N`: Generate N random rules

## Interesting rules discovered
| Name | States | Radius | Rule String |
|------|--------|--------|-------------|
| Rule 30 | 2 | 1 | 30 |
| Ice | 3 | 1 | 122010212001002012222122002 |
| Emergent | 3 | 1 | 020122011122022212121122100 |
| Roots | 4 | 1 | 3112322322013310200321203223230223112111212332200031213033223231 |
| GoL-like | 5 | 1 | (Long string in main_v2.py) |

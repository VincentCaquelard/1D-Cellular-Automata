from PIL import Image
import numpy as np
import seaborn as sns
import random
import argparse
import sys

parser = argparse.ArgumentParser(
    prog='1D Cellular Automata Python implementation',
    description='...'
)
parser.add_argument('-w', '--width', default=100)
parser.add_argument('-n', '--nb_of_iterations', default=300)
parser.add_argument('-n_state', '--nb_of_states', default=3)
parser.add_argument('-r', '--rule', default="202112100110202000122012211")
parser.add_argument('-o', '--out', default="out.png")
parser.add_argument('-init', '--initial_pattern', default="111")
parser.add_argument('--random_rule', action='store_true')
parser.add_argument('--random_init', action='store_true')

def get_random_rule(n_state):
    rule = np.random.randint(n_state, size=pow(n_state, 3))
    return "".join(str(x) for x in rule)

def rand_palette():
    p_l=["crest","viridis","YlOrBr","Spectral","flare","cubehelix","rocket","magma","hls"]
    return p_l[random.randint(0,len(p_l)-1)]

def _get_config(neighbors):
    return np.sum(np.power(n_state, np.arange(2, -1, -1)) * neighbors)

def _get_first_it(init_pattern):
    pt_len = len(init_pattern) # len of the init pattern
    iteration = np.zeros(width, dtype=int)
    shift = (width//2) - pt_len
    iteration[shift:shift+pt_len] = [int(x) for x in init_pattern]
    return iteration

def _get_first_it_random():
    return np.random.randint(n_state, size=width)

args = parser.parse_args()
# Define the dimensions of the image
width = int(args.width)
nb_it = int(args.nb_of_iterations)
n_state = int(args.nb_of_states)

if args.random_rule:
    rule = get_random_rule(n_state)
    print("Random rule: ", rule)
else:
    rule = args.rule
if len(rule) != pow(n_state, 3):
    sys.exit(f"Error: rule size: {len(rule)} incompatible with number of states: {n_state}")

if args.random_init:
    iteration = _get_first_it_random()
else:
    iteration = _get_first_it(args.initial_pattern)
grid = iteration

for i in range(nb_it):
    neighbors = np.zeros((width, 3), dtype=int)
    neighbors[:, 0] = np.roll(iteration, 1)
    neighbors[:, 1] = iteration
    neighbors[:, 2] = np.roll(iteration, -1)
    c = _get_config(neighbors)
    iteration = np.array([int(x) for x in rule[c]])    
    grid = np.vstack((grid, iteration))

color_palette = rand_palette()
palette = sns.color_palette(color_palette, n_state)

# Define the grid of pixel values (in this example, just a diagonal line)
pixels = np.array([tuple(int(c * 255) for c in palette[x]) for x in grid.flatten()])


# Create a new image with the specified dimensions and pixel values
img = Image.new('RGB', (width, nb_it+1))
img.putdata(pixels)

# Save the image to a file
img.save(args.out)
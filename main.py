from PIL import Image
import seaborn as sns
import random
import argparse
import sys

parser = argparse.ArgumentParser(
                    prog='1D Cellular Automata Python implementation',
                    description='...')
parser.add_argument('-w', '--width',default=100) 
parser.add_argument('-n', '--nb_of_iterations',default=300) 
parser.add_argument('-n_state', '--nb_of_states',default=3) 
parser.add_argument('-r', '--rule',default="202112100110202000122012211") 
parser.add_argument('--random_rule', action='store_true')
parser.add_argument('--border_mode', action='store_false')

def get_random_rule(n_state):
	rule=""
	for k in range(pow(n_state,3)):
		rule+=str((random.randint(0,n_state-1)))
	return rule

args = parser.parse_args()
# Define the dimensions of the image
width = int(args.width)
nb_it = int(args.nb_of_iterations)

n_state=int(args.nb_of_states)
if args.random_rule:
	rule=get_random_rule(n_state)
	print("Random rule: ",rule)
else:
	rule= args.rule

if len(rule)!= pow(n_state,3):
	sys.exit(f"Error: rule size: {len(rule)} incompatible with number of states: {n_state}")

#rule= "012121121112210000222102010"
#rule= "0210211111111120021021021021"
#rule= "210211121000120021021221021"
rule_spaghetti= "110211121001120021021221002"
rule_cool="110211121001120021021201002"
#rule="220211121001120021021201002"
#rule_4="202112100110222000000012211"
#rule="202112100110202000122012211"



world = [0] * width
world[width//2]=2

loop_mode=args.border_mode

timeline = world

def rand_palette():
	p_l=["crest","viridis","YlOrBr","Spectral","flare","cubehelix","rocket","magma","hls"]
	return p_l[random.randint(0,len(p_l)-1)]


def _get_config(neighbors):
	l=len(neighbors)
	res = 0
	for k in range(l):
		res += pow(n_state,(l-1)-k)*neighbors[k]
	return res

for i in range(nb_it):
	#print(world)
	world_p1=[0]*width
	if loop_mode:
		for k in range(width):
			neighbors=[world[(k-1)%width], world[k], world[(k+1)%width]]
			c = _get_config(neighbors)
			world_p1[k]=int(rule[(len(rule)-1)-c])
	else:
		for k in range(1,width-1):
			neighbors=[world[k-1], world[k], world[k+1]]
			c = _get_config(neighbors)
			world_p1[k]=int(rule[(len(rule)-1)-c])

	
	world=world_p1
	timeline.extend(world)

color_palette = rand_palette()
palette = sns.color_palette(color_palette, n_state)
# Define the grid of pixel values (in this example, just a diagonal line)
pixels = [tuple(int(c * 255) for c in palette[x]) for x in timeline]

# Create a new image with the specified dimensions and pixel values
img = Image.new('RGB', (width, nb_it+1))
img.putdata(pixels)

# Save the image to a file
img.save('test.png')
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
parser.add_argument('-o', '--out',default="out.png") 
parser.add_argument('-init', '--initial_pattern',default="111") 
parser.add_argument('--random_rule', action='store_true')
parser.add_argument('--random_init', action='store_true')

def get_random_rule(n_state):
	rule=""
	for k in range(pow(n_state,3)):
		rule+=str((random.randint(0,n_state-1)))
	return rule

def rand_palette():
	p_l=["crest","viridis","YlOrBr","Spectral","flare","cubehelix","rocket","magma","hls"]
	return p_l[random.randint(0,len(p_l)-1)]


def _get_config(neighbors):
	l=len(neighbors)
	res = 0
	for k in range(l):
		res += pow(n_state,(l-1)-k)*neighbors[k]
	return res

def _get_first_it(init_pattern):
	pt_len = len(init_pattern) # len of the init pattern
	iteration = [0] * width
	shift=(width//2)-pt_len
	for k in range(pt_len):
		iteration[shift+k]=int(init_pattern[k])
	return iteration

def _get_first_it_random():
	return [random.randint(0,n_state-1) for x in range(width) ]

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

if args.random_init:
	iteration = _get_first_it_random()
else:
	iteration= _get_first_it(args.initial_pattern)

#===========Interesting 3-state rule===========
#rule= "012121121112210000222102010"
#rule= "0210211111111120021021021021"
#rule= "210211121000120021021221021"
#rule_spaghetti= "110211121001120021021221002"
#rule_cool="110211121001120021021201002"
#rule="220211121001120021021201002"
#rule_4="202112100110222000000012211"
#rule="202112100110202000122012211"
# 122010212001002012222122002 frozen ice 
# 020122011122022212121122100 emergent pattern when zoomed out

#============Interesting 4-state rules==============
#->3321222303313302311032132200032220022133033331000103013121220322
#->3112322322013310200321203223230223112111212332200031213033223231  looks like root with random initial row

#============Interesting 5-state rules==============
#->22034430420241013303413134443133020342123002043300402044002430223000232312212040334004314143113141101230123330324414034040414
#->34234111124203400124400032322020004422402330114310113443322142020133014300012311300121231010403004032122044331002304321204220 Conway's Gol like behaviour O:

grid = iteration

for i in range(nb_it):
	#print(iteration)
	iteration_p1=[0]*width
	for k in range(width):
		neighbors=[iteration[(k-1)%width], iteration[k], iteration[(k+1)%width]]
		c = _get_config(neighbors)
		iteration_p1[k]=int(rule[(len(rule)-1)-c])

	
	iteration=iteration_p1
	grid.extend(iteration)

color_palette = rand_palette()
palette = sns.color_palette(color_palette, n_state)

# Define the grid of pixel values (in this example, just a diagonal line)
pixels = [tuple(int(c * 255) for c in palette[x]) for x in grid]

# Create a new image with the specified dimensions and pixel values
img = Image.new('RGB', (width, nb_it+1))
img.putdata(pixels)

# Save the image to a file
img.save(args.out)
import argparse
import sys
from engine import CellularAutomata, generate_image, generate_gif
import random
import numpy as np

# A collection of interesting rules found in the original README and others
INTERESTING_RULES = {
    'rule30': (2, 1, 30, False),
    'rule110': (2, 1, 110, False),
    'rule90': (2, 1, 90, False),
    'rule184': (2, 1, 184, False),
    'ice': (3, 1, "122010212001002012222122002", False),
    'emergent': (3, 1, "020122011122022212121122100", False),
    'spaghetti': (3, 1, "110211121001120021021221002", False),
    'cool': (3, 1, "110211121001120021021201002", False),
    'roots': (4, 1, "3112322322013310200321203223230223112111212332200031213033223231", False),
    'gol_like': (5, 1, "34234111124203400124400032322020004422402330114310113443322142020133014300012311300121231010403004032122044331002304321204220", False)
}

def main():
    parser = argparse.ArgumentParser(description='Advanced 1D Cellular Automata Engine')
    parser.add_argument('-w', '--width', type=int, default=400)
    parser.add_argument('-n', '--iterations', type=int, default=400)
    parser.add_argument('-s', '--states', type=int, default=2)
    parser.add_argument('-r', '--radius', type=int, default=1)
    parser.add_argument('--rule', type=str, help='Rule string or integer')
    parser.add_argument('--totalistic', action='store_true', help='Use totalistic rule')
    parser.add_argument('--preset', choices=INTERESTING_RULES.keys(), help='Use an interesting preset rule')

    parser.add_argument('-o', '--out', default='out.png', help='Output file path')
    parser.add_argument('--gif', action='store_true', help='Generate animated GIF (warning: can be slow/large)')
    parser.add_argument('--duration', type=int, default=50, help='Duration of each frame in GIF (ms)')

    parser.add_argument('--init', choices=['random', 'center', 'pattern'], default='center')
    parser.add_argument('--pattern', type=str, default='1', help='Initial pattern for center or pattern mode')

    parser.add_argument('--palette', default='viridis', help='Seaborn color palette name')
    parser.add_argument('--random_palette', action='store_true', help='Choose a random color palette')
    parser.add_argument('--list_presets', action='store_true', help='List all preset rules')
    parser.add_argument('--gallery', type=int, help='Generate a gallery of N random rules')

    args = parser.parse_args()

    if args.list_presets:
        print("Interesting Presets:")
        for name, params in INTERESTING_RULES.items():
            print(f"  {name:10} : states={params[0]}, radius={params[1]}, totalistic={params[3]}")
        return

    states = args.states
    radius = args.radius
    rule = args.rule
    totalistic = args.totalistic

    if args.preset:
        states, radius, rule, totalistic = INTERESTING_RULES[args.preset]
        print(f"Using preset: {args.preset}")

    if args.gallery:
        import os
        os.makedirs('gallery', exist_ok=True)
        for i in range(args.gallery):
            if args.random_palette:
                p_l=["crest","viridis","YlOrBr","Spectral","flare","cubehelix","rocket","magma","hls", "icefire", "mako", "rocket_r"]
                palette = random.choice(p_l)
            else:
                palette = args.palette

            ca = CellularAutomata(width=args.width, states=states, radius=radius, rule=None, totalistic=totalistic)
            ca.initialize(mode=args.init, pattern=args.pattern)
            grid = ca.run(args.iterations)
            rule_str = "".join(map(str, ca.rule[::-1]))
            out_path = f"gallery/random_{i}_{states}s_{radius}r.png"
            generate_image(grid, states, palette_name=palette, out_path=out_path)
            print(f"Generated {out_path} with rule: {rule_str}")
        print(f"Gallery generated in 'gallery/' folder.")
        return

    if args.random_palette:
        p_l=["crest","viridis","YlOrBr","Spectral","flare","cubehelix","rocket","magma","hls", "icefire", "mako", "rocket_r"]
        args.palette = random.choice(p_l)
        print(f"Random palette: {args.palette}")

    try:
        ca = CellularAutomata(width=args.width, states=states, radius=radius, rule=rule, totalistic=totalistic)
    except Exception as e:
        print(f"Error initializing Cellular Automata: {e}")
        sys.exit(1)

    # Print a snippet of the rule if it's long
    rule_repr = "".join(map(str, ca.rule[::-1]))
    if len(rule_repr) > 64:
        rule_repr = rule_repr[:32] + "..." + rule_repr[-32:]
    print(f"Rule used: {rule_repr}")

    ca.initialize(mode=args.init, pattern=args.pattern)
    print(f"Running {args.iterations} iterations...")
    grid = ca.run(args.iterations)

    if args.gif:
        out_gif = args.out.replace('.png', '.gif') if args.out.endswith('.png') else args.out
        if not out_gif.endswith('.gif'):
            out_gif += '.gif'
        print(f"Generating GIF: {out_gif}...")
        generate_gif(grid, states, palette_name=args.palette, out_path=out_gif, duration=args.duration)
    else:
        print(f"Saving image to {args.out}...")
        generate_image(grid, states, palette_name=args.palette, out_path=args.out)

    print("Done!")

if __name__ == '__main__':
    main()

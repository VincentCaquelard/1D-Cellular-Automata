from engine import CellularAutomata, generate_image
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        prog='1D Cellular Automata - Fast Vectorized Implementation',
        description='A high-performance implementation of 1D CA using NumPy'
    )
    parser.add_argument('-w', '--width', default=100, type=int)
    parser.add_argument('-n', '--nb_of_iterations', default=300, type=int)
    parser.add_argument('-n_state', '--nb_of_states', default=3, type=int)
    parser.add_argument('-r', '--rule', default="202112100110202000122012211")
    parser.add_argument('-o', '--out', default="out.png")
    parser.add_argument('-init', '--initial_pattern', default="111")
    parser.add_argument('--random_rule', action='store_true')
    parser.add_argument('--random_init', action='store_true')

    args = parser.parse_args()

    rule = None if args.random_rule else args.rule
    init_mode = 'random' if args.random_init else 'center'

    ca = CellularAutomata(width=args.width, states=args.nb_of_states, rule=rule)
    ca.initialize(mode=init_mode, pattern=args.initial_pattern)
    grid = ca.run(args.nb_of_iterations)

    generate_image(grid, args.nb_of_states, palette_name="viridis", out_path=args.out)
    print(f"Saved to {args.out}")

if __name__ == '__main__':
    main()

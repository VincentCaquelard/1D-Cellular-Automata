import numpy as np
from PIL import Image
import seaborn as sns

class CellularAutomata:
    def __init__(self, width, states=2, radius=1, rule=None, totalistic=False):
        self.width = width
        self.states = states
        self.radius = radius
        self.totalistic = totalistic
        self.neighborhood_size = 2 * radius + 1

        if totalistic:
            self.num_configs = (self.states - 1) * self.neighborhood_size + 1
        else:
            self.num_configs = self.states ** self.neighborhood_size

        self.rule = self._parse_rule(rule)
        self.grid = None

    def _parse_rule(self, rule):
        if rule is None:
            return np.random.randint(0, self.states, self.num_configs)

        if isinstance(rule, int):
            # Convert int to rule array (Wolfram style)
            rule_str = np.base_repr(rule, base=self.states)
            if len(rule_str) > self.num_configs:
                raise ValueError(f"Rule integer {rule} is too large for {self.num_configs} configurations")
            rule_arr = np.array([int(d, self.states) for d in rule_str.zfill(self.num_configs)])
            return np.flip(rule_arr) # Bit 0 corresponds to config 0

        if isinstance(rule, str):
            if len(rule) != self.num_configs:
                # Try to handle it as an int if it's all digits
                try:
                    # Only if it's not too long for an int
                    if len(rule) < 20:
                        return self._parse_rule(int(rule))
                except ValueError:
                    pass
                raise ValueError(f"Rule string length {len(rule)} does not match expected {self.num_configs}")
            return np.array([int(c, self.states) for c in rule][::-1])

        return np.asanyarray(rule)

    def initialize(self, mode='random', pattern=None):
        self.grid = np.zeros(self.width, dtype=int)
        if mode == 'random':
            self.grid = np.random.randint(0, self.states, self.width)
        elif mode == 'center':
            if pattern is None:
                self.grid[self.width // 2] = 1
            else:
                p_len = len(pattern)
                start = (self.width - p_len) // 2
                self.grid[start:max(0, start+p_len)] = [int(c, self.states) for c in pattern[:self.width]]
        elif mode == 'pattern':
            if pattern is not None:
                p_len = len(pattern)
                self.grid[:min(self.width, p_len)] = [int(c, self.states) for c in pattern[:self.width]]
        return self.grid

    def _get_neighbors(self, current_grid):
        # Efficiently get neighbors for all cells using rolling
        stacked = []
        for i in range(-self.radius, self.radius + 1):
            stacked.append(np.roll(current_grid, -i))
        return np.stack(stacked, axis=1)

    def step(self, current_grid):
        neighbors = self._get_neighbors(current_grid)

        if self.totalistic:
            configs = np.sum(neighbors, axis=1)
        else:
            # Convert neighbor states to a single index
            # Powers should be [states^2, states^1, states^0] for r=1
            powers = self.states ** np.arange(self.neighborhood_size - 1, -1, -1)
            configs = np.dot(neighbors, powers)

        return self.rule[configs]

    def run(self, iterations):
        full_grid = np.zeros((iterations + 1, self.width), dtype=int)
        full_grid[0] = self.grid

        current = self.grid
        for i in range(1, iterations + 1):
            current = self.step(current)
            full_grid[i] = current

        return full_grid

def generate_image(grid, n_states, palette_name="viridis", out_path="out.png"):
    palette = sns.color_palette(palette_name, n_states)
    # Map states to RGB
    colors = (np.array(palette) * 255).astype(np.uint8)
    img_data = colors[grid]
    img = Image.fromarray(img_data, 'RGB')
    if out_path:
        img.save(out_path)
    return img

def generate_gif(full_grid, n_states, palette_name="viridis", out_path="out.gif", duration=100):
    palette = sns.color_palette(palette_name, n_states)
    colors = (np.array(palette) * 255).astype(np.uint8)

    frames = []
    # To make the GIF more interesting, we can show the evolution row by row or just frames of the whole thing
    # Usually for 1D CA, a GIF might show the growth.
    # But let's just make it show the grid accumulated.
    for i in range(1, len(full_grid) + 1):
        # Create an image that is i rows high, but padded to full height to keep dimensions consistent?
        # Actually, let's just show the full grid but masking future rows.
        current_display = np.zeros_like(full_grid)
        current_display[:i] = full_grid[:i]
        # Or better: just show the evolution of the last row? No, that's not 1D CA style.
        # Let's do a scrolling effect or just growing.

        frame_data = colors[current_display]
        frames.append(Image.fromarray(frame_data, 'RGB'))

    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=duration, loop=0)

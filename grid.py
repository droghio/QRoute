import numpy as np
import pprint


class Grid:
    def __init__(self, rows, cols, netlists):
        self._grid = np.zeros([rows, cols], dtype=[("color", "u1"), ("fixed", "bool")])
        # One hot encoding, first bit is white.
        self._grid[:, :]["color"] = 1
        # From there assign each remaning color a bit.
        self.netlist_colors = dict(map(lambda x: (x[1], 1<<(x[0]+1)), enumerate(netlists)))
        self.number_colors = len(netlists)+1
        self.shape = self._grid.shape


    def __copy__(self):
        new_grid = Grid(self._grid.shape[0], self._grid.shape[1], self.netlist_colors.keys())
        new_grid._grid = self._grid.copy()
        return new_grid


    def __str__(self):
        return pprint.pformat(self._grid)


    def __getitem__(self, index):
        return self._grid[index]


    def assign_node(self, row, col, netlist, fixed=True):
        self._grid[row, col] = (self.netlist_colors[netlist], fixed)


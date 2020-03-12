import copy
import threading

from grid import Grid
from render import Render

class Algoritm:
    def __init__(self, view_grid):
        self.seen_solutions_hashes = set()
        self.queued_solutions = []
        self.view_grid = view_grid
        self.curent_min = float("inf")


    @staticmethod
    def mutate(grid):
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row][col]["fixed"] == False:
                    for idx in range(grid.number_colors):
                        color = 1<<idx
                        new_grid = copy.copy(grid)
                        new_grid[row, col]["color"] = color
                        yield(new_grid)


    def run(self, grid):
        self.queued_solutions.append(grid)
        grid_hash = grid._grid.tobytes()
        self.seen_solutions_hashes.add(grid_hash)
        threading.Thread(target=algorithm._run_inner).start()


    def _run_inner(self):
        while len(self.queued_solutions) > 0:
            solution = self.queued_solutions.pop()
            self.view_grid._grid = solution._grid
            for new_solution in self.mutate(solution):
                new_solution_hash = new_solution._grid.tobytes()
                if new_solution_hash not in self.seen_solutions_hashes:
                    self.seen_solutions_hashes.add(new_solution_hash)
                    self.queued_solutions.append(new_solution)

            if len(self.queued_solutions) % 100 == 0:
                print(f"Size: {len(self.queued_solutions)}               ", end="\r")

        print(f"Processed {len(self.seen_solutions_hashes)} colorings.")


if __name__ == "__main__":
    grid_size = (4, 4)
    netlists = [ "A", "B" ]

    grid = Grid(grid_size[0], grid_size[1], netlists)
    grid.assign_node(0, 0, "A")
    grid.assign_node(2, 2, "A")
    print(grid)

    algorithm = Algoritm(grid)
    algorithm.run(grid)

    renderer = Render(grid_size)
    renderer.draw_loop(grid)

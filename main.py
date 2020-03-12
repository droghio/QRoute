import copy
import threading

from collections import deque, namedtuple
from grid import Grid
from render import Render


class Algoritm:
    C_FAILED_REQUIREMENT_WEIGHT = 100
    C_EDGE_WEIGHT = 1

    def __init__(self, view_grid, requirement_nodes):
        self.seen_solutions_hashes = set()
        self.queued_solutions = deque([])
        self.view_grid = view_grid
        self.current_min = float("inf")
        self.current_solution = None
        self.requirement_nodes = requirement_nodes
        self._handle = None
        self._stop = False


    def score(self, grid):
        score = self.C_EDGE_WEIGHT*(grid[:, :]["color"] != 1).sum()
        for requirement in requirement_nodes:
            if grid[requirement[0], requirement[1]]["color"] != grid.netlist_colors[requirement[2]]:
                score += self.C_FAILED_REQUIREMENT_WEIGHT

        return score


    @staticmethod
    def mutate(grid):
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row, col]["fixed"] == False:
                    # If uncolored take the color of any neighbors.
                    if grid[row, col]["color"] == 1:
                        for idx in range(1, grid.number_colors):
                            color = 1<<idx
                            neighbors = (
                                (row, col-1),
                                (row, col+1),
                                (row-1, col),
                                (row+1, col)
                            )

                            for irow,icol in neighbors:
                                if (irow >= 0 and icol >= 0 and
                                        irow < grid.shape[0] and icol < grid.shape[1] and
                                        grid[irow, icol]["color"] == color):
                                    new_grid = copy.copy(grid)
                                    new_grid[row, col]["color"] = color
                                    yield(new_grid)
                                    break


    def run(self, grid):
        self.queued_solutions.append(grid)
        grid_hash = grid._grid.tobytes()
        self.seen_solutions_hashes.add(grid_hash)
        if self._handle == None:
            self._handle = threading.Thread(target=algorithm._run_inner)
            self._handle.start()
        else:
            raise ValueError("The run thread is already running.")


    def _run_inner(self):
        while self._stop == False and len(self.queued_solutions) > 0:
            solution = self.queued_solutions.popleft()

            score = self.score(solution)
            if score < self.current_min:
                self.current_min = score
                self.current_solution = solution

            for new_solution in self.mutate(solution):
                new_solution_hash = new_solution._grid.tobytes()
                if new_solution_hash not in self.seen_solutions_hashes:
                    self.seen_solutions_hashes.add(new_solution_hash)
                    self.queued_solutions.append(new_solution)

            if len(self.seen_solutions_hashes) % 985 == 0:
                print(f"Size: {len(self.queued_solutions)} Score: {score} Min: {self.current_min} Processed: {len(self.seen_solutions_hashes)}            ", end="\r")
                with self.view_grid.lock:
                    self.view_grid._grid = solution._grid.copy()

        print()
        print(f"Processed {len(self.seen_solutions_hashes)} colorings.")
        self.view_grid._grid = self.current_solution._grid.copy()
        print(f"Minimum score: {self.current_min}")


    def stop(self):
        self._stop = True
        self._handle.join()


if __name__ == "__main__":
    grid_size = (5, 5)
    netlists = [ "A", "B" ]

    grid = Grid(grid_size[0], grid_size[1], netlists)
    grid.assign_node(0, 0, "A")
    grid.assign_node(0, 3, "B")
    grid.lock = threading.Lock()
    print(grid)

    requirement_nodes = [(3, 4, "A"), (3, 3, "B")]

    algorithm = Algoritm(grid, requirement_nodes)
    algorithm.run(copy.copy(grid))

    renderer = Render(grid_size)
    renderer.bind("<q>", lambda _: algorithm.stop())
    renderer.draw_loop(grid)

    print(f"Solution Score {algorithm.current_min}")
    print(algorithm.current_solution)
    algorithm.stop()

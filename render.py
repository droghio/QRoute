import math
import random
import tkinter


class Render(tkinter.Tk):
    C_COLORS = [ "white", "blue", "red" ]

    def __init__(self, grid_size):
        super().__init__("Preview")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._canvas = tkinter.Canvas(self)
        self._canvas.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.geometry("500x500")

        self._grid_tags = []
        self._init_grid(grid_size)


    @staticmethod
    def _circle_points(center_x, center_y, radius):
        return (center_x-radius/2, center_y-radius/2, center_x+radius/2, center_y+radius/2)


    def _init_grid(self, grid_size, radius=50, spacing=100):
        for row in range(grid_size[0]):
            self._grid_tags.append([])
            for col in range(grid_size[1]):
                self._grid_tags[-1].append(self._canvas.create_oval(self._circle_points(col*spacing+radius, row*spacing+radius, radius)))


    def draw(self, grid):
        with grid.lock:
            try:
                for row in range(grid.shape[0]):
                    for col in range(grid.shape[1]):
                        self._canvas.itemconfig(self._grid_tags[row][col], fill=self.C_COLORS[int(math.log2(grid[row][col]["color"]))])

            except IndexError:
                print("WARNING: Grid sized changing is not supported.")


    def _draw_loop_inner(self, grid):
        self.draw(grid)
        self._canvas.after(100, lambda : self._draw_loop_inner(grid))


    def draw_loop(self, grid):
        self._draw_loop_inner(grid)
        self.mainloop()

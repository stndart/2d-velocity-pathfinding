from typing import Callable
import numpy as np
from random import randint
from math import ceil

from backend.geometry import Rectangle, Point

def fill_dots(rect: Rectangle, N: int, seed = randint(1, int(1e6))) -> list[Point]:
    """
    Fills the rectangle with random points
    Each point is located in one of the grid cells
    """
    np.random.seed(seed)

    avg_dist = ((rect.top_right.x - rect.bottom_left.x) * (rect.top_right.y - rect.bottom_left.y) / N) ** 0.5
    W, H = ceil((rect.top_right.x - rect.bottom_left.x) / avg_dist), ceil((rect.top_right.y - rect.bottom_left.y) / avg_dist)
    if W * H < N:
        W += 1
    if W * H < N:
        raise ValueError("Too small grid") # This should never happen
    cell_xsize = (rect.top_right.x - rect.bottom_left.x) / W
    cell_ysize = (rect.top_right.y - rect.bottom_left.y) / H
    
    idx = np.random.choice(range(W * H), N, replace=False)
    points = []
    for i in idx:
        # x and y are uniformly distributed in the grid cell
        x = rect.bottom_left.x + (i % W + np.random.rand() * 0.8) * cell_xsize
        y = rect.bottom_left.y + (i // W + np.random.rand() * 0.8) * cell_ysize
        # x and y are at the center of the grid cell
        # x = rect.bottom_left.x + (i % W + 0.5) * cell_xsize
        # y = rect.bottom_left.y + (i // W + 0.5) * cell_ysize
        points.append(Point(x, y))
    return points
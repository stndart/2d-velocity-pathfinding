from typing import Callable
import numpy as np
from perlin_noise import PerlinNoise
from random import randint
from math import ceil

from backend.geometry import Rectangle, Point

def ternal_search(f: Callable[[float], float], a: float, b: float, eps: float = 1e-6) -> float:
    """
    Ternal search algorithm
    :param f: function to minimize
    """
    while abs(b - a) > eps:
        x1 = a + (b - a) / 3
        x2 = b - (b - a) / 3
        if f(x1) < f(x2):
            b = x2
        else:
            a = x1
    return (a + b) / 2

def bin_search(f: Callable[[float], float], a: float, b: float, eps: float = 1e-6) -> float:
    """
    Binary search algorithm
    """
    while abs(b - a) > eps:
        x = (a + b) / 2
        if f(x):
            b = x
        else:
            a = x
    return b

def fill_visited(dots: np.ndarray[float], visited: np.ndarray[int], threshold: float, visit_N: int = 1) -> tuple[np.ndarray[int], bool]:
    """
    Fills the visited array with <visit_N> for one connectivity component of the dots map
    """

    NW, NH = dots.shape
    def dfs(i, j):
        """
        Depth-first search algorithm with a stack
        """
        visited[i, j] = visit_N
        visit_stack = [(i, j)]
        while visit_stack:
            ci, cj = visit_stack.pop()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = ci + dx, cj + dy
                if 0 <= ni < NW and 0 <= nj < NH and not visited[ni, nj] and dots[ni, nj] >= threshold:
                    visited[ni, nj] = visit_N
                    visit_stack.append((ni, nj))
    
    for i in range(NW):
        for j in range(NH):
            if visited[i, j] == 0 and dots[i, j] >= threshold:
                dfs(i, j)
                return visited, True
    return visited, False

def count_dots(dots: np.ndarray[float], threshold: float) -> int:
    """
    Counts the number of dots, which correspond to each connectivity component of thresholded heights map
    """
    NW, NH = dots.shape
    visited = np.zeros((NW, NH), dtype=int)
    cnt = 0

    for i in range(NW*NH):
        visited, success = fill_visited(dots, visited, threshold, cnt + 1)
        if not success:
            break
        cnt += 1
    return cnt, visited

def mean_coords(visited: np.ndarray[int], visit_N: int) -> tuple[float, float]:
    """
    returns mean coordinates of the connectivity component with number <visit_N>
    """

    NW, NH = visited.shape
    xcoords, ycoords = np.meshgrid(np.arange(NW), np.arange(NH))
    xs = xcoords.T[visited == visit_N]
    ys = ycoords.T[visited == visit_N]
    return (np.mean(xs), np.mean(ys))

def fill_dots(rect: Rectangle, N: int, octaves: int = 4, seed = randint(1, int(1e6))) -> list[Point]:
    ocshift = 6
    noises = [PerlinNoise(octaves=3*oc, seed=(seed**oc) % int(1e6)) for oc in range(ocshift, ocshift + octaves)]
    L = 10 * N
    step = max(rect.height(), rect.width()) / L
    NW = ceil(rect.width() / step)
    NH = ceil(rect.height() / step)
    dots = np.zeros((NW, NH))

    def ij_to_rect_coords(i: int, j: int) -> list[float]:
        return [(i + 0.19176481) / NW,
                (j + 0.24157364) / NH]

    for i in range(NW):
        for j in range(NH):
            for n, noise in enumerate(noises):
                dots[i, j] += 1.2 ** (-n) * noise(ij_to_rect_coords(i, j))
    
    min_val, max_val = dots.min(), dots.max()
    dots = (dots - min_val) / (max_val - min_val)

    #plt.imshow(dots, cmap='gray')
    #plt.show()

    # find the threshold, that gives maximum number of points
    threshold_m = ternal_search(lambda x: -count_dots(dots, x)[0], 0.5, 1)
    # find the desired threshold, that gives the desired number of points
    threshold = bin_search(lambda x: count_dots(dots, x)[0] < N, threshold_m, 1)
    
    cnt, visited = count_dots(dots, threshold)
    res = []
    for i in range(cnt):
        res.append(mean_coords(visited, i + 1))
    return [Point(res[i][0] / NW * rect.width(), res[i][1] / NH * rect.height()) for i in range(cnt)]

def mean_min_distance(dots: list[Point]) -> float:
    """
    Returns the mean minimal distance between the dots
    """
    N = len(dots)
    if N == 0:
        return 0
    
    dists = np.ones((N, N)) * float('inf')
    for i in range(N):
        for j in range(i + 1, N):
            dists[i, j] = dists[j, i] = dots[i].distance_to(dots[j])
    return dists.min(axis=1).mean()
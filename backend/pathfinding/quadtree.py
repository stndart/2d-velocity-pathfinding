from typing import Generator, Iterable, Optional
from itertools import chain

from .graph import Graph
from .graph import GraphVertex as Vertex
from .graph import GraphEdge as Edge

from backend.geometry import Point, Rectangle, Line
from backend.sprites import Sprite

SPLIT_CONST = 2

def split_rectangle(rect: Rectangle, N: int = SPLIT_CONST):
    size = rect.top_right - rect.bottom_left
    size /= N
    for ix in range(N):
        for iy in range(N):
            bot_left = rect.bottom_left + Point(size.x * ix, size.y * iy)
            yield ix, iy, Rectangle(bot_left, bot_left + size)

def opposite_direction(direction: str) -> str:
    all_directions = ['left', 'right', 'top', 'bottom']
    opposite = ['right', 'left', 'bottom', 'top']
    if direction in all_directions:
        return opposite[all_directions.index(direction)]
    else:
        raise ValueError('Invalid direction')

def opposite_corner(corner: tuple[str]) -> tuple[str]:
    return tuple(opposite_direction(d) for d in corner)

class QuadTree:
    def __init__(self, rect: Rectangle, parent: Optional['QuadTree'] = None):
        assert rect.size().x == rect.size().y
        
        self.rectangle = rect
        self.parent = parent
        self.sprites: set[Sprite] = set()
        self.children: list[QuadTree] = [None] * SPLIT_CONST ** 2
    
    def __repr__(self) -> str:
        return f'QuadTree of [{self.rectangle.bottom_left}, {self.rectangle.top_right}] region with {len(self.sprites)} sprites'

    def print_tree(self, depth: int = 0, tabulation: str = '| '):
        s = tabulation * depth + '- ' + self.__repr__()
        if self.childless():
            return s
        for ch in self.children:
            if ch is None:
                s += '\n' + tabulation * (depth + 1) + '- empty'
            else:
                s += '\n' + ch.print_tree(depth + 1, tabulation)
        return s
        
    def contains(self, s: Sprite):
        return self.rectangle.contains(s.collision_shape)
    
    def childless(self) -> bool:
        return not any([ch is not None for ch in self.children])
    
    def iter_children(self) -> Iterable['QuadTree']:
        for ch in self.children:
            if ch is None:
                continue
            yield ch
    
    def dfs(self) -> Iterable['QuadTree']:
        yield self
        for ch in self.iter_children():
            yield from ch.dfs()

    def which_corner(self, q: 'QuadTree') -> tuple[str]:
        """
        for a given child QuadTree returns the corner it is located in
        if q is not a child, returns empty tuple
        """
        if self.childless():
            return ()
        for i, ch in enumerate(self.children):
            if ch is q:
                return [('top', 'left'), ('top', 'right'), ('bottom', 'left'), ('bottom', 'right')][i]
        return ()

    def get_side_children(self, side: str) -> Generator['QuadTree', None, None]:
        """
        Returns children of the QuadTree that are located on the specified side.
        side: str = 'left' | 'right' | 'top' | 'bottom'
        """
        if self.childless():
            return
        if side == 'left':
            for i in range(0, SPLIT_CONST ** 2, SPLIT_CONST):
                yield self.children[i]
        elif side == 'right':
            for i in range(SPLIT_CONST - 1, SPLIT_CONST ** 2, SPLIT_CONST):
                yield self.children[i]
        elif side == 'top':
            for i in range(SPLIT_CONST):
                yield self.children[i]
        elif side == 'bottom':
            for i in range(SPLIT_CONST ** 2 - SPLIT_CONST, SPLIT_CONST ** 2):
                yield self.children[i]
        else:
            raise ValueError('Invalid side')
    
    def get_side_grandchildren(self, side: str, edge: Optional[Line] = None) -> Generator['QuadTree', None, None]:
        """
        Returns all chilrden of the Quadtree and it's children that are located on the specified side.
        side: str = 'left' | 'right' | 'top' | 'bottom'
        If edge provided, returns only children, which rectangle contain the edge.
        """
        if self.childless():
            return
        for ch in self.get_side_children(side):
            if ch is not None:
                if edge is not None and not ch.rectangle.has_intersect(edge):
                    continue
                yield ch
                yield from ch.iter_children()
    
    def find_adjacent(self, direction: str = 'all', edge: Optional[Line] = None) -> Generator['QuadTree', None, None]:
        """
        Returns adjacent QuadTree in specified direction.
        direction: str = 'all' | 'left' | 'right' | 'top' | 'bottom'
        If edge is provided, returns adjacent QuadTrees, which rectangles contain the edge.
        """

        if self.parent is None:
            return
        
        if direction == 'all':
            for direction in ['left', 'right', 'top', 'bottom']:
                yield from self.find_adjacent(direction)
            return

        # populate edge: Line if not provided
        available_directions = ['left', 'top', 'right', 'bottom']
        if edge is None:
            if direction in available_directions:
                edge = self.rectangle.edges()[available_directions.index(direction)]
            else:
                raise ValueError('Invalid direction')

        if direction in self.parent.which_corner(self):
            yield from self.parent.find_adjacent(direction, edge)
        else:
            for q in self.parent.children:
                if q is None:
                    continue
                # skip current QuadTree and the one in the opposite corner
                if self.parent.which_corner(q) in [self.parent.which_corner(self), opposite_corner(self.parent.which_corner(self))]:
                    continue
                yield from q.get_side_grandchildren(opposite_direction(direction), edge)

    def init_children(self):
        for ix, iy, rect in split_rectangle(self.rectangle):
            i = ix + iy * SPLIT_CONST
            if self.children[i] is None:
                self.children[i] = QuadTree(rect, self)
    
    def clear_children(self):
        for i, ch in enumerate(self.children):
            if ch is None:
                continue
            if len(ch.sprites) == 0 and ch.childless():
                del ch
                self.children[i] = None
    
    def recursive_parents(self) -> Generator['QuadTree', None, None]:
        if self.parent is not None:
            yield self.parent
            yield from self.parent.recursive_parents()

    def optimize_tree(self) -> set[Sprite]:
        lost_by_children = set()
        for ch in self.iter_children():
            lost_by_children.update(ch.optimize_tree())
        
        lost = set()
        for s in self.sprites:
            if not self.contains(s):
                lost.add(s)
        self.sprites.difference_update(lost)
        
        chlost = set()
        for s in lost_by_children:
            if not self.contains(s):
                chlost.add(s)
        lost_by_children.difference_update(chlost)
        lost.update(chlost)
        
        moved = set()
        for s in chain(self.sprites, lost_by_children):
            for ch in self.iter_children():
                if ch.contains(s):
                    ch.add_sprites([s])
                    moved.add(s)
                    break
        lost_by_children.difference_update(moved)
        self.sprites.difference_update(moved)
        self.sprites.update(lost_by_children)
        
        self.clear_children()
        return lost
    
    def add_sprites(self, sprites: Iterable[Sprite]):
        for s in sprites:
            if self.contains(s):
                self.init_children()
                for ch in self.iter_children():
                    if ch.contains(s):
                        ch.add_sprites([s])
                        break
                else: # if not break encountered
                    self.sprites.add(s)
        
        self.clear_children()
    
    def get_sprites(self) -> set[Sprite]:
        ans = set()
        ans.update(self.sprites)
        for ch in self.iter_children():
            ans.update(ch.get_sprites())
        return ans
    
    def get_collision_candidates(self, s: Sprite) -> set[Sprite]:
        if not self.rectangle.has_intersect(s.collision_shape):
            return set()
        res = set()
        res.update(self.sprites)
        for ch in self.iter_children():
            res.update(ch.get_collision_candidates(s))
        return res
    
    def get_sprites_lazy(self) -> Generator[Sprite, None, None]:
        for s in self.sprites:
            yield s
        for ch in self.iter_children():
            yield from ch.get_sprites_lazy()
    
    def get_quad_tree(self, s: Sprite) -> Optional['QuadTree']:
        if not self.contains(s):
            return None
        
        for ch in self.iter_children():
            t = ch.get_quad_tree(s)
            if t is not None:
                return t
        return self
from typing import Generator, Iterable, Optional
from itertools import chain

from .graph import Graph
from .graph import GraphVertex as Vertex
from .graph import GraphEdge as Edge

from backend.geometry import Point, Rectangle
from backend.sprites import Sprite

SPLIT_CONST = 2

def split_rectangle(rect: Rectangle, N: int = SPLIT_CONST):
    size = rect.top_right - rect.bottom_left
    size /= N
    for ix in range(N):
        for iy in range(N):
            bot_left = rect.bottom_left + Point(size.x * ix, size.y * iy)
            yield ix, iy, Rectangle(bot_left, bot_left + size)

class QuadTree:
    def __init__(self, rect: Rectangle):
        assert rect.size().x == rect.size().y
        
        self.rectangle = rect
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
    
    def init_children(self):
        for ix, iy, rect in split_rectangle(self.rectangle):
            i = ix + iy * SPLIT_CONST
            if self.children[i] is None:
                self.children[i] = QuadTree(rect)
    
    def clear_children(self):
        for i, ch in enumerate(self.children):
            if ch is None:
                continue
            if len(ch.sprites) == 0 and ch.childless():
                del ch
                self.children[i] = None

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
        if not self.rectangle.contains(s):
            return None
        
        for ch in self.iter_children():
            t = ch.get_quad_tree(s)
            if t is not None:
                return t
        return self
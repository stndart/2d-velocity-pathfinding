from multipledispatch import dispatch
from typing import TypeVar, Iterable, Optional

T = TypeVar('T')
def get_matching_item(container: Iterable[T], item: T) -> Optional[T]:
    return next((x for x in container if x == item), None)

class GraphVertex:
    def __init__(self):
        self.edges: dict['GraphEdge', float] = dict()
    
    def __copy__(self):
        raise TypeError(f"Copying of {self.__class__.__name__} is not allowed")

    def __deepcopy__(self, memo):
        raise TypeError(f"Deep copying of {self.__class__.__name__} is not allowed")
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other: 'GraphVertex') -> bool:
        return id(self) == id(other)
    
    def add_edge_to(self, other: 'GraphVertex', cost: float = 1):
        """
        Adds an edge to this vertex's edge list.
        If vertices are already connected, overwrites edge cost.
        """
        new_edge = GraphEdge(self, other)
        self.edges[new_edge] = cost
    
    def has_edge_to(self, other: 'GraphVertex'):
        new_edge = GraphEdge(self, other)
        return new_edge in self.edges
    
    def cost(self, other: 'GraphVertex'):
        return self.edges.get(GraphEdge(self, other), float('inf'))
    
    def remove_edge_to(self, other: 'GraphVertex'):
        self.edges.pop(GraphEdge(self, other))

class GraphEdge:
    def __init__(self, v1: GraphVertex, v2: GraphVertex, cost: float = 1):
        self.v1 = v1
        self.v2 = v2
        
        assert cost >= 0
        self.cost = cost
    
    def __copy__(self):
        raise TypeError(f"Copying of {self.__class__.__name__} is not allowed")

    def __deepcopy__(self, memo):
        raise TypeError(f"Deep copying of {self.__class__.__name__} is not allowed")
    
    def __hash__(self):
        return id(self.v1) + id(self.v2)
    
    def __eq__(self, other: 'GraphEdge') -> bool:
        if not isinstance(other, GraphEdge):
            return False
        
        return self.v1 is other.v1 and self.v2 is other.v2
    
    def other(self, other: GraphVertex):
        return self.v2 if self.v1 is other else self.v1
    
    def __repr__(self):
        return f'Edge: {self.v1} -> {self.v2}'

class Graph:
    """
    Undirected graph
    """
    def __init__(self, vertexes: set[GraphVertex] = set()):
        self.vertexes = vertexes
    
    def add_vertex(self, vertex: GraphVertex):
        v_replace = get_matching_item(self.vertexes, vertex)
        v_replace = v_replace if v_replace else vertex

        # fixing edges
        new_edges = dict()
        for edge in vertex.edges:
            if edge.v1 is vertex and get_matching_item(self.vertexes, edge.v2):
                new_edge = GraphEdge(v_replace, get_matching_item(self.vertexes, edge.v2))
            elif edge.v2 is vertex and get_matching_item(self.vertexes, edge.v1):
                new_edge = GraphEdge(get_matching_item(self.vertexes, edge.v1), v_replace)
            else:
                raise ValueError(f"Vertex {vertex} has an edge with no connection to itself")
            new_edges[new_edge] = vertex.edges[edge]
        
        v_replace.edges.update(new_edges)
        self.vertexes.add(vertex)
        
    def remove_vertex(self, vertex: GraphVertex):
        for e in vertex.edges:
            e.other(vertex).remove_edge_to(vertex)
        self.vertexes.remove(vertex)
    
    @dispatch(GraphVertex, GraphVertex, cost=float)
    def add_edge(self, v1: GraphVertex, v2: GraphVertex, cost: float = 1.0):
        self.add_vertex(v1)
        self.add_vertex(v2)
        v1, v2 = get_matching_item(self.vertexes, v1), get_matching_item(self.vertexes, v2)
        v1.add_edge_to(v2, cost)
        v2.add_edge_to(v1, cost)
    
    @dispatch(GraphEdge, cost=float)
    def add_edge(self, e: GraphEdge, cost: float = 1.0):
        self.add_edge(e.v1, e.v2, cost=cost)

class DirectedGraph(Graph):
    """
    Directed graph
    """
    
    @dispatch(GraphVertex, GraphVertex, cost=float)
    def add_edge(self, v1: GraphVertex, v2: GraphVertex, cost: float = 1.0):
        v1.add_edge_to(v2, cost)
        self.vertexes.add(v1)
        self.vertexes.add(v2)
    
    @dispatch(GraphEdge, cost=float)
    def add_edge(self, e: GraphEdge, cost: float = 1.0):
        self.add_edge(e.v1, e.v2, cost=cost)
    

if __name__ == '__main__':
    from random import random
    G = DirectedGraph()
    vs = {GraphVertex(): i for i in range(5)}
    for v1 in vs:
        G.add_vertex(v1)
        for v2 in vs:
            if v1 is v2:
                continue
            if v1.has_edge_to(v2):
                continue
            if random() < 0.2:
                #G.add_edge(v1, v2, cost=random())
                G.add_edge(GraphEdge(v1, v2), cost=random())
    for v in G.vertexes:
        print(f'{vs[v]}: ', [vs[e.other(v)] for e in v.edges])
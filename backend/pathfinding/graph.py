from multipledispatch import dispatch

class GraphVertex:
    def __init__(self):
        self.edges: dict['GraphEdge', float] = dict()
    
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
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other: 'GraphVertex'):
        return id(self) == id(other)

class GraphEdge:
    def __init__(self, v1: GraphVertex, v2: GraphVertex):
        self.v1 = v1
        self.v2 = v2
    
    def __hash__(self):
        return id(self.v1) + id(self.v2)
    
    def __eq__(self, other: 'GraphEdge'):
        return self.v1 is other.v1 and self.v2 is other.v2
    
    def other(self, other: GraphVertex):
        return self.v2 if self.v1 is other else self.v1

class Graph:
    '''
    Undirected graph
    '''
    def __init__(self, vertexes: set[GraphVertex] = set()):
        self.vertexes = vertexes
    
    def add_vertex(self, vertex: GraphVertex):
        self.vertexes.add(vertex)
        
    def remove_vertex(self, vertex: GraphVertex):
        for e in vertex.edges:
            e.other(vertex).remove_edge_to(vertex)
        self.vertexes.remove(vertex)
    
    @dispatch(GraphVertex, GraphVertex, cost=float)
    def add_edge(self, v1: GraphVertex, v2: GraphVertex, cost: float = 1.0):
        v1.add_edge_to(v2, cost)
        v2.add_edge_to(v1, cost)
        self.vertexes.add(v1)
        self.vertexes.add(v2)
    
    @dispatch(GraphEdge, cost=float)
    def add_edge(self, e: GraphEdge, cost: float = 1.0):
        self.add_edge(e.v1, e.v2, cost=cost)

class DirectedGraph(Graph):
    '''
    Directed graph
    '''
    
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
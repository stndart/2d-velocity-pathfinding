from .graph import Graph, GraphEdge as Edge, GraphVertex as Vertex

class Pathfinder:
    def __init__(self, g: Graph):
        self.graph = g
    
    def find_path(self, start: Vertex, end: Vertex) -> list[Vertex]:
        return []
    
    def update_shortest_paths(self, start: Vertex):
        """
        Updates shortest paths from start to all other vertexes in the graph
        """
        pass

    def preprocess_paths(self):
        """
        Makes preprocessing if algorithm requires it
        """
        pass

class Dijkstra(Pathfinder):
    def __init__(self, g: Graph):
        super().__init__(g)
    
    def find_path(self, start: Vertex, end: Vertex):
        """
        Finds path from start to end using Dijkstra algorithm
        """
        if start not in self.graph.vertexes or end not in self.graph.vertexes:
            raise RuntimeError("Vertexes not in graph")
        
        if start is end:
            return [start]
        
        dist = {v: float('inf') for v in self.graph.vertexes}
        prev = {v: None for v in self.graph.vertexes}
        dist[start] = 0
        
        Q = set(self.graph.vertexes)
        
        while Q:
            u = min(Q, key=lambda v: dist[v])
            Q.remove(u)
            
            if u is end:
                path = []
                while u is not None:
                    path.append(u)
                    u = prev[u]
                return path[::-1]
            
            for e in u.edges:
                v = e.other(u)
                alt = dist[u] + e.cost
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
        
        return []

class Floyd(Pathfinder):
    def __init__(self, g: Graph):
        super().__init__(g)

        self.dist = dict()
        self.pred = dict()

        self.preprocess_paths()
    
    def preprocess_paths(self):
        """
        Fills .dist and .pred with shortest paths between all vertexes with Floyd algorithm
        """

        for u in self.graph.vertexes:
            self.dist[u] = {v: float('inf') for v in self.graph.vertexes}
            self.pred[u] = {v: None for v in self.graph.vertexes}
            self.dist[u][u] = 0

            for e in u.edges:
                v = e.other(u)
                self.dist[u][v] = e.cost
                self.pred[u][v] = u

        for k in self.graph.vertexes:
            for i in self.graph.vertexes:
                for j in self.graph.vertexes:
                    if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.pred[i][j] = self.pred[k][j]
        
    def find_path(self, start: Vertex, end: Vertex) -> list[Vertex]:
        """
        Restores path from preprocessed .pred
        """

        if start not in self.graph.vertexes or end not in self.graph.vertexes:
            raise RuntimeError("Vertexes not in graph")

        if start not in self.dist:
            self.preprocess_paths()

        path = []
        if self.dist[start][end] == float('inf'):
            return path  # No path exists

        current = end
        while current != start:
            if current is None:
                return []  # No path exists
            path.insert(0, current)
            current = self.pred[start][current]

        path.insert(0, start)
        return path
    
    def update_shortest_paths(self, start: Vertex):
        """
        Updates shortest paths from start to all other vertexes in the graph
        """

        if start not in self.graph.vertexes:
            raise RuntimeError("Vertex not in graph")

        if start not in self.dist:
            self.dist[start] = {v: float('inf') for v in self.graph.vertexes}
            self.pred[start] = {v: None for v in self.graph.vertexes}
            self.dist[start][start] = 0

            for e in start.edges:
                v = e.other(start)
                self.dist[start][v] = e.cost
                self.pred[start][v] = start

        for i in self.graph.vertexes:
            for j in self.graph.vertexes:
                if self.dist[i][j] > self.dist[i][start] + self.dist[start][j]:
                    self.dist[i][j] = self.dist[i][start] + self.dist[start][j]
                    self.pred[i][j] = self.pred[start][j]
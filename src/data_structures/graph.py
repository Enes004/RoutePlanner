class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        """Durağı sisteme ekler."""
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u, v, weight):
        """İki durak arasında bağlantı kurar."""
        self.add_node(u)
        self.add_node(v)
        # Liste içinde tuple tutuyoruz: (komşu, süre)
        if (v, weight) not in self.adj_list[u]:
            self.adj_list[u].append((v, weight))
        if (u, weight) not in self.adj_list[v]:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, node):
        """Komşuları liste olarak döndürür."""
        return self.adj_list.get(node, [])
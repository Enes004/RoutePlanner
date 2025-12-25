class Graph:
    def __init__(self):
        #{ "Durak İsmi": [ (Komşu, Mesafe), (Diğer Komşu, Mesafe) ] }
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = [] # "Üsküdar" satırını aç, komşuları henüz boş kalsın.

    def add_edge(self, u, v, weight):
        #Önce durakları ekle
        self.add_node(u)
        self.add_node(v)

        #Birbirlerine komşuluklarını ve ağırlıklarını ekle
        if (v, weight) not in self.adj_list[u]:
            self.adj_list[u].append((v, weight))

        if (u, weight) not in self.adj_list[v]:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, node):
        return self.adj_list.get(node, [])
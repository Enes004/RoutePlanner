from src.graph import graph

g = graph()
g.load_from_json("data/stations.json")

g.print_graph()
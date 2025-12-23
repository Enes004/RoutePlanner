from src.models import Station
import json
import heapq

class graph:
    def __init__(self):
        self.adj_list = {}
        self.stations = {}

    def add_station(self, station: Station):
        self.stations[station.id] = station
        self.adj_list[station.id] = {}


    def add_route(self, from_id, to_id, duration):
        self.adj_list[from_id][to_id] = duration

    def get_neighbors(self, node_id):
        return self.adj_list[node_id]
    
    def get_station(self, id):
        return self.stations[id]
    
    def has_station(self, id):
        return id in self.stations
    
    def print_graph(self):
        for sid, neighbors in self.adj_list.items():
            print(f"{sid} -> {neighbors}")

    def load_from_json(self, path):
        with open(path, "r") as f:
            data = json.load(f)

        for s in data["stations"]:
            st = Station(
                s["id"],
                s["name"],
                s["x_loc"],
                s["y_loc"]
            )
            self.add_station(st)

        for s in data["stations"]:
            sid = s["id"]
            for n in s["neighbors"]:
                self.add_route(sid, n["id"], n["duration"])     

    def shortest_path(self, start_node, end_node):
        distances = {node: float('inf') for node in self.adj_list}
        distances[start_node] = 0

        previous_nodes = {node: None for node in self.adj_list}

        priority_queue_list = [(0, start_node)]

        while priority_queue_list:
            curr_weight, curr_node = heapq.heappop(priority_queue_list)

            if curr_weight > distances[curr_node]:
                continue

            if curr_node == end_node:
                break

            for neighbor, weight in self.adj_list[curr_node].items():
                new_dist = curr_weight + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_nodes[neighbor] = curr_node
                    heapq.heappush(priority_queue_list, (new_dist, neighbor))

        path = []
        node = end_node
        while node is not None:
            path.append(node)
            node = previous_nodes[node]

        path.reverse()
        return path, distances[end_node]        
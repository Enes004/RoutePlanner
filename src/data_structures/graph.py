from src.models import Station
import json

class Graph: 
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
        with open(path, "r", encoding='utf-8') as f: # utf-8 eklemek Türkçe karakterler için önemli
            data = json.load(f)

        for s in data["stations"]:
            st = Station(s["id"], s["name"], s["x_loc"], s["y_loc"])
            self.add_station(st)

        for s in data["stations"]:
            sid = s["id"]
            for n in s["neighbors"]:
                self.add_route(sid, n["id"], n["duration"])
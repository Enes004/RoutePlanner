class Station:
    def __init__(self,id,name,x_loc,y_loc):
        self.id = id
        self.name = name
        self.location = (x_loc,y_loc)
        self.neighbors = {}

    def add_neighbor(self,neighbor_id,duration):
        self.neighbors[neighbor_id]=duration
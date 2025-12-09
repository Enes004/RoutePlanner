class Station:
    def __init__(self,id,name,x,y):
        self.id = id
        self.name = name
        self.location = (x,y)
        self.neighbors = {}
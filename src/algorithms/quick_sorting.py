
class StationSorter:
    def __init__(self):
        pass
    
    def quick_sort_stations(self,stations_in_json):

        if len(stations_in_json)<=1:
            return stations_in_json
        
        pivot_index = len(stations_in_json)//2              
        pivot_station = stations_in_json[pivot_index]   ## Choose the middle element of the list
        pivot_name = pivot_station.name.lower() ## Sort alphabetically and convert to lowercase for ASCII-based comparison

        # list compherations
        left = [station_object for station_object in stations_in_json if station_object.name.lower() < pivot_name]
        middle = [station_object for station_object in stations_in_json if station_object.name.lower() == pivot_name]
        right =  [station_object for station_object in stations_in_json if station_object.name.lower() > pivot_name]

        return self.quick_sort_stations(left) + middle + self.quick_sort_stations(right)

#Json dosyasındaki karmaşık verileri alfabetik olarak sıralayıp binary searche hazırlar

class StationSorter:
    def __init__(self):
        pass
    
    def quick_sort_stations(self,stations_in_json):

        #Bir eleman veya hiç eleman kalınca recursive'i bitir. (Çıkış noktamız)
        if len(stations_in_json)<=1:
            return stations_in_json
        
        pivot_index = len(stations_in_json)//2              
        pivot_station = stations_in_json[pivot_index]   ## Choose the middle element of the list
        pivot_name = pivot_station.name.lower() ## Sort alphabetically and convert to lowercase for ASCII-based comparison

        #İsmi alfabetik olarak pivot isminden küçük/önce olanlar.
        left = [station_object for station_object in stations_in_json if station_object.name.lower() < pivot_name]

        #İsmi pivot ile aynı olanlar.
        middle = [station_object for station_object in stations_in_json if station_object.name.lower() == pivot_name]

        #İsmi alfabetik olarak pivot isminden büyük/sonra olanlar.
        right =  [station_object for station_object in stations_in_json if station_object.name.lower() > pivot_name]

        #Recursive şekilde bir veya birden az kalana kadar her kutuda devam et
        return self.quick_sort_stations(left) + middle + self.quick_sort_stations(right)
        # (A B C) (D) (E F)
        # (A)(B)(C)-(D)-(E)-(F)
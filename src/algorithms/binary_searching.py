
class StationSearcher:
    def __init__(self):
        pass

    def Binary_Search(self,sorted_list,target_name):

        target_name = target_name.lower()
        left = 0
        right = len(sorted_list)-1

        while (left <= right):
            mid = (left+right)//2
            current_station = sorted_list[mid]
            current_name = current_station.name.lower()

            if current_name == target_name:
                return current_station
            
            elif current_name < target_name:
                left = mid+1

            else:
                right = mid-1

        return None



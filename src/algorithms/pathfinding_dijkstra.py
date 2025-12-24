import heapq

class PathFinder:
    def __init__(self):
        pass

    def dijkstra(self, graph_obj, start_node, end_node):
        # Durak isimlerini kontrol et (KeyError önlemi)
        if start_node not in graph_obj.adj_list or end_node not in graph_obj.adj_list:
            return None, float('inf')

        distances = {node: float('inf') for node in graph_obj.adj_list}
        distances[start_node] = 0
        previous_nodes = {node: None for node in graph_obj.adj_list}
        priority_queue = [(0, start_node)]

        while priority_queue:
            curr_weight, curr_node = heapq.heappop(priority_queue)

            if curr_weight > distances[curr_node]:
                continue
            if curr_node == end_node:
                break

            # DÜZELTME: .items() silindi çünkü get_neighbors bir liste döndürüyor
            for neighbor, weight in graph_obj.get_neighbors(curr_node):
                new_dist = curr_weight + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_nodes[neighbor] = curr_node
                    heapq.heappush(priority_queue, (new_dist, neighbor))

        path = []
        node = end_node
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        path.reverse()

        return path, distances[end_node]
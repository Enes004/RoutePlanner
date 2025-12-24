import json

def load_metro_data(json_path, graph, trie):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        id_to_name = {s['id']: s['name'] for s in data['stations']}

        for station in data['stations']:
            name = station['name']
            trie.insert(name)
            graph.add_node(name)

        for station in data['stations']:
            u_name = station['name']
            for neighbor_info in station['neighbors']:
                v_name = id_to_name[neighbor_info['id']]
                duration = neighbor_info['duration']
                graph.add_edge(u_name, v_name, duration)
        
        return data
    except Exception as e:
        print(f"!!! [HATA] Veri yüklenirken bir şeyler ters gitti: {e} !!!")
        return None
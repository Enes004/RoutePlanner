import tkinter as tk
from tkinter import ttk
from src.graph import graph

# Grafı oluştur ve JSON'dan yükle
g = graph()
g.load_from_json("data/stations.json")

def find_path():
    try:
        # Kullanıcının seçtiği isimleri ID'ye çevir
        start_name = start_var.get()
        end_name = end_var.get()

        # isim -> id
        start_id = name_to_id[start_name]
        end_id = name_to_id[end_name]

        path, cost = g.shortest_path(start_id, end_id)
        path_names = [g.get_station(sid).name for sid in path]
        result_label.config(text=f"Path: {' -> '.join(path_names)}\nTotal duration: {cost} minutes")

    except Exception as e:
        result_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("Route Planner")

start_var = tk.StringVar()
end_var = tk.StringVar()

# Station isimlerini listele
station_names = [station.name for station in g.stations.values()]
name_to_id = {station.name: station.id for station in g.stations.values()}

tk.Label(root, text="Select Start Station:").pack()
start_combo = ttk.Combobox(root, values=station_names, textvariable=start_var)
start_combo.pack()

tk.Label(root, text="Select End Station:").pack()
end_combo = ttk.Combobox(root, values=station_names, textvariable=end_var)
end_combo.pack()

tk.Button(root, text="Find Shortest Path", command=find_path).pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

root.mainloop()

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.graph import graph

# Grafı oluştur ve JSON'dan yükle
g = graph()
g.load_from_json("data/stations.json")

root = tk.Tk()
root.title("Route Planner")

start_var = tk.StringVar()
end_var = tk.StringVar()

station_names = [station.name for station in g.stations.values()]
name_to_id = {station.name: station.id for station in g.stations.values()}

tk.Label(root, text="Select Start Station:").pack()
start_combo = ttk.Combobox(root, values=station_names, textvariable=start_var)
start_combo.pack()

tk.Label(root, text="Select End Station:").pack()
end_combo = ttk.Combobox(root, values=station_names, textvariable=end_var)
end_combo.pack()

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(6,6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def draw_graph(path=[]):
    ax.clear()
    # Durakları çiz
    for station in g.stations.values():
        x, y = station.location
        ax.plot(x, y, 'o', color='blue')
        ax.text(x+0.5, y+0.5, station.name, fontsize=8)

    # Hatları çiz
    for sid, neighbors in g.adj_list.items():
        sx, sy = g.get_station(sid).location
        for nid in neighbors:
            nx, ny = g.get_station(nid).location
            ax.plot([sx, nx], [sy, ny], color='gray', linewidth=1)

    # Shortest path varsa vurgula
    if path:
        for i in range(len(path)-1):
            sx, sy = g.get_station(path[i]).location
            nx, ny = g.get_station(path[i+1]).location
            ax.plot([sx, nx], [sy, ny], color='red', linewidth=2)

    ax.set_title("Route Planner Map")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    canvas.draw()

def find_path():
    try:
        start_name = start_var.get()
        end_name = end_var.get()
        start_id = name_to_id[start_name]
        end_id = name_to_id[end_name]

        path, cost = g.shortest_path(start_id, end_id)
        path_names = [g.get_station(sid).name for sid in path]
        result_label.config(text=f"Path: {' -> '.join(path_names)}\nTotal duration: {cost} minutes")
        draw_graph(path)

    except Exception as e:
        result_label.config(text=f"Error: {e}")

tk.Button(root, text="Find Shortest Path", command=find_path).pack(pady=10)

draw_graph()  # başlangıçta tüm grafı çiz

root.mainloop()

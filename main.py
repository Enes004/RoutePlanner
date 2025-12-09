from src.graph import graph
from src.ui import root  # ui.py içinde root = tk.Tk() tanımlı olduğunu varsayıyoruz

g = graph()
g.load_from_json("data/stations.json")

g.print_graph()

    # En kısa yolu test et
start = 1
end = 4
path, cost = g.shortest_path(start, end)
print(f"\nShortest path from {start} to {end}: {path}")
print(f"Total cost: {cost}")

if __name__ == "__main__":
    root.mainloop()
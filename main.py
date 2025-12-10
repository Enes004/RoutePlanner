from src.graph import graph
from src.ui import root 

g = graph()
g.load_from_json("data/stations.json")

print("Graf Yüklendi.")

# --- DÜZELTİLEN KISIM ---
# ID'leri JSON dosyasındaki mevcut ID'lerden seçtik
# 501: Üsküdar (M5)
# 112: Sabiha Gökçen (M4)
start = 501 
end = 112   

# Hata kontrolü ekleyelim ki program patlamasın
if g.has_station(start) and g.has_station(end):
    path, cost = g.shortest_path(start, end)
    print(f"\nShortest path from {start} to {end}: {path}")
    print(f"Total cost: {cost}")
else:
    print("\nHATA: Seçilen ID'ler JSON dosyasında bulunamadı!")

if __name__ == "__main__":
    root.mainloop()
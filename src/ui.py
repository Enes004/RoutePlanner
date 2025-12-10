import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.graph import graph  # Senin graph sınıfını çekiyoruz

# --- AYARLAR ---
plt.style.use('dark_background')  # Matplotlib karanlık mod

# 1. Grafiği Burada Oluşturuyoruz (Main.py buradan çekecek)
g = graph()
g.load_from_json("data/stations.json")

# 2. Ana Pencere Ayarları
root = tk.Tk()
root.title("Istanbul Metro Route Planner")
root.configure(bg='black')  # Arka plan siyah
root.geometry("1300x850")

# Değişkenler
start_var = tk.StringVar()
end_var = tk.StringVar()

# İstasyon isimlerini al ve sırala
# Senin graph yapında stations bir sözlük {id: StationObj}
station_names = sorted([s.name for s in g.stations.values()])
# İsimden ID bulmak için ters sözlük
name_to_id = {s.name: s.id for s in g.stations.values()}

# --- ÜST PANEL (SEÇİMLER) ---
top_frame = tk.Frame(root, bg='black')
top_frame.pack(side=tk.TOP, fill=tk.X, pady=20)

# Start Label & Combo
lbl_start = tk.Label(top_frame, text="BAŞLANGIÇ DURAĞI:", font=("Arial", 14, "bold"), fg="red", bg="black")
lbl_start.pack(side=tk.LEFT, padx=20)

start_combo = ttk.Combobox(top_frame, values=station_names, textvariable=start_var, width=25, font=("Arial", 11))
start_combo.pack(side=tk.LEFT, padx=5)

# End Label & Combo
lbl_end = tk.Label(top_frame, text="BİTİŞ DURAĞI:", font=("Arial", 14, "bold"), fg="red", bg="black")
lbl_end.pack(side=tk.LEFT, padx=20)

end_combo = ttk.Combobox(top_frame, values=station_names, textvariable=end_var, width=25, font=("Arial", 11))
end_combo.pack(side=tk.LEFT, padx=5)

# Sonuç Label'ı
result_label = tk.Label(root, text="Lütfen durak seçiniz...", font=("Consolas", 14, "bold"), fg="#00FF00", bg="black", wraplength=1000)
result_label.pack(pady=10)

# --- MATPLOTLIB GRAFİK ALANI ---
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def draw_graph(path=[]):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    # Senin graph yapında adj_list formatı: {from_id: {to_id: duration}}
    # ve stations formatı: {id: StationObj}

    drawn_edges = set()

    # 1. Hatları Çiz
    for from_id, neighbors in g.adj_list.items():
        start_node = g.stations[from_id]
        sx, sy = start_node.location

        for to_id, duration in neighbors.items():
            end_node = g.stations[to_id]
            nx, ny = end_node.location

            # Çizgiyi tek sefer çizmek için kontrol
            edge_key = tuple(sorted((from_id, to_id)))
            if edge_key not in drawn_edges:
                ax.plot([sx, nx], [sy, ny], color='#00FFFF', linewidth=2, alpha=0.5, zorder=1) # Cyan renk
                drawn_edges.add(edge_key)

    # 2. Durakları Çiz
    for station in g.stations.values():
        x, y = station.location
        # Beyaz nokta
        ax.plot(x, y, 'o', color='white', markersize=6, zorder=5)
        # İsim (M5 vb detayları atıp sadece ismi yazabiliriz veya hepsini yazabiliriz)
        display_name = station.name.split('(')[0].strip()
        ax.text(x + 0.4, y + 0.4, display_name, color='white', fontsize=8, zorder=10)

    # 3. Rota Varsa Üzerine Çiz
    if path:
        path_x = []
        path_y = []
        for sid in path:
            st = g.stations[sid]
            path_x.append(st.location[0])
            path_y.append(st.location[1])
        
        # Rotayı Kırmızı Çiz
        ax.plot(path_x, path_y, color='red', linewidth=4, alpha=0.9, zorder=6)
        ax.plot(path_x, path_y, 'o', color='red', markersize=8, zorder=7)

    canvas.draw()

def find_path():
    try:
        s_name = start_var.get()
        e_name = end_var.get()
        
        if not s_name or not e_name:
            result_label.config(text="Lütfen iki durak seçin!", fg="red")
            return

        start_id = name_to_id[s_name]
        end_id = name_to_id[e_name]

        # Senin graph.py içindeki metodun: return path, distances[end_node]
        path, cost = g.shortest_path(start_id, end_id)

        if cost == float('inf'):
            result_label.config(text="Rota bulunamadı!", fg="red")
        else:
            # İsimleri al
            path_names = [g.stations[sid].name for sid in path]
            route_str = " -> ".join(path_names)
            result_label.config(text=f"ROTA BULUNDU ({cost} dk)\n{route_str}", fg="#00FF00")
            draw_graph(path)

    except Exception as e:
        result_label.config(text=f"Hata: {e}", fg="red")
        print(f"UI Hatası: {e}")

# Buton
btn_find = tk.Button(top_frame, text="ROTAYI HESAPLA", command=find_path, 
                     bg="red", fg="white", font=("Arial", 12, "bold"), padx=10)
btn_find.pack(side=tk.LEFT, padx=30)

# İlk açılışta boş haritayı çiz
draw_graph()
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
# Matplotlib'in backend'ini ayarlıyoruz ki çökme yapmasın
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- KENDİ YAPILARIMIZI ÇEKİYORUZ ---
from src.data_structures.graph import Graph
from src.data_structures.trie import Trie
from src.data_structures.stack import Stack
from src.algorithms.pathfinding_dijkstra import PathFinder
from src.algorithms.bfs_pathfinding import find_path_bfs
from src.utils.data_loader import load_metro_data

class MetroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("İstanbul Metro - AI Route Planner")
        self.root.geometry("1400x900")
        self.root.configure(bg='black')

        # 1. SİSTEMLERİN BAŞLATILMASI
        self.graph = Graph()
        self.trie = Trie()
        self.history_stack = Stack()
        
        # Veriyi yükle (main.py'den bağımsız çalışabilmesi için burada da yüklüyoruz)
        try:
            self.raw_data = load_metro_data("data/stations.json", self.graph, self.trie)
            if not self.raw_data: raise Exception("Veri boş")
        except:
            print("Veri yüklenemedi, ui.py tek başına çalıştırılmış olabilir.")
            self.raw_data = {'stations': []} # Boş veri ile başlat ki çökmesin

        # İstasyon isimlerini sırala
        raw_names = [s['name'] for s in self.raw_data['stations']]
        self.sorted_stations = sorted(raw_names)

        # Koordinatları hızlı çekmek için bir sözlük: {'İsim': (x, y)}
        self.coords = {s['name']: (s['x_loc'], s['y_loc']) for s in self.raw_data['stations']}

        self.setup_ui()

    def setup_ui(self):
        # --- ÜST PANEL (SEÇİMLER) ---
        top_frame = tk.Frame(self.root, bg='black', highlightbackground="#333", highlightthickness=1)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        # Başlangıç (Trie Destekli)
        tk.Label(top_frame, text="NEREDEN:", font=("Consolas", 12, "bold"), fg="#00FF00", bg="black").pack(side=tk.LEFT, padx=10)
        self.start_combo = ttk.Combobox(top_frame, values=self.sorted_stations, width=30)
        self.start_combo.pack(side=tk.LEFT, padx=5)
        # Her tuş bırakıldığında Trie kontrolü yap
        self.start_combo.bind('<KeyRelease>', lambda e: self.check_trie(e, self.start_combo))

        # Bitiş (Trie Destekli)
        tk.Label(top_frame, text="NEREYE:", font=("Consolas", 12, "bold"), fg="#FF0000", bg="black").pack(side=tk.LEFT, padx=10)
        self.end_combo = ttk.Combobox(top_frame, values=self.sorted_stations, width=30)
        self.end_combo.pack(side=tk.LEFT, padx=5)
        self.end_combo.bind('<KeyRelease>', lambda e: self.check_trie(e, self.end_combo))

        # Butonlar
        tk.Button(top_frame, text="EN HIZLI (Dijkstra)", command=self.calculate_dijkstra, bg="#0055ff", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="EN AZ DURAK (BFS)", command=self.calculate_bfs, bg="#ffaa00", fg="black", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        # --- ORTA ALAN (HARİTA VE GEÇMİŞ) ---
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SOL: GEÇMİŞ PANELİ (STACK)
        history_frame = tk.Frame(main_frame, bg='#111', width=250, highlightbackground="#444", highlightthickness=1)
        history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        tk.Label(history_frame, text="GEÇMİŞ ARAMALAR\n(Tekrar çizmek için tıkla)", font=("Consolas", 10, "bold"), fg="cyan", bg="#111").pack(pady=5)
        
        # Listbox ve Scrollbar
        list_scroll = tk.Scrollbar(history_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, bg='black', fg='cyan', font=("Consolas", 9), borderwidth=0, highlightthickness=0, yscrollcommand=list_scroll.set)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        list_scroll.config(command=self.history_listbox.yview)
        
        # DÜZELTME 4: Stack'e tıklayınca rotayı tekrar çiz
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_click)


        # SAĞ: HARİTA (MATPLOTLIB)
        # Figure oluştururken facecolor'ı siyah yapıyoruz
        self.fig = Figure(figsize=(10, 6), facecolor='black')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ALT: SONUÇ PANELİ
        self.result_label = tk.Label(self.root, text="Sistem Hazır. Lütfen durak seçiniz...", font=("Consolas", 12), fg="#00FF00", bg="black", wraplength=1300)
        self.result_label.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        # İlk açılışta boş haritayı çiz
        self.draw_map()

    # --- DÜZELTME 2: Trie Anlık Arama ---
    def check_trie(self, event, combo):
        """Kullanıcı yazdıkça Trie üzerinden öneri sunar ve listeyi açar."""
        # Enter, yön tuşları gibi tuşlarda tetiklenme
        if event.keysym in ['Return', 'Down', 'Up', 'Left', 'Right']:
            return

        typed_text = combo.get()
        
        if typed_text == '':
            combo['values'] = self.sorted_stations
        else:
            # Trie'den önerileri al
            suggestions = self.trie.get_suggestions(typed_text)
            if suggestions:
                combo['values'] = suggestions
                # KRİTİK DÜZELTME: Listeyi programatik olarak aç
                combo.event_generate('<Down>') 
            else:
                 # Öneri yoksa listeyi boşalt ama yazdığı kalsın
                combo['values'] = []

    # --- DÜZELTME 4: Geçmişe Tıklama ---
    def on_history_click(self, event):
        """Listbox'tan bir öğeye tıklandığında rotayı tekrar hesaplar ve çizer."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index) # Örn: "Kadikoy(M4) -> Sabiha Gokcen(M4)"
            
            try:
                start, end = data.split(" -> ")
                # Hızlıca tekrar hesapla (Dijkstra varsayalım görselleştirme için)
                finder = PathFinder()
                path, cost = finder.dijkstra(self.graph, start, end)
                if path:
                    self.update_result(path, f"Geçmişten Yüklendi: {cost} dk (Dijkstra)", "cyan")
                    # Comboboxları da güncelle
                    self.start_combo.set(start)
                    self.end_combo.set(end)
            except:
                pass # Hatalı format varsa görmezden gel

    def calculate_dijkstra(self):
        start = self.start_combo.get()
        end = self.end_combo.get()
        
        if start not in self.coords or end not in self.coords:
             self.result_label.config(text="HATA: Lütfen listeden geçerli duraklar seçiniz!", fg="red")
             return

        finder = PathFinder()
        # Burada hata yakalama ekleyelim
        try:
            path, cost = finder.dijkstra(self.graph, start, end)
            if path:
                self.update_result(path, f"En Hızlı Yol: {cost} dk", "#00FF00")
                self.add_to_history(f"{start} -> {end}")
            else:
                self.result_label.config(text="Rota bulunamadı!", fg="red")
        except Exception as e:
             self.result_label.config(text=f"Hata oluştu: {e}", fg="red")

    def calculate_bfs(self):
        start = self.start_combo.get()
        end = self.end_combo.get()

        if start not in self.coords or end not in self.coords:
             self.result_label.config(text="HATA: Lütfen listeden geçerli duraklar seçiniz!", fg="red")
             return
             
        path = find_path_bfs(self.graph, start, end)
        
        if path:
            self.update_result(path, f"En Az Durak: {len(path)} İstasyon", "orange")
            self.add_to_history(f"{start} -> {end}")
        else:
            self.result_label.config(text="Rota bulunamadı!", fg="red")

    def update_result(self, path, info, color):
        # Rota stringini oluştur
        route_str = ' -> '.join(path)
        self.result_label.config(text=f"{info}\n{route_str}", fg=color)
        self.draw_map(path)

    def add_to_history(self, entry):
        # Stack'e ekle
        self.history_stack.push(entry)
        # Listbox'ı güncelle
        self.history_listbox.delete(0, tk.END)
        # Stack'i tersten yazdır ki en son arama en üstte olsun
        for item in reversed(self.history_stack.items[-15:]): # Son 15 arama
            self.history_listbox.insert(tk.END, item)

    def draw_map(self, path=[]):
        self.ax.clear()
        self.ax.axis('off')

        # Tüm Hatları Çiz (Arka plan çizgileri - Cyan)
        drawn_edges = set()
        for u, neighbors in self.graph.adj_list.items():
            if u not in self.coords: continue
            ux, uy = self.coords[u]
            for v, _ in neighbors:
                if v not in self.coords: continue
                vx, vy = self.coords[v]
                
                edge = tuple(sorted((u, v)))
                if edge not in drawn_edges:
                    self.ax.plot([ux, vx], [uy, vy], color='#00FFFF', alpha=0.2, linewidth=1, zorder=1)
                    drawn_edges.add(edge)

        # --- DÜZELTME 1: Durak İsimleri (Labels) ---
        for name, (x, y) in self.coords.items():
            # Durağı çiz
            self.ax.plot(x, y, 'o', color='white', markersize=4, alpha=0.6, zorder=2)
            # İsmi yaz (x'in biraz sağına, y'nin biraz yukarısına)
            # İsmin sadece ilk kısmını alalım ki harita boğulmasın (örn: "Kadıköy(M4)" -> "Kadıköy")
            display_name = name.split('(')[0]
            self.ax.text(x + 0.5, y + 0.5, display_name, color='white', fontsize=7, alpha=0.8, zorder=3)


        # --- DÜZELTME 3: Kırmızı Rota Çizgileri ---
        if path:
            # 1. Rota üzerindeki durakları kırmızı nokta yap
            px = [self.coords[node][0] for node in path]
            py = [self.coords[node][1] for node in path]
            self.ax.plot(px, py, 'o', color='#FF0000', markersize=7, zorder=5)

            # 2. Rota üzerindeki yolları segment segment çiz (Daha güvenli)
            for i in range(len(path) - 1):
                u_node = path[i]
                v_node = path[i+1]
                ux, uy = self.coords[u_node]
                vx, vy = self.coords[v_node]
                # İki nokta arasına kırmızı çizgi çek
                self.ax.plot([ux, vx], [uy, vy], color='#FF0000', linewidth=3, zorder=4)

        self.canvas.draw()

if __name__ == "__main__":
    # ui.py tek başına çalıştırılırsa diye bir önlem
    root = tk.Tk()
    app = MetroUI(root)
    root.mainloop()
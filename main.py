import tkinter as tk
from src.ui import MetroUI  
from src.data_structures.graph import Graph
from src.data_structures.trie import Trie
from src.utils.data_loader import load_metro_data

def main():
    """
    Programın ana giriş noktası. 
    Arka plan sistemlerini hazırlar ve Kullanıcı Arayüzünü (UI) başlatır.
    """
    
    # 1. TEMEL YAPILARIN OLUŞTURULMASI
    # Bu yapılar program açık olduğu sürece veriyi hafızada tutacak.
    metro_sistemi = Graph()
    arama_motoru = Trie()
    
    # 2. VERİ YÜKLENMESİ
    # JSON dosyasındaki durakları ve yolları Graph ve Trie içine pompalıyoruz.
    json_yolu = "data/stations.json"
    
    print("========================================")
    print("METRO SİSTEMİ BAŞLATILIYOR...")
    print("========================================")
    
    # Veri yükleme işlemi
    data = load_metro_data(json_yolu, metro_sistemi, arama_motoru)
    
    if data is None:
        print("❌ HATA: Veriler yüklenemediği için program başlatılamıyor!")
        return

    print(f"✅ Başarılı: {len(data['stations'])} durak sisteme yüklendi.")
    print("🚀 Arayüz (UI) açılıyor...")

    # 3. KULLANICI ARAYÜZÜNÜN (UI) BAŞLATILMASI
    # Tkinter ana penceresini oluşturup kontrolü MetroUI sınıfına devrediyoruz.
    root = tk.Tk()
    app = MetroUI(root)
    
    # Pencere kapanana kadar programın çalışmasını sağlar
    root.mainloop()

if __name__ == "__main__":
    main()
🚇 Istanbul Metro AI Route Planner

Bu proje, İstanbul Medeniyet Üniversitesi Veri Yapıları dersi final ödevi kapsamında geliştirilmiştir. İstanbul metro ağını bir Çizge (Graph) modeli üzerinde simüle ederek, kullanıcıya en optimize rotayı sunan bir masaüstü uygulamasıdır.
🚀 Öne Çıkan Özellikler

    Akıllı Arama (Trie): Durak isimlerini yazarken anlık otomatik tamamlama önerileri sunar.

    En Hızlı Rota (Dijkstra): İstasyonlar arasındaki süreleri dikkate alarak zaman açısından en optimize yolu hesaplar.

    En Az Durak (BFS): Mesafe fark etmeksizin kullanıcıyı en az durak geçecek şekilde hedefine ulaştırır.

    İnteraktif Harita: Seçilen rotayı koordinat sistemine dayalı bir harita üzerinde görselleştirir.

🛠️ Kullanılan Teknolojiler ve Mimari

Proje, modüler bir yapı üzerine inşa edilmiş olup algoritmalar ve veri yapıları ayrıştırılmıştır:

    Dil: Python 3.10+

    Arayüz: Tkinter (GUI)

    Veri Formatı: JSON (İstasyon ve komşuluk verileri)

Proje Klasör Yapısı
Plaintext

├── algorithms/           # Rota ve sıralama motorları
│   ├── pathfinding_dijkstra.py
│   ├── bfs_pathfinding.py
│   ├── quick_sorting.py
│   └── binary_searching.py
├── data_structures/      # Özel veri yapısı sınıfları
│   ├── graph.py
│   ├── trie.py
│   └── stack.py
├── models.py             # İstasyon nesne modelleri
└── main.py               # Uygulama giriş noktası

📊 Algoritma Analizi (Complexity)

Projede kullanılan temel operasyonların karmaşıklık değerleri şöyledir:
Algoritma	Zaman Karmaşıklığı (O)	Uzay Karmaşıklığı (O)
Dijkstra	O((V+E)logV)	O(V+E)
Trie Search	O(L)	O(N⋅L)
Quick Sort	O(NlogN)	O(logN)
BFS	O(V+E)	O(V)
⚙️ Kurulum ve Çalıştırma

    Depoyu klonlayın:
    Bash

git clone https://github.com/kullaniciadi/istanbul-metro-ai.git

Proje dizinine gidin:
Bash

cd istanbul-metro-ai

Uygulamayı çalıştırın:
Bash

    python main.py


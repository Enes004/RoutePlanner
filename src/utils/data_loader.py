import json

def load_metro_data(json_path, graph, trie):
    """
    Bu fonksiyon bizim projenin 'Giriş Kapısı'. 
    JSON'daki karışık ID'leri ve listeleri alıp, Graph ve Trie'ye 
    onların anlayacağı dilden anlatıyor.
    """
    try:
        # 1. JSON dosyasını açıyoruz (utf-8 önemli, Türkçe karakterler üzmesin)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. ID -> İsim Rehberi (Mapping)
        # Kanka burası çok kritik! JSON'da komşular ID (örn: 501) olarak verilmiş.
        # Ama biz 'Üsküdar' diye arıyoruz. Bu rehber sayesinde 501'in 
        # Üsküdar olduğunu anında bulacağız.
        id_to_name = {station['id']: station['name'] for station in data['stations']}

        # 3. İLK TUR: Önce tüm durakları sisteme bir tanıtalım.
        # Önce isimleri ekliyoruz ki birazdan bağlantı kurarken 'bu kim?' demesin.
        for station in data['stations']:
            name = station['name']
            
            # Arama motoruna (Trie) ismi fırlatıyoruz.
            trie.insert(name)
            
            # Metro ağına (Graph) durağı bir 'düğüm' olarak çakıyoruz.
            graph.add_node(name)

        # 4. İKİNCİ TUR: Şimdi o meşhur rayları (bağlantıları) döşeme vakti!
        for station in data['stations']:
            u_name = station['name'] # Başlangıç durağımız
            
            for neighbor_info in station['neighbors']:
                # Komşunun ID'sini al, rehbere bakıp ismini bul.
                v_id = neighbor_info['id']
                v_name = id_to_name[v_id]
                
                # Aradaki süreyi (dakikayı) al.
                duration = neighbor_info['duration']
                
                # Grafımıza diyoruz ki: 'U durağı ile V durağı arasında şu kadar dk var.'
                # Burası hem Dijkstra hem BFS için hayat suyunun verildiği yer.
                graph.add_edge(u_name, v_name, duration)

        print(f"--- [BAŞARILI] {len(data['stations'])} durak ve bağlantıları sisteme yüklendi! ---")
        return data # Koordinatlar (x_loc, y_loc) UI kısmında lazım olacak, saklayalım.

    except FileNotFoundError:
        print(f"!!! [HATA] {json_path} dosyası bulunamadı. Yolu kontrol et kanka! !!!")
    except Exception as e:
        print(f"!!! [HATA] Veri yüklenirken bir şeyler ters gitti: {e} !!!")
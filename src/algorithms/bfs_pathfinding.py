from collections import deque

#İki node arasındaki en kısa yolu bulan algoritmamız
#Kuyruk veri yapısıyla çalışıyoruz çünkü sıradaki duragı çıkarıyoruz. (en öndeki eleman). yeni eklediğimiz durakları sona atıyoruz
def find_path_bfs(graph, start_node, end_node):
    #Başlangıç ve bitiş aynı node ise hemen döndür
    if start_node == end_node:
        return [start_node]
    
    #Kuyrugu oluşturup içine bir tuple olarak başlangıç durağı ve o ana kadarki izlenen yolu atıyoruz
    #Tuple kullanma nedenimiz hedef duraga vardıgımız da aynı zamanda izlenen yolu da elde etmek
    queue = deque([(start_node, [start_node])])

    #Ziyaret edilenleri not etmek için bir küme oluşturduk.
    #Set veri yapısı kullandık ki O(1) hızında ziyaret edildi mi edilmedi mi bilebilelim Arka planda HashTable veri yapısı kullanır 
    visited = {start_node}

    #kuyruk dolu oldugu surece calıs
    while queue:
        #Tuple veri yapısıyla verileri tutan kuyruktan sıranın en basındaki node ve mevcut yolu tutan listeyi çekiyoruz
        current_node, path = queue.popleft()

        #Hedefe vardıysak döngü bitti , yolu döndürdük
        if current_node == end_node:
            return path
        
        #graph yapısında komşu ve süreyi bir tuple olarak kullanıyorduk. burada komşuları çekince sürede geliyor ama ona ihtiyacımız olmadıgı için _ kullandık
        for neighbor, _ in graph.get_neighbors(current_node):
            #Eger sıradaki durak daha önce ziyaret edilmediyse visited listesine ekliyoruz
            if neighbor not in visited:
                visited.add(neighbor)
                #kuyruga yeni komşuları ekledik , yolu da güncelledik
                queue.append((neighbor, path + [neighbor]))

    return None


"""

2. KUYRUK (QUEUE) TRAFİĞİ:
[ A ]           <-- A siraya girdi.
[ B, C ]        <-- A çikti; komşuları B ve C arkaya girdi.
[ C, D ]        <-- B çikti; komşusu D, C'nin arkasına girdi.
[ D ]           <-- C çikti; (C'nin altı yok).
[ ]             <-- D çikti; HEDEF BULUNDU!


"""


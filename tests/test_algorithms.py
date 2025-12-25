import pytest
import sys
import os

# Testlerin 'src' klasöründeki kodları görebilmesi için yolu ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.algorithms.bfs_pathfinding import find_path_bfs
from src.algorithms.pathfinding_dijkstra import PathFinder
from src.data_structures.trie import Trie

# --- TEST EDİLECEK SINIF VE FONKSİYONLARIN BURADA OLDUĞUNU VARSAYIYORUZ ---
# (Gerçek projende bunları: from main import find_path_bfs, PathFinder, Trie şeklinde import etmelisin)

# Testler için yardımcı bir Graph sınıfı (Senin kodundaki get_neighbors yapısına uygun)
class MockGraph:
    def __init__(self, adj_list):
        self.adj_list = adj_list
    def get_neighbors(self, node):
        return self.adj_list.get(node, [])

# 1. BFS TESTLERİ (Kısa Yol - Ağırlıksız)
def test_bfs_shortest_path():
    adj = {
        'A': [('B', 1), ('C', 1)],
        'B': [('D', 1)],
        'C': [('D', 1)],
        'D': []
    }
    graph = MockGraph(adj)
    # A -> D için en kısa yolu bulmalı
    assert find_path_bfs(graph, 'A', 'D') == ['A', 'B', 'D'] or ['A', 'C', 'D']

def test_bfs_same_start_end():
    graph = MockGraph({'A': []})
    assert find_path_bfs(graph, 'A', 'A') == ['A']

def test_bfs_no_path():
    graph = MockGraph({'A': [], 'B': []})
    assert find_path_bfs(graph, 'A', 'B') is None

# 2. DIJKSTRA TESTLERİ (En Ucuz Yol - Ağırlıklı)
def test_dijkstra_weighted_path():
    adj = {
        'A': [('B', 10), ('C', 1)],
        'C': [('B', 1)], # A-C-B yolu (2 birim) A-B yolundan (10 birim) daha kısa/ucuzdur
        'B': []
    }
    graph = MockGraph(adj)
    finder = PathFinder()
    path, distance = finder.dijkstra(graph, 'A', 'B')
    assert path == ['A', 'C', 'B']
    assert distance == 2

def test_dijkstra_unreachable():
    graph = MockGraph({'A': [], 'B': []})
    finder = PathFinder()
    path, distance = finder.dijkstra(graph, 'A', 'B')
    assert distance == float('inf')

# 3. TRIE TESTLERİ (Kelime ve Öneri Arama)
def test_trie_insert_and_search():
    trie = Trie()
    trie.insert("kadıköy")
    assert trie.search("kadıköy") is True
    assert trie.search("kadı") is False # Tam kelime değilse False dönmeli

def test_trie_starts_with():
    trie = Trie()
    trie.insert("beşiktaş")
    assert trie.starts_with("beşi") is True
    assert trie.starts_with("fener") is False

def test_trie_suggestions():
    trie = Trie()
    trie.insert("ankara")
    trie.insert("antaly")
    trie.insert("artvin")
    
    suggestions = trie.get_suggestions("an")
    assert "ankara" in suggestions
    assert "antaly" in suggestions
    assert "artvin" not in suggestions
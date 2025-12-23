class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    
    def insert(self,word):
        current = self.root

        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()

            current = current.children[char]    

        current.is_end_of_word = True


    def search(self, word):
        current = self.root
        
        for char in word:
  
            if char not in current.children:
                return False
            
            current = current.children[char]
            
        return current.is_end_of_word
    

    def starts_with(self, prefix):

        current = self.root
    
        for char in prefix:
        
            if char not in current.children:

                return False

            current = current.children[char]
        
        return True
    

    def get_suggestions(self, prefix):
        current = self.root
        
        for char in prefix:
            if char not in current.children:
                return [] 
            current = current.children[char]
            
        results = []
        self._dfs(current, prefix, results)
        return results
    
    def _dfs(self, node, path, results):
        if node.is_end_of_word:
            results.append(path) #path = tüm harfler yani kelimeler
            
        for char in sorted(node.children.keys()): # A,K,Ü,M hepsini ayır ve hepsi için ayrı ayrı çalıştır aşağıdaki kodu

            self._dfs(node.children[char], path + char, results)
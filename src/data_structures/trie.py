class TrieNode:
    def __init__(self):
        self.children = {} # Durak ismini (key) verip komşularını (value) jet hızıyla almak için dict kullandık.
        self.is_end_of_word = False #kelimenin sonuna geldiysek kelime oldugunu ayırt etmemiz için.  ->((CAT)EGORIZE)

class Trie:
    def __init__(self):
        self.root = TrieNode()

    
    def insert(self,word):
        current = self.root

        for char in word:
            #cat için düşünürsek
            if char not in current.children: #c-a-t
                current.children[char] = TrieNode() #root-c-a-t

            current = current.children[char]    #current = c-a-t

        current.is_end_of_word = True  #cat = kelime oldu


    def search(self, word):
        current = self.root
        
        for char in word:
  
            if char not in current.children:
                return False
            
            current = current.children[char]
            
        return current.is_end_of_word
    

    def starts_with(self, prefix): # Uskudarın USK unu girdiysek eğer

        current = self.root
    
        for char in prefix:
        
            if char not in current.children:

                return False

            current = current.children[char]
        
        return True
    

    #Girilen prefixe kadar gelir ve dfs'i çağırır
    def get_suggestions(self, prefix):
        current = self.root
        
        for char in prefix:
            if char not in current.children:
                return [] 
            current = current.children[char]
            
        results = []
        self._dfs(current, prefix, results)
        return results
    
    # en derine kadar iner ve kelimeleri toplar
    def _dfs(self, node, path, results): #node şuanki harfi , path - buraya gelen kadarki harfler , resultsta kelimeleri tutar
        if node.is_end_of_word:
            results.append(path) #path = tüm harfler yani kelime
            
        for char in sorted(node.children.keys()): # KAD+ -(I VEYA E) önerilerin kullanıcıya alfabetik sırayla (A'dan Z'ye) gelmesini sağlamak için dalları alfabetik sırayla gezdim.

            self._dfs(node.children[char], path + char, results) # REKÜRSİF KENDİNİ ÇAĞIR (KADI VE KADE İÇİN)
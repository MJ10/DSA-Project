class HashTable:
    def __init__(self, size=1007):
        self.MAX = size
        self.table = [None for _ in range(size)]

    def insert(self, key, value):
        entry = (key, value)
        index = self.hash(key)
        self.table[index].insertAtIndex(entry, 0)

    def search(self, key):
        hash_index = self.hash(key)
        if self.table[hash_index].isEmpty():
            return None
        l = self.table[hash_index].search(key)
        return l

    def hash(self, key):
        hash_code = 0
        for i in range(len(key)):
            hash_code += ord(key[i])
            hash_code += (hash_code << 10)
            hash_code ^= (hash_code >> 6)
        hash_code += (hash_code << 3)
        hash_code ^= (hash_code >> 11)
        hash_code += (hash_code << 15)
        return hash_code % 1007

    def keys(self):
        keys = []
        for row in self.table:
            if not row.isEmpty():
                l = row.print()
                for val in l:
                    keys.append(val[0])
        return keys
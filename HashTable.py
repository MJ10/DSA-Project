class HashNode:
    def __init__(self):
        self.entry = None


class HashTable:
    def __init__(self, size=1007):
        self.MAX = size
        self.table = [HashNode() for _ in range(size)]

    def insert(self, obj):
        index = self.hash(obj.key)
        obj.hash_reference = self.table[index]
        self.table[index].entry = obj

    def search(self, key):
        hash_index = self.hash(key)
        if self.table[hash_index].entry:
            return self.table[hash_index].entry
        return None

    def remove(self, obj):
        obj.hash_reference.entry = None

    def hash(self, key):
        hash_code = 0
        for i in range(len(key)):
            hash_code += ord(key[i])
            hash_code += (hash_code << 10)
            hash_code ^= (hash_code >> 6)
        hash_code += (hash_code << 3)
        hash_code ^= (hash_code >> 11)
        hash_code += (hash_code << 15)
        return hash_code % self.MAX

    def keys(self):
        keys = []
        for entry in self.table:
            if entry:
                keys.append(entry.key)
        return keys

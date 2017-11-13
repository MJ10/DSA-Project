class HashNode:
    """
    Node in the hash table, keeps a track of the cache object at that location.
    """
    def __init__(self):
        self.entry = None


class HashTable:
    """
    A hash table for accessing the cache contents
    Assumed 'collision-free'
    """
    def __init__(self, size=1009):
        """
        Returns a new hash table of size 'size'
        :param size: size of the hash table
        """
        self.MAX = size
        self.size = 0
        self.table = [HashNode() for _ in range(size)]

    def insert(self, obj):
        """
        Insert object obj to the table
        :param obj: Cache object to be inserted
        :return: None
        """
        index = self.hash(obj.key)
        obj.hash_reference = self.table[index]
        self.table[index].entry = obj
        self.size += 1

    def search(self, key):
        """
        Access the object with given key
        :param key: Key of object to be accessed
        :return: Cache object
        """
        hash_index = self.hash(key)
        if self.table[hash_index].entry:
            return self.table[hash_index].entry
        return None

    def remove(self, obj):
        """
        Remove object from hash table
        :param obj: Cache object to be deleted
        :return: None
        """
        self.size -= 1
        obj.hash_reference.entry = None

    def hash(self, key):
        """
        Calculates index for key using jenkin's hash function
        :param key: key to be hashed
        :return: hashed key index
        """
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
        """
        Returns a list of keys present in the hash table
        :return: List of keys present in the hash table
        """
        keys = []
        for entry in self.table:
            if entry.entry:
                keys.append(entry.entry.key)
        return keys

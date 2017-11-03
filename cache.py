from HashTable import HashTable
from LinkedList import FrequencyList


class CacheObject:
    """
    Object to be stored in the cache
    """
    def __init__(self, key, data):
        self.data = data
        self.key = key
        self.parent = None
        self.hash_reference = None


class LFUCache:
    """
    Implementation of the proposed LFU cache data structure
    """
    def __init__(self):
        """
        Initializes an object
        """
        self.table = HashTable()
        self.list = FrequencyList()

    def add(self, key, data):
        """
        Add the data with key to cache.
        :param key: Key of data to be inserted
        :param data: Data to be cached
        :return: None
        """
        cache_object = CacheObject(key, data)
        self.list.insert_new(cache_object)
        self.table.insert(cache_object)

    def evict(self):
        """
        Evict least frequently used cache item
        :return: None
        """
        cache_obj = self.list.delete_keys()
        if cache_obj:
            self.table.remove(cache_obj)
            return self.table.hash(cache_obj.key)

    def retrieve(self, key):
        """
        Retrieve cache object with key 'key'
        :param key:
        :return:
        """
        cache_obj = self.table.search(key)
        if cache_obj:
            self.list.lookup(cache_obj)
            return cache_obj.data
        return None


if __name__ == '__main__':
    cache = LFUCache()
    cache.add("This is a test", {"sone": 24, 132: "sdsds"})
    cache.add("This is a tesafhkt", {"sone": 24, 132: "sdsds"})
    cache.add("This is asadas test", {"sone": 24, 132: "sdsds"})
    print(cache.retrieve("This is a test"))
    print(cache.retrieve("This is a tesafhkt"))
    x = cache.evict()
    print(cache.table.table[x].entry)

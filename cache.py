from HashTable import HashTable
from FrequencyList import FrequencyList


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
        if len(self.table.table) is self.table.MAX:
            self.evict()
        obj_data = self.retrieve(key)
        if obj_data:
            obj_data.data += data
        else:
            cache_object = CacheObject(key, data)
            self.list.insert_new(cache_object)
            self.table.insert(cache_object)

    def evict(self):
        """
        Evict least frequently used cache item
        :return: None
        """
        cache_obj = self.list.delete_obj()
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
            return cache_obj
        return None

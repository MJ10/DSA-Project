class FrequencyNode:
    """
    New frequency node which contains all nodes having similar access frequency
    """

    def __init__(self):
        """
        Initializes Frequency Node object
        """
        self.value = 0
        self.next = None
        self.prev = None
        self.children = ListNode()
        

class ListNode:
    """
    New List Node Object 
    """
    def __init__(self):
        """
        Initializes a List Node object
        """
        self.next = None
        self.prev = None
        self.parent_node = None
        self.data = None


class FrequencyList:
    """
    Linked List containing frequency nodes of different frequencies
    """

    def __init__(self):
        """
        Initializes Frequency List object
        """
        self.head = FrequencyNode()

    def insert_new(self, key):
        """
        Insert new element into the linked list with it's access frequency = 1
        :param key: The object key that is to be inserted into the Frequency List
        :return: None
        """
        temp = self.head
        key_node = ListNode()
        key_node.data = key
        key.parent = key_node
        if temp.next is None:
            node = FrequencyNode()
            node.value = 1
            temp.next = node
            node.prev = temp
            key_node.parent_node = node
            node.children.next = key_node
            key_node.prev = node.children
            
        else:
            key_node.parent_node = temp.next
            self.insert_node(key_node, temp.next)

    def new_frequency_node(self, node):
        """
        Creates a new frequency node and inserts it into the Frequency List
        :param: node: Denotes the frequency node after which the created node is inserted
        :return: FrequencyNode object
        """
        temp = FrequencyNode()
        temp.value = node.value + 1
        temp.prev = node
        temp.next = node.next
        node.next = temp
        temp.next.prev = temp
        return temp
  
    def insert_node(self, list_node, frequency_node):
        """
        Inserts ListNode into the given freqency node in the first position
        :param : list_node : Denotes the  ListNode object that is to be inserted
        :param : frequency_node : Denotes the FrequencyNode object to which the given node is added to
        :return: None
        """
        if frequency_node.children.next is None:
            frequency_node.children.next = list_node
            list_node.prev = frequency_node.children
        else:
            list_node.next = frequency_node.children.next
            list_node.prev = frequency_node.children
            frequency_node.children.next = list_node
            if list_node.next:
                list_node.next.prev = list_node

    def lookup(self, key):
        """
        Frequency of the element searched for is updated and element is inserted accordingly into it's new position
        param: key : Denotes the object that is  being searched for and inserted 
        return:None
        """
        temp = key.parent
        temp1 = temp.parent_node
        if temp1.next:
            if temp1.value == temp1.next.value - 1:
                self.delete_node(temp)
                temp.parent_node = temp1.next
                self.insert_node(temp, temp1.next)
            else:
                temp2 = self.new_frequency_node(temp1)
                self.delete_node(temp)
                temp.parent_node = temp2
                self.insert_node(temp, temp2)
        else:
            temp2 = FrequencyNode()
            temp2.prev = temp1
            temp1.next = temp2
            temp2.value = temp1.value+1
            self.delete_node(temp)
            temp.parent_node = temp2
            self.insert_node(temp, temp2)

        if not temp1.children.next:
            temp1.prev.next = temp1.next
            temp1.next.prev = temp1.prev

    def delete_node(self, temp):
        """
        Deletes a node from the linked list of similar access frequencies
        param: temp: The pointer to the node that is being deleted
        return : None
        """
        temp.prev.next = temp.next
        if temp.next:
            temp.next.prev = temp.prev

    def delete_keys(self):
        """
        Deletes the first element of the least frequently used node in the frequency List
        return : None
        """
        if self.head.next:
            temp = self.head.next
            child = temp.children.next
            if child:
                child.prev.next = child.next
                if child.next:
                    child.next.prev = child.prev
            if not self.head.next.children.next:
                self.head.next.next.prev = self.head
                self.head.next = self.head.next.next
            return child.data
        return None

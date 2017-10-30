class Item:
    """
    Node of FP-tree
    """
    def __init__(self,id):
        self.id = id
        self.count = 1
        self.children = []
        self.father = None

    def get_id(self):
        return self.id

    def get_count(self):
        return self.count

    def get_children(self):
        return self.children

    def get_father(self):
        return self.father

    def contain_child(self,item_id):
        for child in self.children:
            if child.id == item_id:
                return True
        return False

    def get_child(self,item_id):
        for child in self.children:
            if child.id == item_id:
                return child
        return None

    def add_node(self,item_id):
        child = Item(item_id)
        child.father = self
        self.children.append(child)

    def __str__(self):
        return ("id: "+ self.id +
                "\ncount: " + str(self.count))

class ItemTree(Item):
    """
    Root of FP-tree
    """
    def __init__(self):
        self.id = 'root'
        self.count = 0
        self.children = []
        self.father = None
        self.item_trace = {}

    def add_path(self,path):
        """ Add a pattern to fp_tree

        :param path: A list, list[0] is the repeat time of this pattern
        :return: None
        """
        current_node = self
        for item_index in range(1,len(path)):
        #for item_id in path:
            if current_node.contain_child(path[item_index]):
                current_node = current_node.get_child(path[item_index])
                current_node.count += path[0]
            else:
                current_node.add_node(path[item_index])
                current_node = current_node.get_child(path[item_index])
                current_node.count = path[0]
                if not current_node.id in self.item_trace:      #creat the trace list of each item
                    self.item_trace[current_node.id] = []
                    self.item_trace[current_node.id].append(current_node)
                else:
                    self.item_trace[current_node.id].append(current_node)

    def has_no_branch(self):
        cur_node = self
        while cur_node.children:
            if len(cur_node.children)>1:
                return False
            cur_node = cur_node.children[0]
        return True

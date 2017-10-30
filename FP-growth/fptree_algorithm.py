from itertools import combinations, chain
from init_read import*
from fptree_structure import*

def frequent_1_itemsets(transaction_list, absolute_min_support):
    """Generate frequent 1 itemsets

    :param transaction_list: A list of sets represents the transactions   transaction_list[0] is the length of pattern
    :param absolute_min_support: An integer represents the absolute minimum support
    :return: A list of integer represents the frequent items
    """
    if not transaction_list:
        return []

    item_dic = {}
    frequent_itemsets = []
    for transaction in transaction_list:
        for item_index in range(1,len(transaction)):
        #for item in transaction:
            e = transaction[item_index]
            if not e in item_dic:
                item_dic[e] = transaction[0]
            else:
                item_dic[e] += transaction[0]
    for (item, count) in item_dic.items():
        if count>= absolute_min_support:
            frequent_itemsets.append(item)
    frequent_itemsets.sort(key = lambda x:item_dic[x], reverse=True)

    return frequent_itemsets


def build_fp_tree(transaction_list, header_table):
    """Build fp-tree

    :param transaction_list: (pattern list)
    :param header_table: frequent_1_item list
    :return: fp-tree
    """
    fp_tree = ItemTree()

    if not transaction_list:
        return fp_tree
    #first scanning, remove the none-frequent items
    for transaction in transaction_list:
        transaction_copy = transaction[:]
        for item_index in range(1,len(transaction_copy)):
        #for item in transaction_copy:0.
            element = transaction_copy[item_index]
            if not element in header_table:
                transaction.pop(transaction.index(element,1))
        length = transaction.pop(0)
        transaction.sort(key = lambda x: header_table.index(x))
        transaction.insert(0,length)

    transaction_list = list(filter(lambda x:len(x)!=1, transaction_list))

    #second scanning, building fp-tree
    for transaction in transaction_list:
        fp_tree.add_path(transaction)

    return fp_tree

def get_cond_pattern_base(fp_tree,item_id):
    """

    :param fp_tree: FP-tree of a pattern list
    :param item_id: the condition item id
    :return: a list of the condition pattern
    """
    cond_pattern_base = []
    for item_node in fp_tree.item_trace[item_id]:
        pattern = []
        cur_node = item_node.father
        if cur_node.id == 'root':
            continue
        pattern.append(item_node.count)
        while cur_node.id != 'root':
            pattern.append(cur_node.id)
            cur_node = cur_node.father
        cond_pattern_base.append(pattern)

    return cond_pattern_base

def powerset(set):
    """

    :param set: a list represents the set. such as [1,2,3]
    :return: powerset of this set except empty set
    """
    return list(chain.from_iterable([[list(e) for e in combinations(set,r)] for r in range(1,len(set)+1)]))


def get_frequent_itemset(transaction_list,min_surport):
    """ Generate the frequent itemset using recursive method

    :param transaction_list: (pattern list)
    :param min_surport: minimum support
    :return: frequent list
    """
    frequent_itemset = []
    head_list = frequent_1_itemsets(transaction_list, min_surport)
    fp_tree = build_fp_tree(transaction_list,head_list)


    if not fp_tree.children:
        frequent_itemset = []
        return frequent_itemset
    if fp_tree.has_no_branch():
        branch_list = []
        cur = fp_tree
        while cur.children:
            branch_list.append(cur.children[0].id)
            cur = cur.children[0]
        frequent_itemset = powerset(branch_list)
        return  frequent_itemset

    for item in head_list:
        cond_pattern_base = get_cond_pattern_base(fp_tree, item)
        sub_set = get_frequent_itemset(cond_pattern_base, min_surport)
        for e in sub_set:
            e.append(item)
        frequent_itemset += sub_set
    for e in head_list:
        frequent_itemset += [[e]]
    return frequent_itemset

if __name__=='__main__':
    transaction_list = read_data()
    transaction_num = len(transaction_list)
    min_surport = float(input("Input relate mininum support: "))
    absolute_min_surport = int(transaction_num*min_surport)

    frequent_itemsets = get_frequent_itemset(transaction_list, absolute_min_surport)
    for e in frequent_itemsets:
        e.sort()
    frequent_itemsets.sort(key = lambda x:(len(x),x))
    print("transaction num: %d"%transaction_num)
    print("support_num: %d"%absolute_min_surport)

    for e in frequent_itemsets:
        print("items ",end = '')
        print(e)

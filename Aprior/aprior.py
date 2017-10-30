import time
def get_transactions(filename):
    with open(filename) as f:
        transaction_list = f.read().splitlines()
        transactions = []
        for transaction in transaction_list:
            transactions.append(set(list(map(int, transaction.split()))))
        return transactions


def get_L1(transactions: object, abs_min_support: object) -> object:
    id_cont_dir = {}
    for transaction in transactions:
        for item_id in transaction:
            if item_id in id_cont_dir:
                id_cont_dir[item_id] += 1
            else: id_cont_dir[item_id] = 1

    L1_dir = {}
    for id in id_cont_dir.keys():
        if id_cont_dir[id] >= abs_min_support:
            L1_dir[(id,)] = id_cont_dir[id]

    return L1_dir


def aprior(transactions, L1_dir, min_sup):
    itemset_cont_dir = L1_dir.copy()
    L = [[]]
    L1 = list(L1_dir.keys())
    L1.sort()
    L.append(L1)
    k = 1
    while L[k]!=[]:
        L.append([])
        for i in range(len(L[k])):
            for j in range(i+1,len(L[k])):
                if L[k][i][:-1] == L[k][j][:-1]:
                    copy = list(L[k][i][:])      #L[k] is length-k frequent itemsets. form: list of set such as [(1,2),(3,5)]
                    copy.append(L[k][j][-1])
                    copy.sort()
                    if not tuple(copy) in L[k+1]:
                        L[k+1].append(tuple(copy))

        if k>1:
            l_copy = L[k+1][:]
            for itemset in l_copy:
                for i in range(k+1):
                    subset_list = list(itemset[:])
                    subset_list.pop(i)
                    subset_tuple = tuple(subset_list)
                    if not subset_tuple in L[k]:
                        if itemset in L[k+1]:
                            L[k+1].remove(itemset)
                        continue

        for itemset in L[k+1]:
            itemset_cont_dir[itemset] = 0;
        for transaction in transactions:
            for itemset in L[k+1]:
                i_set = set(itemset)
                if i_set <= transaction:
                    itemset_cont_dir[itemset] += 1


        l_copy = L[k+1][:]
        for itemset in l_copy:
            if itemset_cont_dir[itemset] < min_sup:
                L[k+1].remove(itemset)
                itemset_cont_dir.pop(itemset)

        k += 1

    return itemset_cont_dir


def print_fre_itemsets(itemset_cont_dir):
    key_list = list(itemset_cont_dir.keys())
    for key in sorted(key_list,key = lambda x:(len(x),x) ):
        print("items ",end='')
        print(key,end='')
        print(" :",end='')
        print(itemset_cont_dir[key],end='')
        print()

def get_min_sup():
    ans = float(input("Input related minimum support: "))
    return ans
if __name__ == '__main__':
    start = time.clock()

    relate_min_sup = get_min_sup()
    filename = "retail.dat"
    transactions = get_transactions(filename)
    absolut_min_sup = int(len(transactions)*relate_min_sup)
    L1_dir = get_L1(transactions,absolut_min_sup)
    itemset_cont_dir = aprior(transactions, L1_dir, absolut_min_sup)
    print_fre_itemsets(itemset_cont_dir)

    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
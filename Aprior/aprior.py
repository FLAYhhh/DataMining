support_rate = float(input('Input support rate : '))
transaction_num = 0
transactions = []
item_dict = {} #key:item_tuple , value:count
# compute the num of items
with open('retail.dat') as f:
    s = f.read().split()
    l = list(map(int, s))
    max = max(l)

items_list = [0] * (max + 1)

#creat a list of set: transactions (each set is a transaction)
with open('retail.dat') as f:
    line_list = f.read().splitlines()
    for line in line_list:
        transaction_num += 1
        transactions.append( set(list((map(int,line.split())))) )


print("transaction num: %d"%transaction_num)
support_num = int(transaction_num*support_rate); print("support_num:%d" %(support_num))

#compute the support num of each item
for transac in transactions:
    for item in transac:
        items_list[item] += 1

L = [[],[]]
L_set = [[],[]]
# compute L1
for index in range(len(items_list)):
    if items_list[index]>=support_num:
        L[1].append([index])

#L_set.append(set(L[1]))

for e in L[1]:
    #print("item %d : %d" % (e[0] , items_list[e[0]]))
    key = tuple(e)
    item_dict[key] = items_list[e[0]]

#print(L[1])
#print(items_list)
k = 1
while L[k]!=[]:
    L.append([])
    for i in range(len(L[k])):
        for j in range(i+1,len(L[k])):
            if L[k][i][:-1] == L[k][j][:-1]:
                copy = list(L[k][i][:])
                copy.append(L[k][j][-1])
                copy.sort()
                L[k+1].append( tuple(copy) )
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

    #generate frequent item set
    # t_list=[]
    # for itemset in L[k+1]:
    #     t_list.append(tuple(itemset))


    for items in L[k+1]:
        item_dict[items] = 0

    for transac in transactions:
        for items in L[k+1]:
            itemset = set(items)
            if itemset <= transac:
                item_dict[items] += 1

    l_copy = L[k+1][:] # in this for loop , t_list is changed , so it needs  a copy
    for items in l_copy:
        if item_dict[items] < support_num:
            L[k+1].remove(items)
            item_dict.pop(items)
    k+=1

key_list = list(item_dict.keys())
for key in sorted(key_list,key = lambda x:(len(x),x) ):
    print("items ",end='')
    print(key,end='')
    print(" :",end='')
    print(item_dict[key],end='')
    print()
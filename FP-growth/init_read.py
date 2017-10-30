def read_data():
    """ Read data from a text file

    :return: A list of itemlist represents transactions
    """
    transaction_list = []
    with open("retail.dat","r") as f:
        file_str = f.read()

        # #find the max id (one of the return val)
        # item_list = map(int,file_str.split())
        # max_id = max(item_list)

        transaction_lines = file_str.splitlines()
        for transaction in transaction_lines:
            l = list(map(int, transaction.split()))
            l.insert(0,1)
            transaction_list.append(l)

        return transaction_list

if __name__=='__main__':
    print(read_data())

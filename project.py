import time
import init
import collections


# Function to load file and return lists of Transactions
def Load_data(filename, window, cogList, query):
    return init.main(filename, window, cogList, query)


# To convert initial transaction into frozenset
def create_initialset(dataset):
    retDict = collections.Counter()
    for trans in dataset:
        retDict[frozenset(trans)] += 1
    return retDict


# c lass of FP TREE node
class TreeNode:
    def __init__(self, Node_name, counter, parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def increment_counter(self, counter):
        self.count += counter


# To create Headertable and ordered itemsets for FP Tree
def create_FPTree(dataset, minSupport):
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item, 0) + dataset[transaction]
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del (HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]

    retTree = TreeNode('Null Set', 1, None)
    for itemset, count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        if len(frequent_transaction) > 0:
            # to get ordered itemsets form transactions
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
            # to update the FPTree
            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable


# To create the FP Tree using ordered item sets
def updateTree(itemset, FPTree, HeaderTable, count):
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].increment_counter(count)
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)


# To update the link of node in FP Tree
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node


# To transverse FPTree in upward direction
def FPTree_uptransveral(leaf_Node, prefixPath):
    if leaf_Node.parent != None:
        prefixPath.append(leaf_Node.name)
        FPTree_uptransveral(leaf_Node.parent, prefixPath)


# To find conditional Pattern Bases
def find_prefix_path(TreeNode):
    Conditional_patterns_base = {}

    while TreeNode != None:
        prefixPath = []
        FPTree_uptransveral(TreeNode, prefixPath)
        if len(prefixPath) > 1:
            Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
        TreeNode = TreeNode.nodeLink

    return Conditional_patterns_base


# function to mine recursively conditional patterns base and conditional FP tree
def Mine_Tree(HeaderTable, minSupport, prefix, frequent_itemset,cogList):
    cogSet = prefix.copy()
    for cogItem in cogList:
        cogSet.add(int(cogItem))

    bigL = [v[0] for v in sorted(HeaderTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        # add frequent itemset to final list of frequent itemsets

        if cogSet.issubset(new_frequentset):
            frequent_itemset.append(new_frequentset)

        # get all conditional pattern bases for item or itemsets

        Conditional_pattern_bases = find_prefix_path(HeaderTable[basePat][1])

        # call FP Tree construction to make conditional FP Tree

        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases, minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_header, minSupport, new_frequentset, frequent_itemset,cogList)


def main():
    filename = input("Enter the filename:\n")

    min_Support = int(input("Enter the minimum support count:\n"))

    window = int(input("please enter window size:\n"))

    cogInput = input("please enter cog numbers separated by space\n")

    cogList = cogInput.split()

    query = int(input("please enter query size\n"))

    initSet = create_initialset(Load_data(filename, window, cogList, query))
    start = time.time()
    FPtree, HeaderTable = create_FPTree(initSet, min_Support)

    frequent_itemset = []
    # call function to mine all ferquent itemsets
    if HeaderTable is None:
        print("No match found")
        exit()
    Mine_Tree(HeaderTable, min_Support, set([]), frequent_itemset,cogList)
    end = time.time()

    print("Time Taken is:")
    print(end - start)
    print("All frequent itemsets:")
    print(frequent_itemset)

    file = open("COG_INFO_TABLE.txt", "r")
    dataLines = file.readlines()

    answerItems = list()
    cogSet = []
    info_flag = False
    for cogItem in cogList:
        cogSet.append(int(cogItem))
    for i in frequent_itemset:
        for item in i:
            flagItem = 0
            strNew = "COG" + ('0' * (4 - len(str(item)))) + str(item)
            for k in range(len(answerItems)):
                if answerItems[k] == strNew:
                    flagItem = 1
            if flagItem == 0:
                answerItems.append(strNew)

                if (item not in cogSet) and item != 9999:
                    print(strNew)
                    info_flag = False
                    for line in dataLines:
                        if line[0:7] == strNew:
                            print(line)
                            info_flag = True
                    if (info_flag == False):
                        print("No information about this cog in :",file.name)


if __name__ == "__main__":
    main()


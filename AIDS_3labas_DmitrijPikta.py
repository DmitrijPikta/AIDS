class Node:
    def __init__(self, level=None, dad_index=None, key1=None, key2=None):
        #self.dad_index = dad_index
        #self.level = level
        self.key1 = key1
        self.key2 = key2
        self.key3 = None


# Tree elements: 0 - Node, 1 - first children, 2 - second children, 3 - therd children
TwoThreeTree = []


# Return list of two values. 0 - level, 1 - list of dad_indexes
def search(Tree: list, key: int, result: list = None) -> list:
    if result is None:
        result = [0, []]

    # If key is one of Node keys
    if Tree[0].key1 == key or Tree[0].key2 == key or Tree[0].key3 == key:
        return result
    
    # If Node alredy do not have children
    if len(Tree) == 1:
        return None
    
    # Increase level
    result[0] += 1

    # Entering to children Nodes
    if Tree[0].key1 > key:
        dad_index = 0
        result[1].append(dad_index)
        return search(Tree[dad_index + 1], key, result)
    elif Tree[0].key1 < key and (Tree[0].key2 == None or Tree[0].key2 > key) :
        dad_index = 1
        result[1].append(dad_index)
        return search(Tree[dad_index + 1], key, result)
    else:
        dad_index = 2
        result[1].append(dad_index)
        return search(Tree[dad_index + 1], key, result)


def balance(Tree: list, key: int) -> None:
    # get path to place where are 3 keys 
    result = search(Tree, key)

    # if key is at root
    if result[0] == 0:
        new_root = Node()
        #Tree = [new_root, Tree]
        old_root_as_subtree = Tree.copy()
        Tree.clear()
        Tree.extend([new_root, old_root_as_subtree])
        result[1].append(0)

    branch = Tree
    # make branch list of parent and children, where one of children have 3 keys
    for i in range(len(result[1]) - 1):
        branch = branch[result[1][i] + 1]


    moving_element_up = branch[result[1][-1] + 1][0].key2 
    moving_element_side = branch[result[1][-1] + 1][0].key3

    branch[result[1][-1] + 1][0].key2 = None
    branch[result[1][-1] + 1][0].key3 = None

    # making new Node for moving_element_side in right side of Node where were 3 keys
    branch.insert(result[1][-1] + 2, [Node(None, None, moving_element_side)])

    # if where are 4 children
    if len(branch[result[1][-1] + 1]) == 5:
        # children 3, 4 that we will move with moving_element_side
        moving_third_children_side = branch[result[1][-1] + 1][3]
        moving_fourth_children_side = branch[result[1][-1] + 1][4]

        # moving children 
        branch[result[1][-1] + 2].append(moving_third_children_side)
        branch[result[1][-1] + 2].append(moving_fourth_children_side)

        # deleting moved children 
        branch[result[1][-1] + 1].pop()
        branch[result[1][-1] + 1].pop()

    # moving moving_element_up to parent Node
    if branch[0].key1 == None:
        branch[0].key1 = moving_element_up
    elif branch[0].key2 == None:
        if branch[0].key1 < moving_element_up:
            branch[0].key2 = moving_element_up
        else:
            branch[0].key1, branch[0].key2 = moving_element_up, branch[0].key1
    else:
        if branch[0].key1 > moving_element_up:
            branch[0].key1, branch[0].key2, branch[0].key3 = moving_element_up, branch[0].key1, branch[0].key2
        elif branch[0].key1 < moving_element_up and branch[0].key2 > moving_element_up:
            branch[0].key2, branch[0].key3 = moving_element_up, branch[0].key2
        else:
            branch[0].key3 = moving_element_up

    if branch[0].key3 != None:
        balance(Tree, moving_element_up)  
    

def insert_tree(Tree: list, key: int) -> bool:
    # if Tree is emplty
    if len(Tree) == 0:
        Tree.append(Node(None, None, key))

    # If key is one of Node keys
    if Tree[0].key1 == key or Tree[0].key2 == key:
        return 
    
    # If Node alredy do not have children
    if len(Tree) == 1:
        if Tree[0].key2 == None:
            if Tree[0].key1 < key:
                Tree[0].key2 = key
            else:
                Tree[0].key1, Tree[0].key2 = key, Tree[0].key1
            return False
        else:
            if Tree[0].key2 < key:
                Tree[0].key3 = key
            elif Tree[0].key1 < key:
                Tree[0].key2, Tree[0].key3 = key, Tree[0].key2
            else:
                Tree[0].key1, Tree[0].key2, Tree[0].key3 = key, Tree[0].key1, Tree[0].key2
            return True
    
    # Entering to children Nodes
    if Tree[0].key1 > key:
        dad_index = 0
        return insert_tree(Tree[dad_index + 1], key)
    elif Tree[0].key1 < key and (Tree[0].key2 == None or Tree[0].key2 > key) :
        dad_index = 1
        return insert_tree(Tree[dad_index + 1], key)
    else:
        dad_index = 2
        return insert_tree(Tree[dad_index + 1], key)


def insert_with_balancing(Tree: list, key: int) -> None:
    if insert_tree(Tree, key):
        balance(Tree, key)


def print_tree(Tree: list, indent: int = -4) -> None:
    if Tree[0].key2 is None:
        print(f"[{Tree[0].key1}]")
    else:
        print(f"[{Tree[0].key1}, {Tree[0].key2}]")
    
    # If Node do not have children
    if len(Tree) == 1:
        return

    indent += 4
    for i in range(len(Tree) - 1):
        print(f"{indent * ' '}|---", end="")
        print_tree(Tree[i + 1], indent)


def delete(Tree: list, key: int, result: list = None) -> None:
    # find path to key
    if result is None:
        result = search(Tree, key, result)
    
    if result is None:
        return
    
    branch = Tree
    # make branch list of parent and children, where one of children is key for deletion
    for i in range(len(result[1]) - 1):
        branch = branch[result[1][i] + 1]
    
    # if key is in a leaf Node
    if len(branch[result[1][-1] + 1]) == 1:
        # if Node has 2 keys
        if branch[result[1][-1] + 1][0].key2 is not None:
            # if key is first key in Node
            if branch[result[1][-1] + 1][0].key1 == key:
                branch[result[1][-1] + 1][0].key1 = branch[result[1][-1] + 1][0].key2
                branch[result[1][-1] + 1][0].key2 = None
            # if key is second key in Node
            elif branch[result[1][-1] + 1][0].key2 == key:
                branch[result[1][-1] + 1][0].key2 = None
            return
        # if Node has 1 key
        else:
            branch[result[1][-1] + 1][0].key1 = None
            fix_underfull(Tree, result)
            return
    # if key is in an internal Node
    else:
        # if Node where is key for deleting has one key
        if branch[result[1][-1] + 1][0].key1 == key:
            # swap key for deleting with min right child
            branch[result[1][-1] + 1][0].key1, branch[result[1][-1] + 1][2][0].key1 = branch[result[1][-1] + 1][2][0].key1, branch[result[1][-1] + 1][0].key1
            result[1].append(1)
        # if Node where is key for deleting has two keys
        else:
            # swap key for deleting with min right child
            branch[result[1][-1] + 1][0].key2, branch[result[1][-1] + 1][3][0].key1 = branch[result[1][-1] + 1][3][0].key1, branch[result[1][-1] + 1][0].key2
            result[1].append(2)
        delete(Tree, key, result)
        




def fix_underfull(Tree: list, path_to_underfull: list) -> None:
    # make branch list of parent and children, where one of children is key for deletion
    branch = Tree
    for i in range(len(path_to_underfull[1]) - 1):
        branch = branch[path_to_underfull[1][i] + 1]


    # check all children is they have 2 keys 
    indexes_of_children_with_2_keys = []
    for i in range(len(branch) - 1):
        if branch[i + 1][0].key2 is not None:
            indexes_of_children_with_2_keys.append(i)

    # if where are children with 2 keys
    if indexes_of_children_with_2_keys:
        # if where are 2 children with 2 keys
        if len(indexes_of_children_with_2_keys) == 2:
            if path_to_underfull[1][-1] == 0:
                # move key from children where were 2 keys to underfull children
                branch[1][0].key1, branch[2][0].key1 = branch[2][0].key1, branch[2][0].key2
                branch[2][0].key2 = None

                # swap moved key with parent key
                branch[1][0].key1, branch[0].key1 = branch[0].key1, branch[1][0].key1
            elif path_to_underfull[1][-1] == 1:
                # move key from children where were 2 keys to underfull children
                branch[2][0].key1 = branch[1][0].key2
                branch[1][0].key2 = None

                # swap moved key with parent key
                branch[2][0].key1, branch[0].key1 = branch[0].key1, branch[2][0].key1
            else:
                # move key from children where were 2 keys to underfull children
                branch[3][0].key1 = branch[2][0].key2
                branch[2][0].key2 = None

                # swap moved key with parent key
                if branch[0].key2 is not None:
                    branch[3][0].key1, branch[0].key2 = branch[0].key2, branch[3][0].key1
                else:
                    branch[3][0].key1, branch[0].key1 = branch[0].key1, branch[3][0].key1
        # if only first children have 2 keys
        elif  indexes_of_children_with_2_keys[0] == 0:
            if path_to_underfull[1][-1] == 1:
                # move key from children where were 2 keys to underfull children
                branch[2][0].key1 = branch[1][0].key2
                branch[1][0].key2 = None

                # swap moved key with parent key
                branch[2][0].key1, branch[0].key1 = branch[0].key1, branch[2][0].key1
            else:
                branch[3][0].key1 = branch[0].key2
                branch[0].key2 = branch[2][0].key1
                branch[2][0].key1 = branch[0].key1
                branch[0].key1 = branch[1][0].key2
                branch[1][0].key2 = None
        # if only second children have 2 keys
        elif indexes_of_children_with_2_keys[0] == 1:
            if path_to_underfull[1][-1] == 0:
                # move key from children where were 2 keys to underfull children
                branch[1][0].key1, branch[2][0].key1 = branch[2][0].key1, branch[2][0].key2
                branch[2][0].key2 = None

                # swap moved key with parent key
                branch[1][0].key1, branch[0].key1 = branch[0].key1, branch[1][0].key1
            else:
                # move key from children where were 2 keys to underfull children
                branch[3][0].key1 = branch[2][0].key2
                branch[2][0].key2 = None

                # swap moved key with parent key
                if branch[0].key2 is not None:
                    branch[3][0].key1, branch[0].key2 = branch[0].key2, branch[3][0].key1
                else:
                    branch[3][0].key1, branch[0].key1 = branch[0].key1, branch[3][0].key1
        # if only third children have 2 keys
        else:
            if path_to_underfull[1][-1] == 0:
                branch[1][0].key1 = branch[0].key1
                branch[0].key1 = branch[2][0].key1
                branch[2][0].key1 = branch[0].key2
                branch[0].key2 = branch[3][0].key1

                branch[3][0].key1, branch[3][0].key2 = branch[3][0].key2, None
            elif path_to_underfull[1][-1] == 1:
                branch[2][0].key1 = branch[0].key2
                branch[0].key2 = branch[3][0].key1

                branch[3][0].key1, branch[3][0].key2 = branch[3][0].key2, None
        return
    
    # if where are not children with 2 keys
    # if underfull is third children
    if path_to_underfull[1][-1] == 2:
        # delete underfull Node 
        branch.pop()
        # move kay from second parent to second children
        branch[2][0].key2, branch[0].key2 = branch[0].key2, None
        return
    else:
        # delete underfull Node 
        del branch[path_to_underfull[1][-1] + 1]
        # move key from first parent to children
        branch[1][0].key2 = branch[0].key1

        # if keys at first children now are not in order
        if branch[1][0].key1 > branch[1][0].key2:
            branch[1][0].key1, branch[1][0].key2 = branch[1][0].key2, branch[1][0].key1

        # if parent Node had two keys
        if branch[0].key2 is not None:
            branch[0].key1, branch[0].key2 = branch[0].key2, None
            return
        # if parent Node had one key
        else:
            # parent Node is empty now
            branch[0].key1 = None
            print("Parent Node is empty")
            # make path to child
            path_to_underfull[1].pop()
            #path_to_underfull[1].append(0)
            move_child_to_uncle(Tree, path_to_underfull)


def move_child_to_uncle(Tree: list, path_to_child: list) -> None:
    print(path_to_child)

    # make branch list of children, parents and grandparents
    branch = Tree
    if len(path_to_child[1]) > 2:
        for i in range(len(path_to_child[1]) - 2):
            branch = branch[path_to_child[1][i] + 1]
    
    # if moving child's parent is first
    if path_to_child[1][-1] == 0:
        # move child to uncle 
        branch[2].insert(1, branch[1][1])
        # delete parent
        del branch[1]
        # move key from grandparent if uncle have 1 key
        if branch[1][0].key2 is None:
            branch[1][0].key1, branch[1][0].key2 = branch[0].key1, branch[1][0].key1
            branch[0].key1 = branch[0].key2
            branch[0].key2 = None
            return
        # move key from grandparent if uncle have 2 key
        else:
            branch[1][0].key1, branch[1][0].key2, branch[1][0].key3 = branch[0].key1, branch[1][0].key1, branch[1][0].key2
            branch[0].key1 = branch[0].key2
            branch[0].key2 = None

            # now uncle have 3 keys, so call balance
            balance(Tree, branch[1][0].key2)

    # if moving child's parent is second
    elif path_to_child[1][-1] == 1:
        # move child to uncle 
        branch[1].append(branch[2][1])
        # delete parent
        del branch[2]
        # move key from grandparent if uncle have 1 key
        if branch[1][0].key2 is None:
            branch[1][0].key2 = branch[0].key1
            branch[0].key1 = branch[0].key2
            branch[0].key2 = None
            return
        # move key from grandparent if uncle have 2 key
        else:
            branch[1][0].key3 = branch[0].key1
            branch[0].key1 = branch[0].key2
            branch[0].key2 = None

            # now uncle have 3 keys, so call balance
            balance(Tree, branch[1][0].key2)

    # if moving child's parent is third
    else:
        # move child to uncle 
        branch[2].append(branch[3][1])
        # delete parent
        del branch[3]
        # move key from grandparent if uncle have 1 key
        if branch[2][0].key2 is None:
            branch[2][0].key2 = branch[0].key2
            branch[0].key2 = None
            return
        # move key from grandparent if uncle have 2 key
        else:
            branch[2][0].key3 = branch[0].key2
            branch[0].key2 = None
            print_tree(Tree)
            # now uncle have 3 keys, so call balance
            balance(Tree, branch[2][0].key2)
        





    
                
                



# Training 
TwoThreeTree = [Node(0, 0, 50, 90), [Node(1, 0, 20), [Node(2, 0, 10)], [Node(2, 1, 30, 40)]], [Node(1, 1, 70), [Node(2, 2, 60)], [Node(2, 3, 80)]], [Node(1, 2, 120, 150), [Node(2, 4, 100, 110)], [Node(2, 5, 130, 140)], [Node(2, 6, 160)]]]

# print(search(TwoThreeTree, 30))
insert_with_balancing(TwoThreeTree, 65)
insert_with_balancing(TwoThreeTree, 75)
insert_with_balancing(TwoThreeTree, 85)
insert_with_balancing(TwoThreeTree, 15)
insert_with_balancing(TwoThreeTree, 25)
# search(TwoThreeTree, 135)
#print(search(TwoThreeTree, 135))
#balance(TwoThreeTree, 135)
# print(TwoThreeTree[2][1][0].key1)
#print_tree(TwoThreeTree)

Tree1 = []
insert_with_balancing(Tree1, 10)
insert_with_balancing(Tree1, 15)
insert_with_balancing(Tree1, 20)
insert_with_balancing(Tree1, 5)
insert_with_balancing(Tree1, 1)
insert_with_balancing(Tree1, 100)
insert_with_balancing(Tree1, 7)
insert_with_balancing(Tree1, 106)

Tree1 = TwoThreeTree
print_tree(Tree1)
delete(Tree1, 110)
delete(Tree1, 140)
delete(Tree1, 130)
delete(Tree1, 120)
print_tree(Tree1)
delete(Tree1, 160)
#delete(Tree1, 40)
print_tree(Tree1)

#delete(Tree1, 60)
# delete(Tree1, 40)
# delete(Tree1, 30)
# print_tree(Tree1)


#print(search(TwoThreeTree, 5000))

#--------------------
tree = []
insert_tree(tree, 10)
#delete(tree, 10)

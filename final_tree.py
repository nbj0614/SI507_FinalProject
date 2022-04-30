#
# Tree functions for final project
#
def insertTree(tree, book):
    if (tree[0] == None and tree[1] == None and tree[2] == None):   #empty node
        return (book, None, None)
    else:   #internal node
        if (book.primary_isbn13 < tree[0].primary_isbn13):  #new ISBN < current ISBN
            if (tree[1] == None):   # add tp left child if vacant
                return (tree[0], (book, None, None), tree[2])
            else:  # go to left child if occupied
                return (tree[0], insertTree(tree[1], book), tree[2])
        elif (book.primary_isbn13 > tree[0].primary_isbn13): # new ISBN > current ISBN
            if (tree[2] == None):   # add to right child if vacant
                return (tree[0], tree[1], (book, None, None))
            else:   # go to right child if occupied
                return (tree[0], tree[1], insertTree(tree[2], book))
        else:   # do nothing if exists
            return tree


def traversalTree(tree, allList):
    if (tree[1] != None):
        traversalTree(tree[1], allList)
    allList.append(tree[0])
    if (tree[2] != None):
        traversalTree(tree[2], allList)


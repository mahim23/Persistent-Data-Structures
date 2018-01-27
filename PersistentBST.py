from os import unlink


class Node:
    def __init__(self, name=None, parent=[None, None][:], left=None, right=None):
        self.name = name
        self.left = left
        self.right = right
        self.parent = {parent[0]: parent[1]}

    def makeFile(self, data):
        file = open(str(hex(id(self)) + ".txt"), mode="w")
        file.write(data)
        file.close()

    def getData(self):
        file = open(str(hex(id(self)) + ".txt"), mode="r")
        lines = file.readlines()
        data = ""
        for line in lines:
            data += line
        file.close()
        return data

    def deleteFile(self):
        file = open(str(hex(id(self)) + ".txt"), mode="w")
        file.close()
        unlink(file.name)

    def isLeftChild(self, branch):
        if self.parent[branch] is None:
            return False
        if self.parent[branch].left is not None and self.parent[branch].left.name == self.name:
            return True
        return False

    def isRightChild(self, branch):
        if self.parent[branch] is None:
            return False
        if self.parent[branch].right is not None and self.parent[branch].right.name == self.name:
            return True
        return False

    def minimum(self):
        if self.left is None:
            return self
        return self.left.minimum()

    def maximum(self):
        if self.right is None:
            return self
        return self.right.maximum()

    def successor(self, branch):
        if self.right is not None:
            return self.right.minimum()
        if self.parent[branch] is None:
            return None
        x = self
        y = x.parent[branch]
        while y is not None and x != y.left:
            x = y
            y = y.parent[branch]
        return y

    def predecessor(self, branch):
        if self.left is not None:
            return self.left.maximum()
        if self.parent[branch] is None:
            return None
        x = self
        y = x.parent[branch]
        while y is not None and x != y.right:
            x = y
            y = y.parent[branch]
        return y

    def search(self, k):
        if self.name == k:
            return self
        elif self.name > k:
            if self.left is not None:
                return self.left.search(k)
            else:
                return None
        else:
            if self.right is not None:
                return self.right.search(k)
            else:
                return None

    def inFix(self):
        if self.left is not None:
            self.left.inFix()
        print(self.name)
        if self.right is not None:
            self.right.inFix()

    def split(self, branch):
        t = Node(self.name, [branch, self.parent[branch]], self.left, self.right)
        t.makeFile(self.getData())
        if self.left is not None:
            self.left.parent[branch] = t
        if self.right is not None:
            self.right.parent[branch] = t
        del self.parent[branch]
        if t.isLeftChild(branch):
            t.parent[branch].left = t
        elif t.isRightChild(branch):
            t.parent[branch].right = t
        return t

    def __del__(self):
        self.deleteFile()


class PBST:
    def __init__(self):
        self.branches = {"master": None}

    def insert(self, key, branch):
        root = self.branches[branch]
        if root is None:
            tmp = self.branches[branch] = Node(key, [branch, None])
            data = dataInput("Enter data: ")
            tmp.makeFile(data)
            return
        tmp = root
        l = []
        while True:
            if len(tmp.parent) > 1 and tmp.name != key:
                t = tmp.split(branch)
                l.append([t.parent[branch], tmp])
                tmp = t
            if tmp.name == key:
                print("File already exists!")
                while True:
                    try:
                        p, n = l.pop()
                        if n.name < p.name:
                            p.left.deleteFile(branch)
                            p.left = n
                        else:
                            p.right.deleteFile(branch)
                            p.right = n
                        n.parent[branch] = p
                        n.left.parent[branch] = n
                        n.right.parent[branch] = n
                    except IndexError:
                        break
                return
            elif tmp.name > key:
                if tmp.left is None:
                    tmp.left = Node(key, [branch, tmp])
                    data = dataInput("Enter data: ")
                    tmp.left.makeFile(data)
                    return
                else:
                    tmp = tmp.left
            else:
                if tmp.right is None:
                    tmp.right = Node(key, [branch, tmp])
                    data = dataInput("Enter data: ")
                    tmp.right.makeFile(data)
                    return
                else:
                    tmp = tmp.right

    def delete(self, key, branch):
        tmp = self.branches[branch]
        if tmp is None:
            print("File doesn't exist!")
            return
        l = []
        while True:
            if len(tmp.parent) > 1 and tmp.name != key:
                t = tmp.split(branch)
                l.append([t.parent[branch], tmp])
                tmp = t
            if tmp.name == key:
                if tmp.left is not None:
                    pred = tmp.left.maximum()
                    tmp.name = pred.name
                    tmp.makeFile(pred.getData())
                    tmp = tmp.left
                    key = pred.name
                elif tmp.right is not None:
                    suc = tmp.right.minimum()
                    tmp.name = suc.name
                    tmp.makeFile(suc.getData())
                    tmp = tmp.right
                    key = suc.name
                else:
                    tmp.deleteFile()
                    print("File deleted")
                    if tmp.isLeftChild(branch):
                        tmp.parent[branch].left = None
                    elif tmp.isRightChild(branch):
                        tmp.parent[branch].right = None
                    else:
                        self.branches[branch] = None
                    del tmp.parent[branch]
                    return
            elif tmp.name > key:
                if tmp.left is None:
                    print("File doesn't exist!")
                    while True:
                        try:
                            p, n = l.pop()
                            if n.name < p.name:
                                p.left.deleteFile(branch)
                                p.left = n
                            else:
                                p.right.deleteFile(branch)
                                p.right = n
                            n.parent[branch] = p
                            n.left.parent[branch] = n
                            n.right.parent[branch] = n
                        except IndexError:
                            break
                    return
                tmp = tmp.left
            else:
                if tmp.right is None:
                    print("File doesn't exist!")
                    while True:
                        try:
                            p, n = l.pop()
                            if n.name < p.name:
                                p.left.deleteFile(branch)
                                p.left = n
                            else:
                                p.right.deleteFile(branch)
                                p.right = n
                            n.parent[branch] = p
                            n.left.parent[branch] = n
                            n.right.parent[branch] = n
                        except IndexError:
                            break
                    return
                tmp = tmp.right

    def edit(self, k, branch):
        tmp = self.branches[branch]
        if tmp is None:
            print("File doesn't exist!")
            return
        l = []
        while True:
            if len(tmp.parent) > 1:
                t = tmp.split(branch)
                l.append([t.parent[branch], tmp])
                tmp = t
            if tmp.name == k:
                print("Data in file currently: ", tmp.getData())
                data = dataInput("Enter new data: ")
                tmp.makeFile(data)
                return
            elif tmp.name > k:
                if tmp.left is not None:
                    tmp = tmp.left
                else:
                    print("File doesn't exist!")
                    while True:
                        try:
                            p, n = l.pop()
                            if n.name < p.name:
                                p.left.deleteFile(branch)
                                p.left = n
                            else:
                                p.right.deleteFile(branch)
                                p.right = n
                            n.parent[branch] = p
                            n.left.parent[branch] = n
                            n.right.parent[branch] = n
                        except IndexError:
                            break
                    return
            else:
                if tmp.right is not None:
                    tmp = tmp.right
                else:
                    print("File doesn't exist!")
                    while True:
                        try:
                            p, n = l.pop()
                            if n.name < p.name:
                                p.left.deleteFile(branch)
                                p.left = n
                            else:
                                p.right.deleteFile(branch)
                                p.right = n
                            n.parent[branch] = p
                            n.left.parent[branch] = n
                            n.right.parent[branch] = n
                        except IndexError:
                            break
                    return

    def search(self, k, branch):
        node = self.branches[branch]
        if node is not None:
            return node.search(k)

    def inFix(self, branch):
        root = self.branches[branch]
        if root is not None:
            root.inFix()

    def newBranch(self, branch, prevBranch):
        tree1 = self.branches[prevBranch]
        tmp = self.branches[branch] = Node(tree1.name, [branch, None], tree1.left, tree1.right)
        if tree1.left is not None:
            tree1.left.parent[branch] = tmp
        if tree1.right is not None:
            tree1.right.parent[branch] = tmp
        tmp.makeFile(tree1.getData())


def dataInput(prompt):
    contents = ""
    print(prompt, end="")
    while True:
        line = ""
        try:
            line = input()
        except EOFError:
            break
        if line == "end":
            break
        contents += line + "\n"
    return contents

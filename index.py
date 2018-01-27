from PersistentBST import *

print("\n\tARCHEIO")

Tree = PBST()

currentBranch = "master"
prevBranch = None
branches = ["master"]


while True:
    print("\nCurrent Branch:", currentBranch)

    print("\n1. List Files\n2. View File\n3. New File\n4. Delete File\n5. Edit File\n6. List Branches\n7. New "
          "Branch\n8. Switch Branch\n9. Exit\n")

    choice = input("$ ")
    print()

    if choice == "1":
        print("Files: ")
        Tree.inFix(currentBranch)

    elif choice == "2":
        name = input("Enter name of file to be opened: ")
        file = Tree.search(name, currentBranch)
        if file is None:
            print("File does not exist!")
        else:
            print(file.getData())

    elif choice == "3":
        name = input("Enter name of new file: ")
        Tree.insert(name, currentBranch)

    elif choice == "4":
        name = input("Enter name of file to be deleted: ")
        Tree.delete(name, currentBranch)

    elif choice == "5":
        name = input("Enter name of file to be edited: ")
        Tree.edit(name, currentBranch)

    elif choice == "6":
        print("Branches:")
        for branch in branches:
            print(branch)

    elif choice == "7":
        branchName = input("Enter name of new branch: ")
        if branchName in branches:
            print("Branch already exists")
            continue
        branches.append(branchName)
        prevBranch, currentBranch = currentBranch, branchName
        Tree.newBranch(currentBranch, prevBranch)

    elif choice == "8":
        branchName = input("Enter name of branch to switch to: ")
        if branchName not in branches:
            print("Branch doesn't exist")
            continue
        prevBranch, currentBranch = currentBranch, branchName

    elif choice == "exit" or choice == "9":
        file = None
        Tree = None
        print("Exiting...")
        break

    elif choice == "debug":
        print()

    else:
        print("Invalid Input")

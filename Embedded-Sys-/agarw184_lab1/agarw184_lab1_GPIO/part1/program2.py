
#Essential list
initiallist = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

#Asks for number
num = int(input("Enter number:"))

#Using List comprehension conditions
finallist = [i for i in initiallist if i < num]
print("The new list is: {}".format(finallist))


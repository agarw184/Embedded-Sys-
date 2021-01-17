


#Fucntion to generate the Fibonnaci
def fib(fibnum):
    if (fibnum <= 1):
        return 1;
    else:
        return (fib(fibnum - 1) + fib(fibnum - 2))


#Question on how many recursions do we want to generate
fibnum = int(input("How many Fibonacci numbers would you like to generate?"))

#Loop to call the function for the respective numbers
fiblist = []
for i in range(fibnum):
    #Appends the generated numbers in the list
    fiblist.append(fib(i))

#Print statement
print("The Fibonacci Sequence is:")
for j in fiblist:
    print(j)












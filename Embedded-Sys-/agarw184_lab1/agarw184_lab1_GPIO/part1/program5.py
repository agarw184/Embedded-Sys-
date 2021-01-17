#GTA said on Piazza that all possible combinations should be printed
class Twopair:
    def twoSum(self, target, numlist):
        for i in range(len(numlist) - 1):
            for j in range(0, len(numlist)):
                #Check for target sum
                if ((numlist[i] + numlist[j]) == target):
                    #Prints the target sum
                    print("index1=" + str(i) + ", " + "index2=" + str(j))

if __name__ == "__main__":
    number = int(input("What is your target number?"))
    numlist = [10, 20, 10, 40, 50, 60, 70] #Defined list
    Twopair().twoSum(number, numlist) #Function call

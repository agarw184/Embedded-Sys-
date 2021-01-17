import random   #Importing the necessary module

#Number of guesses
numguess = 3

#Switch for lose print
switch = 0

#Randomly generated number between 0 and 10
targetnum = random.randint(0, 10)

#Takes the user input
usernum = int(input("Enter your guess:"))

#Loop that evalutes the user input and prints output "You win" if user wins.
for i in range(numguess - 1):
    if (usernum == targetnum):
        switch = 1
        print("You win!")
        break
    else:
        usernum = int(input("Enter your guess:"))

#Message if user loses!
if(switch == 0):
    print("You lose!")



#Generating the dictionary
birthdays = {"Albert Einstein": "03/14/1879",
             "Benjamin Franklin": "01/17/1706",
             "Ada Lovelace": "08/10/1815"
             }
#Welcome message
print("Welcome to the birthday dictionary. We know the birthdays of:")
for i in birthdays:
    print(i)

#Takes the input
print("Who’s birthday do you want to look up?")
name = input()

#Now iterates through the dictionary to check
for key in birthdays.keys():
    if (name == key):
        print(name + "\'s birthday is " + str(birthdays[name]))
        break
    #Error handling
    else:
        print("Name entered not in the dictionary")
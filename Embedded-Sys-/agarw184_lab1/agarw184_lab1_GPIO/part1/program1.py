#Importing Required Module
from datetime import date

#Name question
name = input("What is your name?")

#Age question
age = int(input("How old are you?"))

#Record year by the time that person would be 100
year = date.today().year + (100 - age)

#Print statement
print("{} will be 100 years old in the year {}".format(name, year))
# NAME : MUHAMMAD BILAL
# DATA ANALYSIS ASSIGNMENT
# ASSIGNMENT 1


# Student Name   
name = input("What's the student's name? ")
m1 = int(input("Enter marks for Subject 1: "))
m2 = int(input("Enter marks for Subject 2: "))
m3 = int(input("Enter marks for Subject 3: ")) 
if m1 >= 40 and m2 >= 40 and m3 >= 40:
     total = m1 + m2 + m3 
     per =total / 3 
     if per >= 40: print(name, "has Passed with", per, "%") 
     else: print(name, "has Failed with", per, "%")
else: 
     print(name, "has Failed (less than 40 in one subject)")
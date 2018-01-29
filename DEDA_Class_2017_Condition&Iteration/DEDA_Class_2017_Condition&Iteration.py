"""
Introducing the Condition and Iteration in Python
"""

"""
Condition
"""

# if() takes 1 argument to evaluate if the argument is True or False
bool_seq = [True, False, 0, 1, -1, 100, '', (), [], {}, [False], [True]]
# False, 0, empty sequence will be evaluated as False
for bool_smb in bool_seq:
    if bool_smb:
        print(bool_smb, ": This is True")
    elif not bool_smb:
        print(bool_smb, ": This is False")

# True, False, and, or
print(True or False)  # True
print(True and False)  # False
print(True or True)  # True
print(True and True)  # True
print(False and False)  # False
print(False or False)  # False

# operator "is" is not "=="
# "is" is used to evaluate if two 2 variables pointed to the same object, "==" is used to evaluate the equivalence of 2 variables
bool_seq_diff = [True, False, 0, 1, -1, 100, '', (), [], {}, [False], [True]]
print(bool_seq == bool_seq_diff)  # True
print(bool_seq is bool_seq_diff)  # False
bool_seq_same = bool_seq
print(bool_seq == bool_seq_same)  # True
print(bool_seq is bool_seq_same)  # True
# 2 variables pointed to the same object will vary simultaneously
bool_seq.append(1)
print(bool_seq)
print(bool_seq_same)

# what if I want to create different object but don't want to copy the values manually?
# The answer is deep copy, different data structure may provide different methods.
# Further more see: https://docs.python.org/3/library/copy.html
bool_seq_2 = bool_seq.copy()
print(bool_seq_2 is bool_seq)  # False

# using id(), you can check the memory address of a variable
id(bool_seq)
# the same object will have the same memory address



"""
Iteration
"""

iterate_object = ['\t', 'Digital', 'Economy', 'and', 'Decision', 'Analytics', '\n', 'in', 'Python']

"""
for loop
"""
# Important: Try not using index in the loop while do it in a pythonic way
# This is a NOT recommended way to iterate, because it's ugly and less efficient.
print("\n\t===Example 1===")
for i in range(len(iterate_object)):
    print(i)
    print(iterate_object[i])

# Using any name you want in the for loop
print("\n\t===Example 2===")
for word in iterate_object:
    print(word)

# what if I want to use the index?
print("\n\t===Example 3===")
for idx, word in enumerate(iterate_object):
    print(idx, word)

# using the keyword "continue" to skip a loop and key word "break" to stop whole loop.
print("\n\t===Example 4===")
for word in iterate_object:
    if word == '\n':
        continue
    elif word == 'in':
        print("****break in here****")
        break
    else:
        print(word)

# a loop embed in another loop
print("\n\t===Example 5===")
for word in iterate_object:
    if word == 'in':
        break
    else:
        for letter in word:
            if letter.isupper() is True:
                print(letter)

# infinite loop
num = 0
while True:
    print(num)
    num +=1









import random

def fillVariables(variables, size):
    filled = [] + variables
    for i in range(len(variables), size):
        filled.append(0)
    return filled
def plus(a, b):
    return a, b

def minus(a, b):
    return a**2, b**2


x = minus(plus(5, 6)[0], plus(5, 6)[1])


print(type(x))

print(x)


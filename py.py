def euklides(m, n): return n if m % n == 0 else euklides(n, m % n)

# Lägg till alla talets faktorer, förutom talet självt i en lista
# Om alla faktorer tillsammans blir talet returna True annars returna False
def perfect_integer(integer):
    factors = list()
    for i in range(integer-1, 0, -1):
        if integer % i == 0:
            factors.append(i)
    return True if sum(factors) == integer else False
        
print(euklides(1232, 42))
print(perfect_integer(28))
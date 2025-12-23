
a = 7
result = True
for x in range(0, 10000000):
    result *= (x % a == 0 or (x % 28 != 0 and x % 35 != 0))
print(result)

print()







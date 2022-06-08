import math

PV = 100
f = 1.03
n = 2

# Without the math package you must use the ** for exponents as follows
FV = PV * f**n
print(FV)

# However with the math module you can use that mat.pow() function
FV = PV * math.pow(f, n)
print(FV)

#Theres even more fuctions you can use with the match module as follows

math.sqrt(FV/PV) - 1 #deduct 1 for interest rate
math.sin(3)

print(math.e) # used for euler number

print(math.pi)

# You can import math as ma
import math as ma

print(ma.pi)

# you can import specific modules
from math import sqrt as sq

print(sq(FV/PV) - 1) # deduct 1 for interest
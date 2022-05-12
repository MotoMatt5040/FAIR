# FORMULAS

# Future Value

# FV = PV(1+r)^n

# FV = Future Value
# PV = Present Value (today)
# r = Interest Rate (per period)
# n = Number of periods

# Example 1 - You save 100 USD for one year at an interest rate of 3%
PV = 100.00
r = .03
n = 1

FV = PV*(1+r)**n
print(FV)
# Example 2 - You save 100 USD for three years at an interest rate of 3% p.a.
PV = 100.00
r = .03
n = 3

FV = PV*(1+r)**n
print(FV)

# Discounting

# PV = FV/(1+r)^n

# FV = Future Value
# PV = Present Value (today)
# r = Interest Rate (per period)
# n = Number of periods

# Example 1 - How many USD to save today at an interest rate of 4.5% p.a. to get 110 USD in one year?

FV = 110.00
r = .045
n = 1

PV = FV/(1+r)**n
print(PV)

# Example 2 - How many USD to save today at an interest rate of 4.5% p.a. to get 110 USD in three years?

FV = 110.00
r = .045
n = 3

PV = FV/(1+r)**n
print(PV)

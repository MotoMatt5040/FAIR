# FORMULAS

# TODO Future Value

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
print(f'Future Value = {FV}')

# Example 2 - You save 100 USD for three years at an interest rate of 3% p.a.
PV = 100.00
r = .03
n = 3

FV = PV*(1+r)**n
print(f'Future Value = {FV}')

# TODO Discounting

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
print(f'Present Value = {PV}')

# Example 2 - How many USD to save today at an interest rate of 4.5% p.a. to get 110 USD in three years?

FV = 110.00
r = .045
n = 3

PV = FV/(1+r)**n
print(f'Present Value = {PV}')

# TODO Interest Rates

# r = (FV/PV)^(1/n)-1

# Example 1 - Today you receive the offer to deposit 90 USD in a savings account, getting back 93.5 USD in one year.
FV = 93.5
PV = 90
n = 1

r = (FV/PV)**(1/n)-1

print(f'Interest Rate = {r}')

# Example 2 - Today you receive the offer to deposit 90 USD in a savings account, getting back 93.5 USD in three years.
FV = 93.5
PV = 90
n = 3

r = (FV/PV)**(1/n)-1

print(f'Interest Rate = {r}')

# TODO Stock Returns

    # TODO Price Returns

# r = ((P_(t+1))/P_t)-1

# NOTE _ represents base
# P_t = Price at timestamp t
# r = Period Return

# Example - One year ago you invested 50 USD in a stock that is now worth 56.5 USD

print(f'Price Return = {56.5 / 50 - 1}')

    # TODO Total Returns

# r = ((P_(t+1))+(D_(t+1)))/(P_t)-1 = (P_(t+1))/(P_t)-1+(D_(t+1))/(P_t)

# D = Dividend

# Example - One year ago you invested 50 USD in a stock that recently paid a Dividend of 2 USD and is now worth 56.5 USD

print(f'Total Return = {(56.5+2)/50-1}')

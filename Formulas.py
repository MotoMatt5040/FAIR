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

# TODO FV With Cashflow

# FV_N = Future Value at N
# CF_t = cashflow at timestamp t
# N = Total number of periods
# r = Interest Rate (per period)
# t = timestamp

# Example - Today you have 100 USD in your savings account and you save another
# - 10 USD in t1
# - 20 USD in t2
# - 50 USD in t3
# - 30 USD in t4
# - 25 USD in t5

n = [0, 1, 2, 3, 4, 5]
cf = [100, 10, 20, 50, 30, 25]
r = .03
f = 1+r
fv = 0
# FV = cf[0] * f**n[-1] + cf[1] * f**n[-2] + cf[2] * f**n[-3] + cf[3] * f**n[-4] + cf[4] * f**n[-5] + cf[5]

# Calculate the FV of your savings account after 5 years given an interest rate of 3% p.a.
for i in range(len(cf)):
    fv += cf[i] * f**n[-(i+1)]
print(f'Future Value = {fv}')

import numpy as np

# Numpy arrays
cf = [50, 100, 120, 150, 200, 300]
print(type(cf))

cf_a = np.array(cf) #turns list into numpy array
print(type(cf_a))
print(f"cf_a: {cf_a}")
"""For all intents and purposes, lets say we needed to deduct 20 from our list of data.
With a normal list we cannot deduct 20 from all values, we will get an error when attempting

cf - 20

We will get the same error when trying to perform any list wide data manipulation such as

cf * 1.1
cf * 2

The proper method to manipulate all the data in a list would be to use

cf_new = []
for i in cf:
    cf_new.append(i - 20)
print(cf_new)

Without iterating through each individual element, we cannot adjust the data with a normal list"""

# Moving on to numpy

"""numpy supports data adjustments using the aforementioned methods that didn't work"""

print(cf_a - 20)

"""will deduct 20 from all values in the numpy array. All other functions will work the same."""

# This is a different way of data manipulation in numpy

"""If we create an additional array in numpy that has the same amount of data as the array we would like 
to use it with, we can perform addition and subtraction the same way a matrix would perform addition 
and subtraction"""

add_cf = np.array([10, 20, -10, 30, 10, -5])

print(cf_a + add_cf)

# numpy only supports one data type
"""Trying to convert a list with multiple data types to a numpy array will store every value as a string"""
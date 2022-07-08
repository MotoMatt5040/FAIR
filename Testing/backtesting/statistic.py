def summation(list_values):
    """Function that given a list of values calculates the summation

    Args:
        list_values (list): List of values

    Returns:
        int-float: Summation value
    """
    accumulator = 0
    for value in list_values:
        accumulator += value
    return accumulator


def summation2(list_values):
    """
Function that given a list of values calculates the summation
    of all values squared

    Args:
        list_values (list): List of values

    Returns:
        int-float: Summation value
    """
    accumulator = 0
    for value in list_values:
        accumulator += value*value
    return accumulator


def mean(list_values):
    """Function that given a list of values calculates the mean.

    Args:
        list_values (list): List of values

    Returns:
        int-float: Mean
    """
    return summation(list_values) / len(list_values)


def covariance(list_x, list_y):
    """Function that calculates the covariance given two lists

    Args:
        list_x (list): List of X values
        list_y (list): List of Y values

    Returns:
        int-float: Covariance
    """
    accumulator = 0
    i = 0
    for valor in list_x:
        accumulator += valor * list_y[i]
        i+=1
    return (accumulator / len(list_x)) - (mean(list_x) * mean(list_y))


def variance(list_values):
    """Function that returns the variance given a list of values

    Args:
        list_values (list): List with values

    Returns:
        int-float: Variance
    """
    return summation2(list_values) / len(list_values) - mean(list_values) ** 2

   
def slope(list_x, list_y):
    """Function that given two lists, returns the slope of the
    regression line. Both lists must have the same length

    Args:
        list_x (list): X values
        list_y (list): Y values

    Returns:
        int-float: Slope of the line
    """
    return covariance(list_x, list_y) / variance(list_x)


def slopeY(list_y):
    """
Function that given a list, returns the slope of the
    regression line. Two lists are needed, list X is
    fill with 1, 2, 3... up to the number of elements in the list AND
    Both lists must have the same length

    Args:
        list_y (list): Y values

    Returns:
        int-float: Slope of the line
    """
    lista_x = []
    for i in range(len(list_y)):
        lista_x.append(i+1)
    return covariance(lista_x, list_y) / variance(lista_x)
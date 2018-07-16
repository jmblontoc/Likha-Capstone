from friends.datamining import correlations


# get slope of regression line
def get_slope(r, numbers):

    sv_x = get_standard_deviation(numbers, 0)
    sv_y = get_standard_deviation(numbers, 1)

    return r * (sv_y / sv_x)


# get y intercept
def get_y_intercept(r, numbers):

    return correlations.get_means(numbers)[1] - (get_slope(r, numbers) * correlations.get_means(numbers)[0])


# get main equation
# returns a string(?)
def get_equation_string(r, numbers):

    a = round(get_y_intercept(r, numbers), 2)
    b = round(get_slope(r, numbers), 2)

    return 'y = ' + str(a) + ' + (' + str(b) + ')x'


def get_line(r, numbers):

    a = round(get_y_intercept(r, numbers), 2)
    b = round(get_slope(r, numbers), 2)

    return [[0, a], [-a / b, 0]]


def get_variables(r, numbers):

    a = round(get_y_intercept(r, numbers), 2)
    b = round(get_slope(r, numbers), 2)

    return [a, b]


def get_standard_deviation(numbers, n):

    mean = correlations.get_means(numbers)[n]

    sum = 0
    for number in numbers:
        sum = sum + ((number[n] - mean) ** 2)

    sv = (sum / (len(numbers) - 1)) ** 0.5
    return sv

# # # # # # # # # # # # # # # # # # WEIGHTED MOVING AVERAGE # # # # # # # # # # # # # # # #

def get_weights(n):

    weights = []

    # get the denominator
    sum = 0
    for x in range(1, n + 1):
        sum = float(sum) + x

    for x in range(1, n + 1):
        weights.append(round(x / sum, 2))

    return weights


# data must be a list
def get_weighted_moving_average(data):

    length = len(data)
    weights = get_weights(length)

    sum = 0
    for x in range(0, length):
        sum = sum + (data[x] * weights[x])

    return round(sum, 2)


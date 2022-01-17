import numpy as np


def x_moving_average(raw_array, x):
    averaged_array = np.array([])
    tba = raw_array[len(raw_array) - x:]

    for i in range(len(raw_array) - x):
        sumlist = []
        for k in range(i+1, i + x + 1):
            sumlist.append(raw_array[k])
        print(sumlist)
        print(sum(sumlist)/x)

        averaged_array = np.append(averaged_array, sum(sumlist)/x)

    averaged_array = np.append(averaged_array, tba)
    return averaged_array


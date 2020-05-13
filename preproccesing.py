import math
from itertools import zip_longest
from pandas import *
import scipy.interpolate as interp

def work_your_magic(raw_arr):
    raw_arr = zip_longest(*preprocess_csv(raw_arr))
    final_array = []
    for line in raw_arr:
        arr = np.array([])
        for item in line:
            if item == ' ' or item == '' or item == np.nan or item is None:
                pass
            else:
                arr = np.append(arr, item)

        final_array.append(arr)

    new_final_array = []
    for row in final_array:
        if len(row) < 150:
            row_interp = interp.interp1d(np.arange(row.size), row)
            row_stretch = row_interp(np.linspace(0, row.size - 1, 150))
            new_final_array.append(row_stretch)
        else:
            new_final_array.append(row)

    final_array = zip_longest(*new_final_array)
    last_array = []
    for row in final_array:
        row = np.asarray(row)
        if len(row) < 20:  # stretch
            row_interp = interp.interp1d(np.arange(row.size), row)
            row_stretch = row_interp(np.linspace(0, row.size - 1, 20))
            last_array.append(row_stretch)
        elif len(row) > 20:  # compress
            row_interp = interp.interp1d(np.arange(row.size), row)
            row_compress = row_interp(np.linspace(0, row.size - 1, 20))
            last_array.append(row_compress)
        else:
            last_array.append(row)

    return last_array

def preprocess_csv(raw_arr):
    in_csv = zip_longest(*raw_arr)
    new_2d_array = []
    for line in in_csv:
        arr = []
        for item in line:
            if item is None or item == '' or item == ' ':
                arr.append(' ')
            else:
                arr.append(abs(float(item)))
        new_2d_array.append(arr)

    #     new_2d_array = list(zip_longest(*new_2d_array))
    to_delete = []
    for index, row in enumerate(new_2d_array):
        zeroes = 0
        non_zeroes = 0
        empty = 0
        for item in row:
            if item == 0:
                zeroes += 1
            elif item != ' ' and item != 0:
                non_zeroes += 1
            elif item == ' ':
                empty += 1
        if zeroes > non_zeroes or empty / 3 > non_zeroes:
            to_delete.append(row)

    for row in to_delete:
        new_2d_array.remove(row)

    #     new_2d_array = [append(item)]
    return zip_longest(*new_2d_array)
def featuresCalc(arr):
    time = 5
    i = 0
    matrix = []
    minX = 999
    minY = 999
    count = 0
    PatternCounter = -1

    for i in range(1, len(arr) - 1):
        normalCounteer = 0
        maxX = arr[i - 1][normalCounteer]
        maxY = arr[i - 1][normalCounteer + 1]

        for j in range(0, (len(arr[i])), 2):

            if (j + 1 < len(arr[i - 1])):
                x = (arr[i][j]) - (arr[(i - 1)][j])
                y = (arr[i][j + 1]) - (arr[i - 1][j + 1])
                x2 = (arr[i][j])
                x1 = (arr[i - 1][j])
                y2 = (arr[i][j + 1])
                y1 = (arr[i - 1][j + 1])

                distance_no_root = pow((arr[i][j]) - int(arr[i - 1][j]), 2) + pow((arr[i][j + 1]) - (arr[i - 1][j + 1]),
                                                                                  2)
                dist = math.sqrt(distance_no_root)
                Speed = int(((dist / time)+10))
                if (x2 < x1 and y2 == y1):
                    # print(x)
                    # print(y)
                    # print("West")
                    dir = 4
                elif (x2 < x1 and y2 > y1):
                    # print(x)
                    # print(y)
                    # print("North West")
                    dir = 8
                elif (x2 < x1 and y2 < y1):
                    # print(x)
                    # print(y)
                    # print("South West")
                    dir = 7
                elif (x2 > x1 and y2 == y1):
                    # print(x)
                    # print(y)
                    # print("East")
                    dir = 2
                elif (x2 > x1 and y2 > y1):
                    # print(x)
                    # print(y)
                    # print("North East")
                    dir = 5
                elif (x2 > x1 and y2 < y1):

                    dir = 6
                elif (x2 == x1 and y2 > y1):

                    dir = 1
                elif (x2 == x1 and y2 < y1):

                    dir = 3
                elif (x2 == x1 and y2 == y1):
                    # print(x2)
                    # print(x1)
                    # print("Didn't move")
                    dir = 0

                if (i == 1):
                    if (dir != 0):
                        count = 1
                else:
                    PatternCounter += 5
                    if (dir != 0):
                        try:
                            count = matrix[i - 2][PatternCounter] + 10
                        except IndexError:
                            count = 1
                    else:
                        try:
                            count = matrix[i - 2][PatternCounter]
                        except IndexError:
                            count = 10

                if (arr[i - 1][normalCounteer] > maxX):  # Xmax
                    maxX = arr[i - 1][normalCounteer]
                elif (minX > arr[i - 1][normalCounteer]):  # Xmin
                    minX = arr[i - 1][normalCounteer]
                if (arr[i - 1][normalCounteer + 1] > maxY):  # Ymax
                    maxY = arr[i - 1][normalCounteer + 1]
                elif (minY > arr[i - 1][normalCounteer + 1]):  # Ymin
                    minY = arr[i - 1][normalCounteer + 1]

                if (j == 0):
                    matrix.append([arr[i - 1][normalCounteer], arr[i - 1][normalCounteer + 1], Speed, dir, count])
                else:
                    matrix[i - 1].append(arr[i - 1][normalCounteer])
                    matrix[i - 1].append(arr[i - 1][normalCounteer + 1])
                    matrix[i - 1].append(Speed)
                    matrix[i - 1].append(dir)
                    matrix[i - 1].append(count)
                normalCounteer += 2

        PatternCounter = -1
        MaxDistance = pow(maxX - minX, 2) + pow(maxY - minY, 2)
        dist = math.sqrt(MaxDistance)
        # matrix+=[dist]
        matrix[i - 1].append(dist)
    return matrix

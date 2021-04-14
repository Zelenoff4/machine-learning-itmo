import math


def manhattan_distance(a, b):
    return sum(abs(a_feature - b_feature) for a_feature, b_feature in zip(a, b))


def euclidean_distance(a, b):
    return math.sqrt(sum((a_features - b_features) * (a_features - b_features) for a_features, b_features in zip(a, b)))


def chebyshev_distance(a, b):
    return max(abs(a_features - b_features) for a_features, b_features in zip(a, b))


def uniform_kernel(x):
    return 0.5 if x < 1 else 0


def triangular_kernel(x):
    return 1 - x if x <= 1 else 0


def epanechnikov_kernel(x):
    return 0.75 * (1 - x ** 2) if x <= 1 else 0


def quartic_kernel(x):
    return 15 / 16 * (1 - x ** 2) ** 2 if x <= 1 else 0


def triweight_kernel(x):
    return 35 / 32 * (1 - x ** 2) ** 3 if x <= 1 else 0


def tricube_kernel(x):
    return 70 / 81 * (1 - x ** 3) ** 3 if x <= 1 else 0


def gaussian_kernel(x):
    return 1 / math.sqrt(2 * math.pi) * math.e ** (-1 / 2 * x ** 2)


def cosine_kernel(x):
    return math.pi / 4 * math.cos(math.pi / 2 * x) if x <= 1 else 0


def logistic_kernel(x):
    return 1 / (math.e ** x + 2 + math.e ** (-x))


def sigmoid_kernel(x):
    return 2 / math.pi * 1 / (math.e ** x + math.e ** (-x))


def main():
    n, k = map(int, input().split())
    objects = []
    for i in range(n):
        data = list(map(int, input().split()))
        objects.append((data[:-1], data[-1]))
    request_object = list(map(int, input().split()))

    distance_function = input()
    kernel_function = input()
    window = input()
    window_parametr = int(input())

    kernels = {
        'uniform': uniform_kernel,
        'triangular': triangular_kernel,
        'epanechnikov': epanechnikov_kernel,
        'quartic': quartic_kernel,
        'triweight': triweight_kernel,
        'tricube': tricube_kernel,
        'gaussian': gaussian_kernel,
        'cosine': cosine_kernel,
        'logistic': logistic_kernel,
        'sigmoid': sigmoid_kernel,
    }

    # for kernel in kernels.values():
    #     print(kernel(100))

    distances = {
        'euclidean': euclidean_distance,
        'manhattan': manhattan_distance,
        'chebyshev': chebyshev_distance,
    }

    distance = distances[distance_function]
    kernel = kernels[kernel_function]

    # print(objects)
    objects.sort(key=lambda x: distance(x[0], request_object))
    if window == 'variable':
        window_parametr = distance(objects[window_parametr][0], request_object)
    # print(objects)

    try:
        if window_parametr != 0:
            numerator = sum(
                known_object[1] * kernel(distance(known_object[0], request_object) / window_parametr)
                for known_object in objects
            )

            denominator = sum(
                kernel(distance(known_object[0], request_object) / window_parametr)
                for known_object in objects
            )
            print("%.15f" % (numerator / denominator))
        else:
            s = 0
            good_points = 0
            summ = 0
            for known_object in objects:
                if distance(known_object[0], request_object) == 0:
                    s += known_object[1]
                    good_points += 1
                summ += known_object[1]
            if good_points != 0:
                print("%.15f" % (s / good_points))
            else:
                print("%.15f" % (summ / n))
    except ZeroDivisionError:
        print("%.15f" % (sum(known_object[1] for known_object in objects) / n))


if __name__ == '__main__':
    main()

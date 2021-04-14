def main():
    m = int(input())
    matrix = [0] * (2 ** m)
    for i in range(2 ** m):
        matrix[i] = int(input())
    # print(matrix)
    net = [[], []]
    first = []
    second = []
    for i in range(2 ** m):
        first.append([0] * (m + 1))
    second.append([0] * (2 ** m + 1))
    net[0] = first
    net[1] = second
    net[1][0][2 ** m] = -0.5
    # print(first)
    # print(net)
    for i in range(2 ** m):
        if matrix[i]:
            net[0][i][m] = 0.5
            net[1][0][i] = 1
            for j in range(m):
                if (i >> j) & 1:
                    net[0][i][j] += 1e5
                    net[0][i][m] -= 1e5
                else:
                    net[0][i][j] -= 1e5
        else:
            net[0][i][m] = -0.5

    print(2)
    print(2 ** m, 1)
    for i in range(2):
        for j in range(len(net[i])):
            print(*net[i][j])


if __name__ == '__main__':
    main()

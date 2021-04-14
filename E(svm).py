def main():
    n = int(input())
    scalar_mps = []
    ys = []
    for i in range(n):
        line = input().split()
        scalar_mps.append(list(map(int, line[:-1])))
        ys.append(int(line[-1]))

    lambda_coeff = int(input())

    lambdas = [0] * n

    for _ in range(9):
        for i in range(n):
            for j in range(i + 1, n):
                same_class = 1 if ys[i] == ys[j] else -1
                a = (-same_class) * ys[i] * ys[j] * scalar_mps[i][j] + 0.5 * (ys[i] ** 2) * scalar_mps[i][i] + 0.5 * (ys[j] ** 2) * scalar_mps[j][j]

                b = -2 if same_class < 0 else 0
                for l in range(len(lambdas)):
                    # b += lambdas[l] * ys[l] * ys[i] * scalar_mps[i][l]
                    b += lambdas[l] * ys[l] * (scalar_mps[i][l] * ys[i] + (-same_class) * scalar_mps[j][l] * ys[j])

                left = max(-lambdas[i], -lambdas[j]) if same_class < 0 \
                    else max(-lambdas[i], lambdas[j] - lambda_coeff)
                right = min(lambda_coeff - lambdas[i], lambda_coeff - lambdas[j]) if same_class < 0 \
                    else min(lambda_coeff - lambdas[i], lambdas[j])
                middle = -b / (2 * a)
                # print(a, left, right, middle)
                if a < 0:
                    if (middle > right) or (abs(middle - left) > abs(middle - right)):
                        lambdas[i] += left
                        lambdas[j] += left if same_class < 0 else -left
                    else:
                        lambdas[i] += right
                        lambdas[j] += right if same_class < 0 else -right
                else:
                    if middle < left:
                        lambdas[i] += left
                        lambdas[j] += left if same_class < 0 else -left
                    elif middle > right:
                        lambdas[i] += right
                        lambdas[j] += right if same_class < 0 else -right
                    else:
                        lambdas[i] += middle
                        lambdas[j] += middle if same_class < 0 else -middle

    # print(*list(map(lambda x: lambda_coeff - x, lambdas)), sep='\n')
    # print(*lambdas, sep='\n')
    for i in range(n):
        print("%.15f" % lambdas[i])

    shift = 0
    ind = n - 1
    for i in range(len(lambdas) - 1, -1, -1):
        if lambdas[i] != 0:
            shift = ys[i]
            ind = i
            break
    tmp = 0
    for j in range(n):
        tmp += scalar_mps[j][ind] * ys[j] * lambdas[j]
    print("%.15f" % (shift - tmp))


if __name__ == '__main__':
    main()

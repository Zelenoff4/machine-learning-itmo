def main():
    n = int(input())
    xs = []
    ys = []
    for i in range(n):
        x, y = map(int, input().split())
        xs.append((x, i))
        ys.append((y, i))

    xs.sort()
    ys.sort()
    # print(xs)
    # print(ys)

    ranks_xs = [0] * n
    ranks_ys = [0] * n
    for i in range(n):
        ranks_xs[xs[i][1]] = i
        ranks_ys[ys[i][1]] = i
    ans = 0
    for i in range(n):
        ans += (ranks_xs[i] - ranks_ys[i]) ** 2
    numerator = 6 * ans
    denominator = n * (n ** 2 - 1)
    print("%.10f" % (1 - numerator / denominator))


if __name__ == '__main__':
    main()
def main():
    n, m = map(int, input().split())
    xs = []
    ys = []
    for i in range(n):
        line = input().split()
        xs.append(list(map(int, line[:-1])))
        ys.append(int(line[-1]))
    print(xs)

    overall_max = max(
        max(
            max(list(map(abs, array)))
            for array in xs
        ),
        max(list(map(abs, ys)))
    )

    for i in range(n):
        xs[i] = [item / overall_max for item in xs[i]]
    print(xs)
    ys = [item / overall_max for item in ys]
    print(ys)


if __name__ == '__main__':
    main()

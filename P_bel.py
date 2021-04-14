def main():
    _ = int(input())
    n = int(input())
    objects = [tuple(map(int, input().split())) for _ in range(n)]
    xs = [obj[0] for obj in objects]
    ys = [obj[1] for obj in objects]
    cnt_x = {}
    cnt_xy = {}
    for x, y in zip(xs, ys):
        if x not in cnt_x.keys():
            cnt_x[x] = 0
        if (x, y) not in cnt_xy.keys():
            cnt_xy[(x, y)] = 0
        cnt_x[x] += 1
        cnt_xy[(x, y)] += 1
    # print(cnt_x, cnt_xy)
    sum_sq = {}
    sum_lin = {}
    for (x, y), count in cnt_xy.items():
        if x not in sum_lin.keys():
            sum_lin[x] = 0
            sum_sq[x] = 0
        probability = count / cnt_x[x]
        print(probability)
        sum_lin[x] += y * count / cnt_x[x]
        sum_sq[x] += y * y * count / cnt_x[x]
    print(sum_lin)
    print(sum_sq)
    answer = 0
    for x in sum_lin.keys():
        answer += cnt_x[x] / n * (sum_sq[x] - sum_lin[x] ** 2)
    # print('{:.12f} {:.12f}'.format(sum_sq, sum_lin))
    # print('{:.12f}'.format(sum_sq - sum_lin ** 2))
    print('{:.12f}'.format(answer))


if __name__ == '__main__':
    main()
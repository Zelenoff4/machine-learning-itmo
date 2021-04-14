def sum_dist(xs):
    xs = sorted(xs)
    cur_sum = 0
    answer = 0
    for i, x in enumerate(xs):
        cur_sum += x
        answer += x * (i + 1) - cur_sum
    return 2 * answer


def main():
    _ = int(input())
    n = int(input())
    objects = [tuple(map(int, input().split())) for _ in range(n)]
    xs = [obj[0] for obj in objects]
    ys = [obj[1] for obj in objects]
    all_dist = sum_dist(xs)
    grouped_xs = {}
    for x, y in zip(xs, ys):
        if y not in grouped_xs:
            grouped_xs[y] = []
        grouped_xs[y].append(x)
    inner_dist = sum(sum_dist(cur_xs) for cur_xs in grouped_xs.values())
    outer_dist = all_dist - inner_dist
    print(inner_dist)
    print(outer_dist)


if __name__ == '__main__':
    main()
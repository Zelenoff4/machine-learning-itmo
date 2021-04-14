
def main():
    # fin = open('input.txt', 'r')
    # fout = open('output.txt', 'w')
    n, m, k = map(int, input().split())
    class_ids = [class_id - 1 for class_id in list(map(int, input().strip().split()))]
    classes = []
    for i in range(m):
        classes.append([])
    for i in range(n):
        classes[class_ids[i]].append(i)

    ans = []
    for i in range(k):
        ans.append([])

    position_index = 0
    for i in range(m):
        for item in classes[i]:
            ans[position_index].append(item)
            position_index = (position_index + 1) % k

    for i in range(k):
        print(len(ans[i]), *sorted([item + 1 for item in ans[i]]))


if __name__ == '__main__':
    main()

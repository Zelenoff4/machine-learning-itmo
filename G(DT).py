class Node:
    def __init__(self, node_id, value, node_type):
        self.id = node_id
        if node_type == 'leaf':
            self.value = value
        else:
            self.left = None
            self.right = None
            self.question = None


def build_tree(sorted_by_feature_objects, node_id, max_height):
    objects = sorted_by_feature_objects[0]
    classes = [data[1] for data in objects]
    counts = [(classes.count(cur), cur) for cur in set(classes)]
    most_frequent_class_id = counts[-1][1]
    print(counts)


def main():
    m, k, h = map(int, input().split())
    n = int(input())
    train = []
    for i in range(n):
        line = input().split()
        train.append((
            list(map(int, line[:-1])),
            int(line[-1])
        ))

    sorted_by_feature_number = []
    for i in range(m):
        sorted_by_feature_number.append(sorted(train, key=lambda x: x[0][i]))

    build_tree(sorted_by_feature_number, 1, h)



if __name__ == '__main__':
    main()

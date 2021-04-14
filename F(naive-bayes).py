import math
from collections import defaultdict


class DataObject:
    def __init__(self, class_id, words):
        self.class_id = class_id
        self.words = words


class ClassData:
    def __init__(self, class_id):
        self.aprior_prob = 0
        self.prob = 0
        self.words = set()
        self.appearances = 0
        self.id = class_id
        # self.size = 0
        self.words_appearances = defaultdict(int)

    def add_word(self, word):
        self.words.add(word)

    def add_appearance(self):
        self.appearances += 1

    # def add_size(self, size_to_add):
    #     self.size += size_to_add

    def set_aprior_prob(self, overall_appearances):
        self.aprior_prob = self.appearances / overall_appearances


def main():
    k = int(input())
    lambdas = list(map(int, input().split()))
    alpha = int(input())
    n = int(input())

    train = []
    for i in range(n):
        line = input().split()
        train.append(DataObject(int(line[0]) - 1, list(set(line[2:]))))

    test = []
    m = int(input())
    for i in range(m):
        line = input().split()
        test.append(DataObject(-1, list(set(line[1:]))))

    # aprior_probs = []
    # class_probs = {}
    # class_words = [set() for _ in range(k)]
    # class_appearences = {}
    # classes = {}
    classes = [ClassData(i) for i in range(k)]
    # for i in range(k):
    #     classes[i + 1] = ClassData(i + 1)

    for train_data in train:
        # class_words[train_data.class_id].add(train_data.words)
        current_class = classes[train_data.class_id]
        # current_class.add_size(len(train_data.words))
        current_class.add_appearance()
        for word in train_data.words:
            current_class.add_word(word)
            if word in current_class.words_appearances:
                current_class.words_appearances[word] += 1
            else:
                current_class.words_appearances[word] = 1

    # train_classes_appearances = sum(class_data.appearances for class_data in classes.values())
    train_classes_appearances = sum(class_data.appearances for class_data in classes)
    for i in range(k):
        current_class = classes[i]
        current_class.set_aprior_prob(train_classes_appearances)

    for test_data in test:
        logarithms = [
            0 if current_class.appearances == 0 else
            math.log(lambdas[current_class.id]) + math.log(current_class.aprior_prob)
            # for current_class in classes.values()
            for current_class in classes
        ]
        for word in test_data.words:
            for i in range(k):
                # current_class = classes[i + 1]
                current_class = classes[i]
                probability = 1
                try:
                    numerator = current_class.words_appearances[word] + alpha
                    denominator = current_class.appearances + alpha * len(current_class.words)
                    probability = numerator / denominator
                except ZeroDivisionError:
                    pass
                logarithms[i] += math.log(probability)
        min_log = min(logarithms)
        # try:
        # predictions = [
        #     0 if classes[i].appearances == 0 else
        #     math.e ** (logarithms[i] - min_log)
        #     for i in range(k)
        # ]
        predictions = []
        for i in range(k):
            if classes[i].appearances == 0:
                predictions.append(0.)
            else:
                try:
                    predictions.append(math.e ** (logarithms[i] - min_log))
                except OverflowError:
                    predictions.append(0.)

        tmp = sum(predictions)
        for i in range(len(predictions)):
            predictions[i] /= tmp
        print(*predictions)

    # print(logarithms)


def gen_tests():
    import random, string
    for w in range(10):
        random.seed()
        k = random.randint(1, 10)
        lambdas = [random.randint(1, 10) for _ in range(k)]
        alpha = random.randint(1, 10)
        n = random.randint(1, 200)
        # classes = [ClassData(i) for i in range(k)]
        train = []
        for i in range(n):
            class_id = random.randint(1, max(k - 1, 1))
            words_number = random.randint(1, 10 ** 4)
            words = [random.choice(string.ascii_lowercase) for _ in range(words_number)]
            train.append(DataObject(class_id - 1, words))

        m = random.randint(1, 200)
        test = []
        for i in range(m):
            # class_id = random.randint(1, k)
            words_number = random.randint(1, 10 ** 4)
            words = [random.choice(string.ascii_lowercase) for _ in range(words_number)]
            test.append(DataObject(-1, words))

        classes = [ClassData(i) for i in range(k)]
        # for i in range(k):
        #     classes[i + 1] = ClassData(i + 1)

        for train_data in train:
            # class_words[train_data.class_id].add(train_data.words)
            current_class = classes[train_data.class_id]
            # current_class.add_size(len(train_data.words))
            current_class.add_appearance()
            for word in train_data.words:
                current_class.add_word(word)
                if word in current_class.words_appearances:
                    current_class.words_appearances[word] += 1
                else:
                    current_class.words_appearances[word] = 1

        # train_classes_appearances = sum(class_data.appearances for class_data in classes.values())
        train_classes_appearances = sum(class_data.appearances for class_data in classes)
        for i in range(k):
            current_class = classes[i]
            current_class.set_aprior_prob(train_classes_appearances)

        for test_data in test:
            logarithms = [
                0 if current_class.appearances == 0 else
                math.log(lambdas[current_class.id]) + math.log(current_class.aprior_prob)
                # for current_class in classes.values()
                for current_class in classes
            ]
            for word in test_data.words:
                for i in range(k):
                    # current_class = classes[i + 1]
                    current_class = classes[i]
                    probability = 1
                    try:
                        numerator = current_class.words_appearances[word] + alpha
                        denominator = current_class.appearances + alpha * len(current_class.words)
                        probability = numerator / denominator
                    except ZeroDivisionError:
                        pass
                    logarithms[i] += math.log(probability)
            min_log = min(logarithms)
            print(min_log, logarithms, classes[logarithms.index(min_log)].appearances)
            predictions = [
                0 if classes[i].appearances == 0 else
                math.e ** (logarithms[i] - min_log)
                for i in range(k)
            ]
            tmp = sum(predictions)
            for i in range(len(predictions)):
                predictions[i] /= tmp
            # print(*predictions)


if __name__ == '__main__':
    main()

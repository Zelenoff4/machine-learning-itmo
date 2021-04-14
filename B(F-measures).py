def calc_precision(tp, fp):
    return 0 if not tp else tp / (tp + fp)


def calc_recall(tp, fn):
    return 0 if not tp else tp / (tp + fn)


def main():
    k = int(input())
    classes = [0] * k
    rows = [0] * k
    columns = [0] * k
    precisions = [0.0] * k
    recalls = [0.0] * k
    f_measures = [0.0] * k

    cm = []

    total_elements = 0
    for i in range(k):
        line = list(map(int, input().split()))
        cm.append(line)
        for j in range(len(line)):
            classes[i] += line[j]
            total_elements += line[j]
            rows[i] += line[j]
            columns[j] += line[j]

    # print(classes, total_elements, rows, columns)
    for i in range(k):
        tp = cm[i][i]
        fp = columns[i] - tp
        fn = rows[i] - tp

        precisions[i] = calc_precision(tp, fp)
        recalls[i] = calc_recall(tp, fn)
        f_measures[i] = 0 if not tp else (2 * precisions[i] * recalls[i]) / (recalls[i] + precisions[i])

    overall_precision = 0.0
    overall_recall = 0.0
    overall_f_micro_measure = 0.0

    # print(precisions, recalls, f_measures)
    for i in range(k):
        overall_precision += precisions[i] * classes[i]
        overall_recall += recalls[i] * classes[i]
        overall_f_micro_measure += f_measures[i] * classes[i]

    # print(overall_precision, overall_recall, overall_f_micro_measure)

    overall_f_macro_measure = (2 * overall_recall * overall_precision) / (overall_recall + overall_precision)
    overall_f_macro_measure /= total_elements
    overall_f_micro_measure /= total_elements

    print("%.12f" % overall_f_macro_measure, "%.12f" % overall_f_micro_measure, sep='\n')


if __name__ == '__main__':
    main()

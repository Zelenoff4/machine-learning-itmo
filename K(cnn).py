from copy import deepcopy


def get_array(n, d):
    return [[[0] * d for _ in range(n)] for _ in range(n)]


class Node:
    def __init__(self, matrix):
        self.matrix = matrix
        self.derivatives = None
        self.dimensions = len(matrix), len(matrix[0][0])

    def set_derivatives(self, derivatives):
        self.derivatives = derivatives

    def forward(self):
        pass

    def backprop(self):
        pass

    def print_matrix(self):
        n, d = self.dimensions
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    print(self.matrix[i][j][k], end=' ')
        print()

    def print_derivatives(self):
        n, d = self.dimensions
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    print(self.derivatives[i][j][k], end=' ')
        print()

    def print_parameter_derivative(self):
        raise NotImplementedError


class Pool(Node):
    def __init__(self, matrix, s, prev_node):
        super().__init__(matrix)
        self.s = s
        self.prev_node = prev_node
        self.dimensions = (prev_node.dimensions[0] + s - 1) // s, prev_node.dimensions[1]
        self.indexes = get_array(self.dimensions[0], self.dimensions[1])

    def forward(self):
        n, d = self.dimensions
        n1, d1 = self.prev_node.dimensions
        self.matrix = get_array(n, d)
        # print(self.prev_node.matrix, 'pool prev matrix', n1)
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    local_indexes = []
                    maxv = None
                    for i_stride in range(self.s):
                        for j_stride in range(self.s):
                            new_i = i * self.s + i_stride
                            new_j = j * self.s + j_stride
                            if new_i < n1 and new_j < n1:
                                value = self.prev_node.matrix[new_i][new_j][k]
                                # print(maxv, value, maxv == value)
                                if maxv is None or maxv < value:
                                    # if not maxv or maxv < value:
                                    #     maxv = value
                                    #     local_indexes = [(new_i, new_j)]
                                    # elif maxv == value:
                                    #     local_indexes.append((new_i, new_j))
                                    maxv = value
                                    local_indexes = [(new_i, new_j)]

                                elif maxv == value:
                                    local_indexes.append((new_i, new_j))
                                    # print('added %s here' % maxv, (new_i, new_j))
                                # if not maxv or maxv < value:
                                #     maxv = value
                                #     local_indexes = [(new_i, new_j)]
                                # elif maxv == value:
                                #     local_indexes.append((new_i, new_j))
                    self.matrix[i][j][k] = maxv
                    self.indexes[i][j][k] = local_indexes

    def backprop(self):
        n, d = self.dimensions
        n1, d1 = self.prev_node.dimensions
        ans = get_array(n1, d1)
        # print(self.derivatives, 'derivs in pool', self.indexes)
        for i in range(n):
            for j in range(n):
                for k in range(d):
                    for new_i, new_j in self.indexes[i][j][k]:
                        ans[new_i][new_j][k] = self.derivatives[i][j][k]
        # print(ans, 'derivs to be sent to relu')
        self.prev_node.derivatives = ans


class Relu(Node):
    def __init__(self, matrix, alpha, prev_node):
        super().__init__(matrix)
        self.alpha = alpha
        self.prev_node = prev_node
        self.dimensions = prev_node.dimensions

    def _func(self, x):
        return x if x >= 0 else self.alpha * x

    def _derivative(self, x):
        return 1 if x >= 0 else self.alpha

    def apply_rlu(self, a, matrix):
        ans = []
        for i in range(len(matrix)):
            ans.append([0] * len(matrix[0]))

        for i in range(len(ans)):
            for j in range(len(ans[i])):
                ans[i][j] = matrix[i][j] if matrix[i][j] >= 0 else a * matrix[i][j]
        return ans

    def forward(self):
        self.matrix = get_array(*self.dimensions)
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[0]):
                for k in range(self.dimensions[1]):
                    self.matrix[i][j][k] = self._func(self.prev_node.matrix[i][j][k])

    def backprop(self):
        n, d = self.dimensions
        derivatives = deepcopy(self.derivatives)
        # print(derivatives)
        for i in range(n):
            for j in range(n):
                for k in range(d):
                    derivatives[i][j][k] *= self._derivative(self.prev_node.matrix[i][j][k])

        self.prev_node.derivatives = derivatives


class Bias(Node):
    def __init__(self, matrix, bias, prev_node):
        super().__init__(matrix)
        self.bias = bias
        self.prev_node = prev_node
        self.dimensions = prev_node.dimensions
        self.parameter_derivative = [0] * self.dimensions[1]

    def forward(self):
        n, d = self.dimensions
        self.matrix = [[[self.prev_node.matrix[i][j][k] + self.bias[k] for k in range(d)] for j in range(n)] for i in range(n)]
        # print(self.matrix, 'matrix in bias', self.matrix[0][0])

    def get_parameter_derivative(self):
        n, d = self.dimensions
        parameter_derivative = [0] * d
        for k in range(d):
            s = 0
            for vec in self.derivatives:
                for subvec in vec:
                    s += subvec[k]
            parameter_derivative[k] += s
        self.parameter_derivative = parameter_derivative

    def backprop(self):
        self.prev_node.derivatives = deepcopy(self.derivatives)
        self.get_parameter_derivative()

    def print_parameter_derivative(self):
        print(*self.parameter_derivative)


def read_matrix_from_line(n, d, line):
    line = list(map(int, line))
    tmp = [[[line[i * n * n + j * n + k] for k in range(n)] for j in range(n)] for i in range(d)]
    ans = [[[0] * d for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(d):
                ans[i][j][k] = tmp[k][i][j]
    return ans


def cycle_mapper(n, i):
    return (i + n) % n


def mirror_mapper(n, i):
    if i < 0:
        return mirror_mapper(n, abs(i))
    if i < n:
        return i
    else:
        return mirror_mapper(n, n - 2 - (i - n))


def border_mapper(n, i):
    if i < 0:
        return 0
    if i < n:
        return i
    else:
        return n - 1


class CNV(Node):
    def __init__(self, matrix, h, k, s, p, a, prev_node):
        super().__init__(matrix)
        self.h = h
        self.k = k
        self.s = s
        self.p = p
        self.a = a
        self.prev_node = prev_node
        self.old_dimension = self.dimensions[1]
        self.dimensions = (self.dimensions[0] + 2 * p - k) // s + 1, h
        self.new_matrix = None
        self.old_indexes = []
        self.parameter_derivative = []

    def get_parameter_derivative(self):
        n, d = self.dimensions
        parameter_derivative = [[[[0] * self.k for _ in range(self.k)] for _ in range(self.old_dimension)] for _ in range(self.h)]
        # print(self.derivatives)
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    for i_stride in range(self.k):
                        for j_stride in range(self.k):
                            for t in range(self.old_dimension):
                                parameter_derivative[k][t][i_stride][j_stride] += self.new_matrix[i * self.s + i_stride][j * self.s + j_stride][t] * self.derivatives[i][j][k]
        self.parameter_derivative = parameter_derivative

    def backprop(self):
        n, d = self.dimensions
        n1, d1 = self.prev_node.dimensions
        derivatives = get_array(n1, d1)
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    for i_stride in range(self.k):
                        for j_stride in range(self.k):
                            old_i = self.old_indexes[i * self.s + i_stride][j * self.s + j_stride][0]
                            old_j = self.old_indexes[i * self.s + i_stride][j * self.s + j_stride][1]
                            for t in range(self.old_dimension):
                                derivatives[old_i][old_j][t] += self.derivatives[i][j][k] * self.a[k][t][i_stride][j_stride]

        self.prev_node.derivatives = derivatives

        self.get_parameter_derivative()

    def print_parameter_derivative(self):
        # print(len(self.parameter_derivative), self.h)
        # print(self.parameter_derivative)
        for t in range(self.h):
            for i in range(self.old_dimension):
                for j in range(self.k):
                    for k in range(self.k):
                        print(self.parameter_derivative[t][i][j][k], end=' ')
        print()


class CNVE(CNV):
    def __init__(self, matrix, h, k, s, p, a, prev_node):
        super(CNVE, self).__init__(matrix, h, k , s, p, a, prev_node)

    def forward(self):
        n, d = self.prev_node.dimensions
        new_dimension = n + self.p * 2
        new_matrix = get_array(new_dimension, d)
        old_indexes = []
        for i in range(new_dimension):
            old_indexes.append([0] * new_dimension)

        for i in range(new_dimension):
            for j in range(new_dimension):
                for k in range(d):
                    new_i = border_mapper(n, i - self.p)
                    new_j = border_mapper(n, j - self.p)
                    new_matrix[i][j][k] = self.prev_node.matrix[new_i][new_j][k]
                    old_indexes[i][j] = [new_i, new_j]

        self.new_matrix = new_matrix
        self.old_indexes = old_indexes
        self.matrix = get_array(*self.dimensions)

        for k in range(d):
            for i in range(n):
                for j in range(n):
                    s = 0
                    for i_stride in range(self.k):
                        for j_stride in range(self.k):
                            for t in range(self.old_dimension):
                                s += new_matrix[self.s * i + i_stride][self.s * j + j_stride][t] * self.a[k][t][i_stride][j_stride]
                    self.matrix[i][j][k] = s


class CNVM(CNV):
    def __init__(self, matrix, h, k, s, p, a, prev_node):
        super(CNVM, self).__init__(matrix, h, k, s, p, a, prev_node)

    def forward(self):
        n, d = self.prev_node.dimensions
        new_dimension = n + 2 * self.p
        new_matrix = get_array(new_dimension, d)
        old_indexes = []
        for i in range(new_dimension):
            old_indexes.append([0] * new_dimension)

        for i in range(new_dimension):
            for j in range(new_dimension):
                for k in range(d):
                    new_i = mirror_mapper(n, i - self.p)
                    new_j = mirror_mapper(n, j - self.p)
                    new_matrix[i][j][k] = self.prev_node.matrix[new_i][new_j][k]
                    old_indexes[i][j] = [new_i, new_j]

        self.new_matrix = new_matrix
        self.old_indexes = old_indexes
        self.matrix = get_array(*self.dimensions)

        n, d = self.dimensions
        # print(len(new_matrix), n, d)
        for k in range(d):
            for i in range(n):
                for j in range(n):
                    s = 0
                    for i_stride in range(self.k):
                        for j_stride in range(self.k):
                            for t in range(self.old_dimension):
                                # print(self.s * i + i_stride, self.s * j + j_stride, i, j, "HAI")
                                s += new_matrix[self.s * i + i_stride][self.s * j + j_stride][t] * self.a[k][t][i_stride][j_stride]
                    self.matrix[i][j][k] = s
        # print(self.matrix, "CNVM", self.matrix[0], 'qwe', self.matrix[1][1])


class CNVC(CNV):
    def __init__(self, matrix, h, k, s, p, a, prev_node):
        super(CNVC, self).__init__(matrix, h, k, s, p, a, prev_node)

    def forward(self):
        n, d = self.dimensions
        new_dimension = n + self.p * 2
        new_matrix = get_array(new_dimension, d)
        old_indexes = []
        for i in range(new_dimension):
            old_indexes.append([0] * new_dimension)

        for i in range(new_dimension):
            for j in range(new_dimension):
                for k in range(d):
                    new_i = cycle_mapper(n, i - self.p)
                    new_j = cycle_mapper(n, j - self.p)
                    new_matrix[i][j][k] = self.prev_node.matrix[new_i][new_j][k]
                    old_indexes[i][j] = [new_i, new_j]

        self.new_matrix = new_matrix
        self.old_indexes = old_indexes
        self.matrix = get_array(*self.dimensions)

        for k in range(d):
            for i in range(n):
                for j in range(n):
                    s = 0
                    for i_stride in range(self.k):
                        for j_stride in range(self.k):
                            for t in range(self.old_dimension):
                                s += new_matrix[self.s * i + i_stride][self.s * j + j_stride][t] * \
                                     self.a[k][t][i_stride][j_stride]
                    self.matrix[i][j][k] = s


def read_cnv(line, d):
    h, k, s, p = list(map(int, line[:4]))
    tmp = list(map(int, line[4:]))
    matrix = [[[[tmp[i * d * k * k + j * k * k + q * k + t] for t in range(k)] for q in range(k)] for j in range(d)] for i in range(h)]
    return matrix, h, k, s, p


def read_matrix(n):
    ans = []
    for i in range(n):
        line = list(map(int, input().rstrip().split()))
        ans.append(line)
    return ans


def print_matrix(matrix):
    for vec in matrix:
        print(*vec)
        # for item in vec:
        #     print("%.20f" % item, end=' ')
        # print()


def print_vector(vector):
    print(*vector)
    # for item in vector:
    #     print("%.20f" % item, end=' ')
    # print()


def main():
    line = input().split()
    n, d = int(line[0]), int(line[1])
    matrix = read_matrix_from_line(n, d, line[2:])

    L = int(input())
    net = [Node(matrix)]
    # print(net[-1].matrix)

    for i in range(L):
        line = input().split()
        operation_type = line[0]

        if operation_type == 'pool':
            net.append(Pool(matrix, int(line[1]), net[-1]))
        elif operation_type == 'relu':

            net.append(Relu(matrix, 1 / int(line[1]), net[-1]))
        elif operation_type == 'bias':
            net.append(Bias(matrix, list(map(int, line[1:])), net[-1]))
        else:
            cnv_matrix, h, k, s, p = read_cnv(line[1:], net[-1].dimensions[1])
            if operation_type == 'cnvm':
                # print(cnv_matrix, 'cnvm matrix')
                net.append(CNVM(matrix, h, k, s, p, cnv_matrix, net[-1]))
            elif operation_type == 'cnve':
                net.append(CNVE(matrix, h, k, s, p, cnv_matrix, net[-1]))
            else:
                net.append(CNVC(matrix, h, k, s, p, cnv_matrix, net[-1]))

    # line = input().split()
    # for node in net:
    #     print(node.dimensions)

    for node in net:
        node.forward()

    n, d = net[-1].dimensions
    line = input().split()
    # print(n, d)
    last_derivatives = read_matrix_from_line(n, d, line)
    net[-1].set_derivatives(last_derivatives)

    for node in reversed(net):
        node.backprop()

    net[-1].print_matrix()
    net[0].print_derivatives()

    for node in net:
        try:
            node.print_parameter_derivative()
        except NotImplementedError:
            continue


if __name__ == '__main__':
    main()

import math


def add_matrices(input_matrices):
    ans = []
    for i in range(len(input_matrices[0])):
        ans.append([0] * len(input_matrices[0][0]))

    for matrix in input_matrices:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                ans[i][j] += matrix[i][j]

    return ans


def multiply_matrices(first_matrix, second_matrix):
    ans = []
    for i in range(len(first_matrix)):
        ans.append([0] * len(second_matrix[0]))
    for i in range(len(ans)):
        for j in range(len(ans[i])):
            for k in range(len(first_matrix[0])):
                ans[i][j] += first_matrix[i][k] * second_matrix[k][j]

    return ans


def apply_rlu(a, matrix):
    ans = []
    for i in range(len(matrix)):
        ans.append([0] * len(matrix[0]))

    for i in range(len(ans)):
        for j in range(len(ans[i])):
            ans[i][j] = matrix[i][j] if matrix[i][j] >= 0 else a * matrix[i][j]
    return ans


def adamar_multiplication(input_matrices):
    ans = []
    for i in range(len(input_matrices[0])):
        ans.append([1] * len(input_matrices[0][0]))

    for matrix in input_matrices:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                ans[i][j] *= matrix[i][j]

    return ans


def tanh(matrix):
    ans = []
    for i in range(len(matrix)):
        ans.append([0.0] * len(matrix[i]))
    for i in range(len(ans)):
        for j in range(len(ans[i])):
            ans[i][j] = math.tanh(matrix[i][j])

    return ans


def calculate_derivative(vertex, matrix, derivative, ind, matrices):
    eps = 1e-9

    def _get_derivative(matrix_, derivative_, function):
        ans = []
        for i in range(len(matrix_)):
            ans.append([0.0] * len(matrix_[i]))
        for i in range(len(matrix_)):
            for j in range(len(matrix_[i])):
                ans[i][j] = function(matrix_[i][j]) * derivative_[i][j]

        return ans

    operation_type = vertex[0]
    if operation_type == 'rlu':
        alpha = 1.0 / vertex[1][0]
        return _get_derivative(
            matrix_=matrix,
            derivative_=derivative,
            function=lambda x: alpha if x < -eps else 1
        )
    elif operation_type == 'sum':
        return derivative
    elif operation_type == 'tnh':
        return _get_derivative(
            matrix_=matrix,
            derivative_=derivative,
            function=lambda x: 4 / (math.exp(x) + math.exp(-x)) / (math.exp(x) + math.exp(-x))
        )
    elif operation_type == 'had':
        vertex_to_deriviate = vertex[1]
        ans = []
        for i in range(len(derivative)):
            ans.append([q for q in derivative[i]])
        for i in range(len(ans)):
            for j in range(len(ans[i])):
                count_of_others = 0
                for k in vertex_to_deriviate:
                    if k != ind:
                        ans[i][j] *= matrices[k][i][j]
                        count_of_others += 1
                for k in range(len(vertex_to_deriviate) - (count_of_others + 1)):
                    ans[i][j] *= matrices[ind][i][j]

        return ans
    elif operation_type == 'mul':
        first_index = vertex[1][0]
        second_index = vertex[1][1]
        if ind == first_index:
            other_matrix = matrices[second_index]
        else:
            other_matrix = matrices[first_index]

        ans = []
        for i in range(len(matrix)):
            ans.append([0.0] * len(matrix[i]))
        if first_index == second_index:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    for k in range(len(other_matrix)):
                        if i == j == k:
                            continue
                        ans[i][j] += derivative[i][k] * other_matrix[j][k] + derivative[k][j] * other_matrix[k][i]
                ans[i][i] += 2 * matrix[i][i] * derivative[i][i]
            for i in range(len(ans)):
                ans[i] = list(map(lambda x: x / 2, ans[i]))
        else:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if ind == first_index:
                        other_matrix_vector = [q for q in other_matrix[j]]
                        other_derivative = [q for q in derivative[i]]
                    else:
                        other_matrix_vector = [other_matrix[k][i] for k in range(len(other_matrix))]
                        other_derivative = [derivative[k][j] for k in range(len(derivative))]
                    for k in range(len(other_matrix_vector)):
                        ans[i][j] += other_matrix_vector[k] * other_derivative[k]
        return ans


def add_matricies_component(a, b):
    ans = []
    for i in range(len(a)):
        ans.append([0] * len(a[i]))

    for i in range(len(a)):
        for j in range(len(a[i])):
            ans[i][j] = a[i][j] + b[i][j]

    return ans


def main():
    n, m, w = map(int, input().split())
    # print(n, m, k)
    computations_graph = []
    for i in range(n):
        line = input().split()
        operation_type = line[0]
        remainings = line[1:]
        if operation_type in ['sum', 'had']:
            remainings = list(map(lambda x: int(x) - 1, remainings[1:]))
        elif operation_type in ['mul', 'tnh']:
            remainings = list(map(lambda x: int(x) - 1, remainings))
        elif operation_type == 'rlu':
            remainings = list(map(int, remainings))
            remainings[-1] -= 1
        elif operation_type == 'var':
            remainings = list(map(int, remainings))

        computations_graph.append((
            operation_type,
            remainings
        ))
    matrices = []
    for i in range(m):
        rows = computations_graph[i][1][0]
        columns = computations_graph[i][1][1]
        matrix_input = []
        for j in range(rows):
            matrix_input.append([0] * columns)
        for j in range(rows):
            line = input().split()
            for k in range(columns):
                matrix_input[j][k] = int(line[k])
        matrices.append(matrix_input)
    # print(matrices, len(matrices), matrices[2], matrices[1])
    # for i in range(len(matrices)):
    #     print(matrices[i])
    # print(computations_graph)
    # print(multiply_matrices(matrices[0], matrices[1]))
    for i in range(m, n):
        vertex = computations_graph[i]
        operation_type = vertex[0]
        if operation_type == 'mul':
            a = matrices[vertex[1][0]]
            b = matrices[vertex[1][1]]
            matrices.append(
                multiply_matrices(
                    first_matrix=a,
                    second_matrix=b
                )
            )
        elif operation_type == 'sum':
            matrices_to_add = [matrices[vertex[1][i]] for i in range(len(vertex[1]))]
            matrices.append(
                add_matrices(matrices_to_add)
            )
        elif operation_type == 'rlu':
            alpha = 1.0 / vertex[1][0]
            matrices.append(
                apply_rlu(alpha, matrices[vertex[1][1]])
            )
        elif operation_type == 'tnh':
            matrices.append(
                tanh(matrices[vertex[1][0]])
            )
        elif operation_type == 'had':
            matrices_to_had = [matrices[vertex[1][i]] for i in range(len(vertex[1]))]
            matrices.append(
                adamar_multiplication(matrices_to_had)
            )

    # for i in range(len(matrices)):
    #     print(matrices[i])

    derivatives = []
    for i in range(n):
        new_der = []
        for j in range(len(matrices[i])):
            new_der.append([0] * len(matrices[i][0]))
        derivatives.append(new_der)
    for i in range(n - w, n):
        derivative_input = []
        for j in range(len(matrices[i])):
            derivative_input.append([0] * len(matrices[i][j]))
        # print(derivatives_input)
        for j in range(len(matrices[i])):
            line = input().split()
            for k in range(len(line)):
                derivative_input[j][k] = int(line[k])
        derivatives[i] = derivative_input
    # for i in range(len(derivatives)):
    #     print(derivatives[i])
    #
    # print('qwe')
    # for i in range(len(matrices)):
    #     print(matrices[i])

    for i in range(n - 1, m - 1, -1):
        vertex = computations_graph[i]
        vertexes_to_deriviate = vertex[1] if vertex[0] != 'rlu' else vertex[1][1:]
        for ind in vertexes_to_deriviate:
            derivative = derivatives[i]
            # print( derivative)
            new_derivative = calculate_derivative(
                vertex,
                matrices[ind],
                derivative,
                ind,
                matrices
            )
            derivatives[ind] = add_matricies_component(derivatives[ind], new_derivative)

    for i in range(n - w, n):
        for j in range(len(matrices[i])):
            print(*matrices[i][j])

    # print(len(derivatives), "qweqwe")
    for i in range(m):
        for j in range(len(derivatives[i])):
            print(*derivatives[i][j])




if __name__ == '__main__':
    main()

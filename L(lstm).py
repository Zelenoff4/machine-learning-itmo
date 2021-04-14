import math


def sigmoid_function(x):
    return 1 / (1 + math.exp(-x))


def add_matricies_component(a, b):
    ans = []
    for i in range(len(a)):
        ans.append([0] * len(a[i]))

    for i in range(len(a)):
        for j in range(len(a[i])):
            ans[i][j] = a[i][j] + b[i][j]

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


def matrix_times_vector(matrix, vector):
    ans = [0.0] * len(vector)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            ans[i] += matrix[i][j] * vector[j]

    # print(ans, "UTOCHKA")
    return ans


def vector_times_vector(v1, v2):
    return [x * y for x, y in zip(v1, v2)]


def vector_times_transposed_vector(v1, v2):
    ans = []
    for i in range(len(v1)):
        ans.append([0] * len(v1))

    for i in range(len(v1)):
        for j in range(len(v1)):
            ans[i][j] = v1[i] * v2[j]

    return ans


def vector_plus_vector(v1, v2):
    return [x + y for x, y in zip(v1, v2)]


def calculate_formula(w, x, u, h, b):
    return vector_plus_vector(
        vector_plus_vector(
            matrix_times_vector(w, x),
            matrix_times_vector(u, h)
        ),
        b
    )


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


def transpose_matrix(matrix):
    return [list(i) for i in zip(*matrix)]


def main():
    n = int(input())
    wf = read_matrix(n)
    uf = read_matrix(n)
    bf = list(map(int, input().rstrip().split()))
    wi = read_matrix(n)
    ui = read_matrix(n)
    bi = list(map(int, input().rstrip().split()))
    wo = read_matrix(n)
    uo = read_matrix(n)
    bo = list(map(int, input().rstrip().split()))
    wc = read_matrix(n)
    uc = read_matrix(n)
    bc = list(map(int, input().rstrip().split()))

    # vectors = [wf, uf, bf, wi, ui, bi, wo, uo, bo, wc, uc, bc]
    # print(len(vectors))
    # for i in range(len(vectors)):
    #     for j in range(n):
    #         line = list(map(int, input().rstrip().split()))
    #         vectors[i].append(line)
    # # for i in vectors:
    # #     print(i)

    m = int(input())
    h0 = list(map(int, input().split()))
    c0 = list(map(int, input().split()))
    # print(m, h0, c0)
    xs = []
    for i in range(m):
        xs.append(list(map(int, input().split())))

    dh = list(map(int, input().split()))
    dc = list(map(int, input().split()))

    # print(dh, dc)
    h = [h0]
    f = []
    I = []
    o = []
    c = [c0]
    tanhs = []

    # print()
    # print(xs)
    # print(wf, uf, sep=' qwe ')
    # print(wi, ui, sep=' asd ')
    # print(wo, uo, sep=' zxc ')
    # print(wc, uc, sep=' rfv ')
    # print(h)
    # print(bo)
    for i in range(m):
        f.append(
            list(map(sigmoid_function, calculate_formula(wf, xs[i], uf, h[i], bf)))
        )
        I.append(
            list(map(sigmoid_function, calculate_formula(wi, xs[i], ui, h[i], bi)))
        )
        o.append(
            list(map(sigmoid_function, calculate_formula(wo, xs[i], uo, h[i], bo)))
        )
        tanhs.append(
            list(map(math.tanh, calculate_formula(wc, xs[i], uc, h[i], bc)))
        )
        c.append(
            vector_plus_vector(
                vector_times_vector(f[i], c[i]),
                vector_times_vector(I[i], tanhs[i])
            )
        )
        h.append(
            vector_times_vector(
                o[i],
                # list(map(math.tanh, c[i + 1]))
                c[i + 1]
            )
        )
    # print('h', h)
    # print('c', c)
    # print(f)
    # print(I)
    # print(o)
    print_matrix(o)
    # print(tanhs)
    # print('h[m] below')
    print_vector(h[m])
    # print('c[m] below')
    print_vector(c[m])

    dwf = []
    duf = []
    dwi = []
    dui = []
    dwo = []
    duo = []
    dwc = []
    duc = []
    for i in range(n):
        dwf.append([0.0] * n)
        duf.append([0.0] * n)
        dwi.append([0.0] * n)
        dui.append([0.0] * n)
        dwo.append([0.0] * n)
        duo.append([0.0] * n)
        dwc.append([0.0] * n)
        duc.append([0.0] * n)
    dbf = [0.0] * n
    dbi = [0.0] * n
    dbo = [0.0] * n
    dbc = [0.0] * n

    for i in range(m - 1, -1, -1):
        # do = list(map(int, input().split()))
        do = vector_plus_vector(
            vector_times_vector(
                dh,
                # list(map(math.tanh, c[i + 1]))
                c[i + 1]
            ),
            # do
            list(map(int, input().split()))
        )
        dct = vector_plus_vector(
            dc,
            vector_times_vector(dh, o[i])
        )
        dF = vector_times_vector(
            c[i],
            dct
        )
        dTanh = vector_times_vector(
            I[i],
            dct
        )
        dI = vector_times_vector(
            tanhs[i],
            dct
        )

        dF = vector_times_vector(
            dF,
            list(map(lambda x: x * (1 - x), f[i]))
        )
        # print(dF)
        dTanh = vector_times_vector(
            dTanh,
            list(map(lambda x: 1 - x ** 2, tanhs[i]))
        )
        # print(dTanh)
        dI = vector_times_vector(
            dI,
            list(map(lambda x: x * (1 - x), I[i]))
        )
        # print(dI)
        do = vector_times_vector(
            do,
            list(map(lambda x: x * (1 - x), o[i]))
        )
        # print(do)

        dwc = add_matricies_component(
            dwc,
            vector_times_transposed_vector(dTanh, xs[i])
        )
        dwf = add_matricies_component(
            dwf,
            vector_times_transposed_vector(dF, xs[i])
        )
        dwi = add_matricies_component(
            dwi,
            vector_times_transposed_vector(dI, xs[i])
        )
        dwo = add_matricies_component(
            dwo,
            vector_times_transposed_vector(do, xs[i])
        )

        duc = add_matricies_component(
            duc,
            vector_times_transposed_vector(dTanh, h[i])
        )
        duf = add_matricies_component(
            duf,
            vector_times_transposed_vector(dF, h[i])
        )
        dui = add_matricies_component(
            dui,
            vector_times_transposed_vector(dI, h[i])
        )
        duo = add_matricies_component(
            duo,
            vector_times_transposed_vector(do, h[i])
        )

        dbc = vector_plus_vector(dbc, dTanh)
        dbf = vector_plus_vector(dbf, dF)
        dbi = vector_plus_vector(dbi, dI)
        dbo = vector_plus_vector(dbo, do)

        dx = vector_plus_vector(
            matrix_times_vector(transpose_matrix(wc), dTanh),
            vector_plus_vector(
                matrix_times_vector(transpose_matrix(wf), dF),
                vector_plus_vector(
                    matrix_times_vector(transpose_matrix(wi), dI),
                    matrix_times_vector(transpose_matrix(wo), do)
                )
            )
        )

        print_vector(dx)

        dh = vector_plus_vector(
            matrix_times_vector(transpose_matrix(uc), dTanh),
            vector_plus_vector(
                matrix_times_vector(transpose_matrix(uf), dF),
                vector_plus_vector(
                    matrix_times_vector(transpose_matrix(ui), dI),
                    matrix_times_vector(transpose_matrix(uo), do)
                )
            )
        )
        dc = vector_times_vector(dct, f[i])

    print_vector(dh)
    print_vector(dc)

    print_matrix(dwf)
    print_matrix(duf)
    print_vector(dbf)

    print_matrix(dwi)
    print_matrix(dui)
    print_vector(dbi)

    print_matrix(dwo)
    print_matrix(duo)
    print_vector(dbo)

    print_matrix(dwc)
    print_matrix(duc)
    print_vector(dbc)


if __name__ == '__main__':
    main()

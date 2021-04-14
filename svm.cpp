#include <cstdio>
#include <vector>
#include <cmath>
#include <iostream>

double
getA(const std::vector<double> &l, const std::vector<std::vector<double> > &k, const std::vector<double> &y, size_t a,
        size_t b, int mode) {
    return mode * k[a][b] * y[a] * y[b] +
            0.5 * k[a][a] * y[a] * y[a] +
            0.5 * k[b][b] * y[b] * y[b];
}

double
getB(const std::vector<double> &l, const std::vector<std::vector<double> > &k, const std::vector<double> &y, size_t a,
        size_t b, int mode) {
    double ans = 0;
    if (mode > 0) {
        ans = -2;
    }
    for (size_t i = 0; i < l.size(); i++) {
        ans += l[i] * y[i] * k[a][i] * y[a];
        ans += l[i] * mode * k[b][i] * y[b] * y[i];
    }

    return ans;
}

double getC(const std::vector<double> &l, const std::vector<std::vector<double> > &k, const std::vector<double> &y) {
    double ans = 0.0;

    for (size_t i = 0; i < l.size(); i++) {
        for (size_t j = 0; j < l.size(); j++) {
            ans += 0.5 * l[i] * l[j] * y[i] * y[j] * k[i][j];
        }
        ans -= l[i];
    }

    return ans;
}

double eps = 1e-9;

double
calculateB(const std::vector<double> &l, const std::vector<std::vector<double> > &k, const std::vector<double> &y) {
    double cc = 0.0;

    size_t i = l.size() - 1;
    for (; i >= 0; i--) {
        if (l[i] != 0) {
            cc = y[i];
            break;
        }
    }
    double w = 0;
    for (size_t j = 0; j < l.size(); j++) {
        w += k[j][i] * y[j] * l[j];
    }

    return cc - w;
}

int main() {
    int n = 0;
    scanf("%d", &n);

    std::vector<std::vector<double> > k(n);
    std::vector<double> y(n);

    for (size_t i = 0; i < n; i++) {
        int tmp = 0;
        k[i].resize(n);
        for (size_t j = 0; j < n; j++) {
            scanf("%d", &tmp);
            k[i][j] = tmp;
        }
        scanf("%d", &tmp);
        y[i] = tmp;
    }

    int cc = 0;
    scanf("%d", &cc);

    std::vector<double> l(n);

    for (size_t qq = 0; qq < 700; qq++) {
        for (size_t i = 0; i < n; i++) {
            for (size_t j = i + 1; j < n; j++) {
                if (y[i] != y[j]) {
                    double a = getA(l, k, y, i, j, 1);
                    std::cout << a << " diff classes" << std::endl;
                    if (std::fabs(a) < eps) {
                        continue;
                    }
                    double b = getB(l, k, y, i, j, 1);

                    double middle = -b / (2.0 * a);
                    double left = std::max(-l[i], -l[j]);
                    double right = std::min(cc - l[i], cc - l[j]);
                    if (a > 0) {
                        if (middle < left) {
                            l[i] += left;
                            l[j] += left;
                        } else if (middle > right) {
                            l[i] += right;
                            l[j] += right;
                        } else {
                            l[i] += middle;
                            l[j] += middle;
                        }
                    } else {
                        double leftToMiddle = std::fabs(middle - left);
                        double rightToMiddle = std::fabs(middle - right);
                        if (middle < left) {
                            l[i] += right;
                            l[j] += right;
                        } else if (middle > right) {
                            l[i] += left;
                            l[j] += left;
                        } else if (leftToMiddle > rightToMiddle) {
                            l[i] += left;
                            l[j] += left;
                        } else {
                            l[i] += right;
                            l[j] += right;
                        }
                    }
                } else {
                    double a2 = getA(l, k, y, i, j, -1);
                    std::cout << a2 << " same classes" << std::endl;
                    if (std::fabs(a2) < eps) {
                        continue;
                    }
                    double b2 = getB(l, k, y, i, j, -1);
                    double middle2 = -b2 / (2.0 * a2);

                    double left2 = std::max(-l[i], l[j] - cc);
                    double right2 = std::min(cc - l[i], l[j]);
                    if (a2 > 0) {
                        if (middle2 < left2) {
                            l[i] += left2;
                            l[j] -= left2;
                        } else if (middle2 > right2) {
                            l[i] += right2;
                            l[j] -= right2;
                        } else {
                            l[i] += middle2;
                            l[j] -= middle2;
                        }
                    } else {
                        double leftToMiddle = std::fabs(middle2 - left2);
                        double rightToMiddle = std::fabs(middle2 - right2);
                        if (middle2 < left2) {
                            l[i] += right2;
                            l[j] -= right2;
                        } else if (middle2 > right2) {
                            l[i] += left2;
                            l[j] -= left2;
                        } else if (leftToMiddle > rightToMiddle) {
                            l[i] += left2;
                            l[j] -= left2;
                        } else {
                            l[i] += right2;
                            l[j] -= right2;
                        }
                    }
                }
            }
        }
    }

    for (size_t i = 0; i < n; i++) {
        printf("%.12g\n", l[i]);
    }
    printf("%.12g\n", calculateB(l, k, y));
    return 0;
}
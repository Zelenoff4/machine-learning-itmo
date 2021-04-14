#include <cstdio>
#include <iostream>
#include <vector>
#include <cstring>
#include <memory>
#include <algorithm>
#include <cstdlib>

const double eps = 1e-10;

struct Layer {
    Layer() = default;

    Layer(std::shared_ptr<Layer> previousLayer)
            : m_previousLayer(previousLayer) {
    }

    virtual void generateNewLayer() = 0;

    virtual void generateDerivative() = 0;

    std::vector<std::vector<std::vector<double>>> &getNewLayerMatrix() {
        return m_newLayer;
    }

    void printOut() {
        print(m_newLayer);
    }

    void printDerivative() {
        print(m_derivative);
    }

    void printDerivativeParameters() {
        for (double m_derivativeParameter : m_derivativeParameters) {
            std::cout << m_derivativeParameter << " ";
        }
        std::cout << "\n";
    }

    void printInputLayer() {
        print(m_inputLayer);
    }


    std::shared_ptr<Layer> m_previousLayer;
    std::vector<std::vector<std::vector<double>>> m_newLayer;
    std::vector<std::vector<std::vector<double>>> m_derivative;
    std::vector<double> m_derivativeParameters;
    std::vector<std::vector<std::vector<double>>> m_inputLayer;

private:
    void print(std::vector<std::vector<std::vector<double>>> &m) {
        for (auto &d : m) {
            for (auto &i : d) {
                for (double j : i) {
                    std::cout << j << " ";
                }
            }
        }
        std::cout << "\n";
    }
};

struct CNV : public Layer {
    enum class Border {
        Mirror,
        Extension,
        Cycle
    };

    CNV(std::shared_ptr<Layer> previousLayer,
        std::vector<std::vector<std::vector<std::vector<double>>>> filters,
        Border borderStyle,
        int borderSize,
        int step = 1)
            : Layer(previousLayer), m_filters(filters), m_borderStyle(borderStyle), m_borderSize(borderSize),
              m_step(step) {
    }

    void generateNewLayer() override {
        m_newLayer.resize(m_filters.size());
        m_inputLayer.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_inputLayer.size(); d++) {
            m_inputLayer[d].resize(m_previousLayer->m_newLayer[d].size() + 2 * m_borderSize);
            for (int i = 0; i < m_inputLayer[d].size(); i++) {
                m_inputLayer[d][i].resize(m_previousLayer->m_newLayer[d].size() + 2 * m_borderSize);
            }
        }
        for (int filter = 0; filter < m_filters.size(); filter++) {
            m_newLayer[filter].resize(
                    (m_previousLayer->m_newLayer[0].size() + 2 * m_borderSize - m_filters[0][0].size()) / m_step + 1);
            int newI = 0;
            int newJ = 0;
            int _ii = -m_borderSize;
            int _ii1 = (m_previousLayer->m_newLayer[0].size() + m_borderSize);
            for (int ii = -m_borderSize;
                 ii < (int) (m_previousLayer->m_newLayer[0].size() + m_borderSize - m_filters[0][0].size() +
                             1); ii += m_step) {
                m_newLayer[filter][newI].resize(
                        (m_previousLayer->m_newLayer[0][0].size() + 2 * m_borderSize - m_filters[0][0][0].size()) /
                        m_step + 1);
                newJ = 0;
                for (int jj = -m_borderSize;
                     jj < (int) (m_previousLayer->m_newLayer[0][0].size() + m_borderSize - m_filters[0][0][0].size() +
                                 1); jj += m_step) {
                    double tmp = 0;
                    for (int depth = 0; depth < m_filters[filter].size(); depth++) {
                        for (int i = 0; i < m_filters[filter][depth].size(); i++) {
                            for (int j = 0; j < m_filters[filter][depth][i].size(); j++) {
                                std::pair<int, int> newIndexes = getIndex(ii + i, jj + j,
                                                                          m_previousLayer->m_newLayer[0].size(),
                                                                          m_previousLayer->m_newLayer[0][0].size());
                                tmp += m_filters[filter][depth][i][j] *
                                       m_previousLayer->m_newLayer[depth][newIndexes.first][newIndexes.second];
                                m_inputLayer[depth][ii + i + m_borderSize][jj + j + m_borderSize] = m_previousLayer->m_newLayer[depth][newIndexes.first][newIndexes.second];
                            }
                        }
                    }
                    m_newLayer[filter][newI][newJ] = tmp;
                    newJ++;
                }
                newI++;
            }
        }
    }

    void generateDerivative() override {
        m_derivativeParameters.resize(
                m_filters.size() * m_filters[0].size() * m_filters[0][0].size() * m_filters[0][0][0].size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            std::vector<std::vector<double>> matrix(m_previousLayer->m_newLayer[0].size());
            for (auto &qq : matrix) {
                qq.resize(m_previousLayer->m_newLayer[0][0].size());
            }
            int newI = 0;
            int newJ = 0;
            for (int ii = -m_borderSize;
                 ii < (int) (m_previousLayer->m_newLayer[0].size() + m_borderSize - m_filters[0][0].size() +
                             1); ii += m_step) {
                newJ = 0;
                for (int jj = -m_borderSize;
                     jj < (int) (m_previousLayer->m_newLayer[0][0].size() + m_borderSize - m_filters[0][0].size() +
                                 1); jj += m_step) {
                    double tmp = 0;
                    for (int i = 0; i < m_filters[0][0].size(); i++) {
                        for (int j = 0; j < m_filters[0][0][i].size(); j++) {
                            for (int depth = 0; depth < m_filters.size(); depth++) {
                                std::pair<int, int> newIndexes = getIndex(ii + i, jj + j,
                                                                          m_previousLayer->m_newLayer[0].size(),
                                                                          m_previousLayer->m_newLayer[0][0].size());
                                matrix[newIndexes.first][newIndexes.second] +=
                                        m_derivative[depth][newI][newJ] * m_filters[depth][d][i][j];
                                int newIndex = depth * m_filters[depth].size() * m_filters[0][0].size() *
                                               m_filters[0][0][0].size() +
                                               d * m_filters[0][0].size() * m_filters[0][0][0].size() +
                                               i * m_filters[0][0][0].size() + j;
                                m_derivativeParameters[newIndex] += m_derivative[depth][newI][newJ] *
                                                                    m_previousLayer->m_newLayer[d][newIndexes.first][newIndexes.second];
                            }
                        }
                    }
                    newJ++;
                }
                newI++;
            }
            m_previousLayer->m_derivative.push_back(matrix);
        }
    }

private:
    std::pair<int, int> getIndex(int i, int j, int n, int m) {
        int newI = i, newJ = j;
        switch (m_borderStyle) {
            case Border::Mirror:
                if (newI < 0) {
                    newI = -newI;
                } else if (newI >= n) {
                    newI = n + (n - newI) - 2;
                }

                if (newJ < 0) {
                    newJ = -newJ;
                } else if (newJ >= m) {
                    newJ = m + (m - newJ) - 2;
                }
                break;
            case Border::Extension:
                if (newI < 0) {
                    newI = 0;
                } else if (newI >= n) {
                    newI = n - 1;
                }

                if (newJ < 0) {
                    newJ = 0;
                } else if (newJ >= m) {
                    newJ = m - 1;
                }
                break;
            case Border::Cycle:
                if (newI < 0) {
                    newI = n + newI;
                } else if (newI >= n) {
                    newI = newI - n;
                }

                if (newJ < 0) {
                    newJ = m + newJ;
                } else if (newJ >= m) {
                    newJ = newJ - m;
                }
                break;
        }
        if (newI >= 0 && newI < n && newJ >= 0 && newJ < m) {
            return std::make_pair(newI, newJ);
        } else {
            return getIndex(newI, newJ, n, m);
        }

    }

    Border m_borderStyle;
    int m_borderSize;
    int m_step;
    std::vector<std::vector<std::vector<std::vector<double>>>> m_filters;

};

struct Bias : public Layer {
    Bias(std::shared_ptr<Layer> previousLayer,
         std::vector<int> b)
            : Layer(previousLayer), m_b(b) {
    }

    void generateNewLayer() override {
        m_newLayer.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            m_newLayer[d].resize(m_previousLayer->m_newLayer[d].size());
            for (int i = 0; i < m_previousLayer->m_newLayer[d].size(); i++) {
                m_newLayer[d][i].resize(m_previousLayer->m_newLayer[d][i].size());
                for (int j = 0; j < m_previousLayer->m_newLayer[d][i].size(); j++) {
                    m_newLayer[d][i][j] = m_previousLayer->m_newLayer[d][i][j] + m_b[d];
                }
            }
        }
    }

    void generateDerivative() override {
        m_previousLayer->m_derivative = m_derivative;
        m_derivativeParameters.resize(m_b.size());
        for (int d = 0; d < m_derivative.size(); d++) {
            double tmp = 0.0;
            for (int i = 0; i < m_derivative[d].size(); i++) {
                for (int j = 0; j < m_derivative[d][i].size(); j++) {
                    tmp += m_derivative[d][i][j];
                }
            }
            m_derivativeParameters[d] = tmp;
        }
    }

private:
    std::vector<int> m_b;
};

struct InitialLayer : public Layer {
    InitialLayer(std::vector<std::vector<std::vector<double>>> previousLayer)
            : Layer() {
        m_newLayer = previousLayer;
    }

    void generateNewLayer() override {
    }

    void generateDerivative() override {
    }

};


struct Relu : public Layer {
    Relu(std::shared_ptr<Layer> previousLayer, double alpha)
            : Layer(previousLayer), m_alpha(alpha) {
    }

    void generateNewLayer() override {
        m_newLayer.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            m_newLayer[d].resize(m_previousLayer->m_newLayer[d].size());
            for (int i = 0; i < m_previousLayer->m_newLayer[d].size(); i++) {
                m_newLayer[d][i].resize(m_previousLayer->m_newLayer[d][i].size());
                for (int j = 0; j < m_previousLayer->m_newLayer[d][i].size(); j++) {
                    m_newLayer[d][i][j] = std::max(m_previousLayer->m_newLayer[d][i][j],
                                                   m_previousLayer->m_newLayer[d][i][j] * m_alpha);
                }
            }
        }
    }

    void generateDerivative() override {
        m_previousLayer->m_derivative.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            m_previousLayer->m_derivative[d].resize(m_previousLayer->m_newLayer[d].size());
            for (int i = 0; i < m_previousLayer->m_newLayer[d].size(); i++) {
                m_previousLayer->m_derivative[d][i].resize(m_previousLayer->m_newLayer[d][i].size());
                for (int j = 0; j < m_previousLayer->m_newLayer[d][i].size(); j++) {
                    m_previousLayer->m_derivative[d][i][j] =
                            (m_previousLayer->m_newLayer[d][i][j] < 0 ? m_alpha : 1.0) * m_derivative[d][i][j];
                }
            }
        }
    }

private:
    double m_alpha;
};

struct Pool : public Layer {
    Pool(std::shared_ptr<Layer> previousLayer, int s)
            : Layer(previousLayer), m_size(s) {
    }

    void generateNewLayer() override {
        m_newLayer.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            m_newLayer[d].resize(m_previousLayer->m_newLayer[d].size() / m_size);
            for (int i = 0; i < m_previousLayer->m_newLayer[d].size() / m_size; i++) {
                m_newLayer[d][i].resize(m_previousLayer->m_newLayer[d][0].size() / m_size);
                for (int j = 0; j < m_previousLayer->m_newLayer[d][0].size() / m_size; j++) {
                    double maxValue = m_previousLayer->m_newLayer[d][i * m_size][j * m_size];
                    for (int ii = 0; ii < m_size; ii++) {
                        for (int jj = 0; jj < m_size; jj++) {
                            maxValue = std::max(m_previousLayer->m_newLayer[d][i * m_size + ii][j * m_size + jj], maxValue);
                        }
                    }
                    m_newLayer[d][i][j] = maxValue;
                }
            }
        }
    }

    void generateDerivative() override {
        m_previousLayer->m_derivative.resize(m_previousLayer->m_newLayer.size());
        for (int d = 0; d < m_previousLayer->m_newLayer.size(); d++) {
            m_previousLayer->m_derivative[d].resize(m_previousLayer->m_newLayer[d].size());
            for (int i = 0; i < m_previousLayer->m_newLayer[d].size(); i++) {
                m_previousLayer->m_derivative[d][i].resize(m_previousLayer->m_newLayer[d][i].size());
                for (int j = 0; j < m_previousLayer->m_newLayer[d][i].size(); j++) {
                    m_previousLayer->m_derivative[d][i][j] =
                            abs(m_previousLayer->m_newLayer[d][i][j] - m_newLayer[d][i / m_size][j / m_size]) < eps
                            ? m_derivative[d][i / m_size][j / m_size] : 0;
                }
            }
        }
    }

private:
    int m_size;
};

int main() {
    std::vector<std::vector<std::vector<double>>> inputMatrix;

    int d, n;

    scanf("%d", &n);
    scanf("%d", &d);

    inputMatrix.resize(d);
    for (int depth = 0; depth < d; depth++) {
        inputMatrix[depth].resize(n);
        for (int i = 0; i < n; i++) {
            inputMatrix[depth][i].resize(n);
            for (int j = 0; j < n; j++) {
                int tmp;
                scanf("%d", &tmp);
                inputMatrix[depth][i][j] = tmp;
            }
        }
    }

    int operationsCount = 0;
    scanf("%d", &operationsCount);

    std::vector<std::shared_ptr<Layer>> layers;
    std::shared_ptr<Layer> initialLayer;
    initialLayer.reset(new InitialLayer(inputMatrix));
    initialLayer->generateNewLayer();
    layers.push_back(initialLayer);

    for (int op = 0; op < operationsCount; op++) {
        char operation[10];
        scanf("%s", operation);
        std::shared_ptr<Layer> newLayer;
        if (strncmp("cnv", operation, 3) == 0) {
            int h, k, s, p;
            scanf("%d", &h);
            scanf("%d", &k);
            scanf("%d", &s);
            scanf("%d", &p);
            std::vector<std::vector<std::vector<std::vector<double>>>> a;
            a.resize(h);
            for (int hh = 0; hh < h; hh++) {
                a[hh].resize(layers.back()->m_newLayer.size());
                for (int dd = 0; dd < layers.back()->m_newLayer.size(); dd++) {
                    a[hh][dd].resize(k);
                    for (int i = 0; i < k; i++) {
                        a[hh][dd][i].resize(k);
                        for (int j = 0; j < k; j++) {
                            int tmp;
                            scanf("%d", &tmp);
                            a[hh][dd][i][j] = tmp;
                        }
                    }
                }
            }
            CNV::Border border;
            if (operation[3] == 'm') {
                border = CNV::Border::Mirror;
            } else if (operation[3] == 'e') {
                border = CNV::Border::Extension;
            } else if (operation[3] == 'c') {
                border = CNV::Border::Cycle;
            }
            newLayer.reset(new CNV(layers[layers.size() - 1], a, border, p, s));
        } else if (strcmp("bias", operation) == 0) {
            std::vector<int> b(layers.back()->m_newLayer.size());
            for (int i = 0; i < layers.back()->m_newLayer.size(); i++) {
                int tmp;
                scanf("%d", &tmp);
                b[i] = tmp;
            }
            newLayer.reset(new Bias(layers[layers.size() - 1], b));
        } else if (strcmp("relu", operation) == 0) {
            int alpha = 0;
            scanf("%d", &alpha);
            newLayer.reset(new Relu(layers[layers.size() - 1], 1.0 / static_cast<double>(alpha)));
        } else if (strcmp("pool", operation) == 0) {
            int s = 0;
            scanf("%d", &s);
            newLayer.reset(new Pool(layers[layers.size() - 1], s));
        }
        newLayer->generateNewLayer();
        //newLayer->printInputLayer();
        //newLayer->printOut();
        layers.push_back(newLayer);
    }
    std::vector<std::vector<std::vector<double>>> derivativeOut;
    derivativeOut.resize(layers.back()->m_newLayer.size());
    for (int d = 0; d < layers.back()->m_newLayer.size(); d++) {
        derivativeOut[d].resize(layers.back()->m_newLayer[d].size());
        for (int i = 0; i < layers.back()->m_newLayer[d].size(); i++) {
            derivativeOut[d][i].resize(layers.back()->m_newLayer[d][i].size());
            for (int j = 0; j < layers.back()->m_newLayer[d][i].size(); j++) {
                int tmp;
                scanf("%d", &tmp);
                derivativeOut[d][i][j] = tmp;
            }
        }
    }
    layers.back()->m_derivative = derivativeOut;
    layers.back()->printOut();
    for (int i = layers.size() - 1; i > 0; i--) {
        layers[i]->generateDerivative();
    }
    layers.front()->printDerivative();
    for (int i = 0; i < layers.size(); i++) {
        auto pointerCNV = std::dynamic_pointer_cast<CNV>(layers[i]);
        if (pointerCNV) {
            pointerCNV->printDerivativeParameters();
        } else {
            auto pointerBias = std::dynamic_pointer_cast<Bias>(layers[i]);
            if (pointerBias) {
                pointerBias->printDerivativeParameters();
            }
        }
    }
    return 0;
}
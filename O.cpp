#include <iostream>
#include <vector>
#include <map>
#include <algorithm>

using namespace std;


int dist(vector<int> a){
    sort(a.begin(), a.end());
    int cur_sum = 0, ans = 0;
    for (int i = 0; i < a.size(); i++){
        cur_sum += a[i];
        ans += a[i] * (i + 1) - cur_sum;
    }
    return 2 * ans;
}


int main() {
    int k, n;
    cin >> k;
    cin >> n;
    vector<int> xs, ys;
    map< int, vector<int> > clusters;
    for (int i = 0; i < n; i++){
        int x, y;
        cin >> x >> y;
        xs.push_back(x);
        ys.push_back(y);
    }
    int all_distance = dist(xs);
    for (int i = 0; i < n; i++){
        clusters[ys[i]].push_back(xs[i]);
    }
    int inner_distance = 0;
    for (auto i: clusters){
        inner_distance += dist(i.second);
    }
    cout << inner_distance << endl;
    cout << all_distance - inner_distance << endl;
    return 0;

}

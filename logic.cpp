#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

#define fi first
#define se second
#define pb push_back
//#define FILE

#define taskname ""
#define taski taskname".in"
#define tasko taskname".out"

typedef long long ll;
typedef unsigned int uint;

int main()
{
	ios:: sync_with_stdio(false);
	#ifdef HOME
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
	#elif defined(FILE)
	freopen(taski, "r", stdin);
	freopen(tasko, "w", stdout);
	#endif

	int C = 10000;
	int n;
	cin >> n;
	vector<int> res(1 << n);
	for(int i = 0; i < (1 << n); i++)
		cin >> res[i];
	vector<vector<vector<double> > > ans;
	ans.resize(2);
	ans[0].resize(1 << n);
	ans[1].resize(1);
	for(int i = 0; i < (1 << n); i++)
		ans[0][i].resize(n + 1);
	ans[1][0].resize((1 << n) + 1);
	ans[1][0][1 << n] = -0.5;
	for(int i = 0; i < (1 << n); i++) {
		if(res[i] == 1) {
			ans[0][i][n] = 0.5;
			ans[1][0][i] = 1;
			for(int j = 0; j < n; j++) {
				if((i >> j)&1) {
					ans[0][i][j] += C;
					ans[0][i][n] -= C;
				} else {
					ans[0][i][j] -= C;
				}
			}
		} else {
			ans[0][i][n] = -0.5;
		}
	}
	cout << 2 << "\n";
	cout << (1 << n) << " " << 1 << "\n";
	for(int i = 0; i < 2; i++)
		for(int j = 0; j < ans[i].size(); j++) {
			for(int k = 0; k < ans[i][j].size(); k++)
				cout << fixed << setprecision(1) << ans[i][j][k] << " ";
			cout << "\n";
		}
	return 0;
}
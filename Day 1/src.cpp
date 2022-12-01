#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
    vector<int> cals;
    cals.push_back(0);
    
    int calories = 0;
    while (cin >> calories)
    {
        if (calories == -1)
            cals.push_back(0);
        else cals[cals.size() - 1] += calories;
    }

    sort(cals.begin(), cals.end());

    // Part 1
    cout << cals[cals.size() - 1] << endl;

    // Part 2
    cout << cals[cals.size() - 1] + cals[cals.size() - 2] + cals[cals.size() - 3] << endl;
}
#include<bits/stdc++.h>
using namespace std;

const int DIM = 8;

string s[DIM][DIM];
char me;

bool readFile()
{
    ifstream in;
    in.open("shared_file.txt");

    char now;
    in >> now;

    if (now!=me) return false;

    for (int i = 0; i < DIM; i++) {
        for (int j = 0; j < DIM; j++) {
            in >> s[i][j];
        }
    }

    in.close();

    return true;
}

void makeMove(int x, int y)
{
    ofstream out;
    out.open("shared_file.txt");
    out << 0 << "\n";
    out << x << " " << y << "\n";
    out.close();
}

int main(int argc, char *argv[])
{


    me = argv[1][0];
    cout << "started as " << me << endl;
    while (true) {
        if (readFile()==false) continue;
        int x, y;
        cin>>x>>y;
        makeMove(x, y);
    }
    return 0;
}

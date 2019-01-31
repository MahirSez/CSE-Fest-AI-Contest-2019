#include<bits/stdc++.h>
#define read freopen("in.txt","r",stdin)
#define write freopen("out.txt","w",stdout)
#define N 8
#define pii pair<int,int>
#define uu first
#define vv second
#define INF 1e8
#define ll long long int
using namespace std;


int critVal[10][10] ;

///1st will store player ID
///2nd will store number of orbs
///MY ID IS ALWAYS 2


int dx[] = {1 , -1 , 0 , 0 };
int dy[] = {0 , 0 , -1 , 1 };

int cornerX[] = { 0 , 0 , N-1 , N-1};
int cornerY[] = {0 , N-1 , 0 , N-1};

bool winGame(vector<vector<pii>>board ,int turn) {

    for(int i =0 ; i <N ; i++ ) {
        for(int j =0 ; j <N ; j++ ) {
            if(board[i][j].vv && board[i][j].uu != turn ) return false;
        }
    }
    return true;
}
bool loseGame(vector<vector<pii>>board , int turn) {

    if( turn == 1) turn =2 ;
    else turn = 1;
    return winGame(board , turn);
}

bool isSide(int x, int y ) {

    return(x == 0 || x == N-1 || y == 0 || y == N-1)  ;
}


bool isCorner(int x , int y) {
    for(int i =0 ; i < 4 ; i++ ) {
        if( cornerX[i] == x && cornerY[i] == y) return true;
    }
    return false;
}

bool insideBoard(int x , int y) {

    return (x >=0 && y>=0 && x < N && y < N);
}


///This BFS calculates the effectiveness of the chain reaction
///Needs a bit of modification
/// give credit for opponent's blowup
///subtract opponents next move
int bfs(vector<vector<pii>>&board , int x , int y ) {

    int totPoint = 0;
    queue<pii>q;
    q.push({x,y});
    int cnt = 0;
    int bonus = 0;
    int tot= 0;
    while( !q.empty() ) {

        int xx = q.front().uu;
        int yy = q.front().vv;

        q.pop();
        tot++;
        if( tot > 10) {
            break;
        }
        if( board[xx][yy].vv && board[xx][yy].uu ==1) {
            cnt++; ///enemy eaten
            if( isCorner(xx,yy) ) bonus += 10000;
            else if( isSide(xx,yy) && board[xx][yy].vv == critVal[xx][yy]-1) bonus += 5000;
            else if(board[xx][yy].vv == critVal[xx][yy]-1) bonus += 3000;
        }

        board[xx][yy].uu = 2;
        board[xx][yy].vv++;
        if( board[xx][yy].vv < critVal[xx][yy]) continue; ///not has to explode

        board[xx][yy].vv -= critVal[xx][yy]; ///explosion

        for(int i =0 ; i < 4; i ++ ) {
            int xxx = xx +dx[i];
            int yyy = yy + dy[i];
            if( insideBoard(xxx ,yyy) ) {
                q.push({xxx,yyy});
            }
        }
    }
    return bonus + (cnt * 500);

}


int getLevel(vector<vector<pii>>board , int x1 , int y1 , int x2 , int y2) {
    ///-1 is for 1st one is low
    ///0  for equal
    ///1 for 1st one is high
    int totProb1 = board[x1][y1].vv;
    int totProb2 = board[x2][y2].vv;

    if( critVal[x1][y1] < critVal[x2][y2]) totProb1--;
    else if(critVal[x1][y1] > critVal[x2][y2]) totProb2--;

    if( totProb1 < totProb2) return -1;
    if( totProb1 > totProb2) return 1;
    return 0;
}


int calcForCorner(vector<vector<pii>>board,int x, int y ) {

    if(board[x][y].uu ==0 ) { ///fillup

        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv >1) {
                return -3000; ///there's two on the side
            }
        }
        return 5000; ///safe to sit
    }
    else { ///blowup

        int cnt = 0;
        bool equalLevel = true;
        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu==1 ) {
                cnt++;
                if( getLevel(board , x , y , xx , yy) == -1 ) equalLevel = false;
            }
        }

        if( cnt ==0 ) return -3000;///no enemy
        if( equalLevel ) return 4000; ///equal level...its a must to sit
        return 500; ///not mandatory
    }
}



int calcForSides(vector<vector<pii>>board , int x , int y) {


    if( board[x][y].vv ==0 ) { ///fillup

        int cnt = 0 ;

        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv ) {
                cnt++;
            }
        }

        if( cnt==0) { ///No one adjacent
            return 2500;
        }
        int frnd = 0;

        bool high =false ,lo = false, equ = false;
        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu ==1 ) {
                int level = getLevel(board , x , y , xx , yy);
                if(  level== -1 ) high = true;
                else if(level == 0) equ = true; ///the states are of enemy
                else lo = true;
            }
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu ==2 ) {
                frnd++;
            }
            if( insideBoard(xx ,yy) && isCorner(xx,yy)) {
                return -1000;
            }
        }
        if( high ) return -2000; ///enemy at high
        if( equ ) return 2000; ///enemy at equal
        if( frnd ) return -100; ///friendly
        if( lo ) return 200;
        return 500;

    }

    if( board[x][y].vv ==1) { ///increment

        int cnt = 0 ;

        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].uu ) {
                cnt++;
            }
        }

        if( cnt==0) { ///No one adjacent
            return 500;
        }

        bool high =false ,lo = false, equ = false;
        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu ==1 ) {
                int level = getLevel(board , x , y , xx , yy);
                if(  level== -1 ) high = true;
                else if(level == 0) equ = true;
                else lo = true;
            }
        }
        if( equ ) return 2500; ///enemy at equal
        else if( high ) return -2500; ///enemy at high
        else if( lo ) return 200;
        return -200;
    }

    return INF; ///blowUp
}


int calcForMiddle(vector<vector<pii>>board , int x , int y) {

    if( board[x][y].vv <3 ) { ///fillup + increment

        int cnt = 0 ;

        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].uu ) {
                cnt++;
            }
        }

        if( cnt==0 && board[x][y].vv ==0 ) { ///No one adjacent
            return 1000;
        }
        if( cnt==0 && board[x][y].vv ==1 ) { ///No one adjacent
            return 500;
        }
        if( cnt==0 && board[x][y].vv ==2 ) { ///No one adjacent
            return 200;
        }
        int frnd = 0;
        bool high =false ,lo = false, equ = false;
        for(int i =0 ; i < 4 ; i++ ) {
            int xx = x + dx[i];
            int yy = y + dy[i];
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu ==1 ) {
                int level = getLevel(board , x , y , xx , yy);
                if(  level== -1 ) high = true;
                else if(level == 0) equ = true;
                else lo = true;
            }
            if( insideBoard(xx,yy) && board[xx][yy].vv && board[xx][yy].uu ==2 ) {
                frnd++;
            }
        }
        if( high ) return -2000; ///enemy at high
        if( equ ) return 1000; ///enemy at equal
        if( frnd ) 100;
        return 300;
    }

    return INF;
}


/// postive is  player 2
///negative for player 1
int getMagic(vector<vector<pii>>&board , int x , int y ,int turn) { ///reference added here

    int val = 100;
//    if( winGame(board , turn) ) return INF;
//    if( loseGame(board , turn)) return -INF;

    if( isCorner(x,y) ) {
        val = calcForCorner(board , x,y);
    }
    else if( isSide(x,y) ) {

        val = calcForSides(board , x , y );
    }
    else {
        val = calcForMiddle(board , x , y);
    }

    if( val == INF) return (bfs(board , x , y ) -1000);
    return (val + bfs(board , x , y ));
}



///maximizer = 2 -> ME (wants to maximize)
///maximizer = 1 -> other player(wants to minimize)
int miniMax(vector<vector<pii>> board,int x , int y ,  int depth ,int  alpha , int beta , int maximizer) {

    int magicVal = getMagic(board , x , y ,maximizer);
    if( depth <=0 )  {
        return magicVal *(maximizer == 2 ? 1 : -1);
    }


    if( magicVal == INF || magicVal == -INF ) return magicVal;

    if( maximizer==2) {

        int mxVal = -INF;

        for(int i =0 ; i < N ; i++ ) {
            for(int j = 0 ; j < N ; j++ ) {

                if( board[i][j].uu == 1) continue;

                int tmp = magicVal + miniMax( board, i , j ,depth -1 , alpha , beta, 1);
                mxVal = max(tmp , mxVal);
                alpha = max(alpha , tmp);
                if( beta <= alpha) return mxVal;
            }
        }
        return mxVal;
    }
    else {

        int mnVal = INF;

        for(int i =0 ; i < N ; i++ ) {
            for(int j = 0 ; j < N ; j++ ) {

                if( board[i][j].uu == 2) continue;

                int tmp = (magicVal + miniMax( board,i , j , depth -1 , alpha ,beta, 2))*(-1);
                mnVal = min(mnVal, tmp);
                beta = min(beta , tmp);
                if( beta <= alpha ) return mnVal;
            }
        }
        return mnVal;
    }
}

pii getPos(vector<vector<pii>> board){
    pii pos = {-1, -1};
    int val = -INF;

    for(int i =N -1; i >= 0 ; i-- ) {
        for(int j = N-1 ; j >=0 ; j-- ) {

            if( board[i][j].uu == 1) continue;

            int tmp = miniMax(board , i , j , 2 , -INF , INF , 2);
            if( tmp  > val) {
                val = tmp ;
                pos = pii(i,j);
            }
        }
    }
    return pos;
}



void precalCritical() {
     for(int i = 0 ; i <N ; i++ ) {
        for(int j = 0 ; j < N ; j++ ) {

            int cnt = 0;
            int x = i , y = j;
            for(int k = 0; k < 4 ; k++ ) {
                int xx = x + dx[k];
                int yy = y + dy[k];
                if(insideBoard(xx,yy)) cnt++;
            }
            critVal[x][y] = cnt;
        }
    }
}


void writeMove(int x, int y)
{
    ofstream out;
    out.open("shared_file.txt");
    out << 0 << "\n";
    out << x << " " << y << "\n";
    out.close();
}
bool myTurn(char me,vector<vector<pii>>&board) ///Reference is a must here
{
    ifstream in;
    in.open("shared_file.txt");

    char now;
    in >> now;

    if (now!=me) return false;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            string str;
            in >> str;

            if( str == "No") board[i][j] =pii(0,0);
            else {
                if( str[0] == me) board[i][j].uu = 2;
                else board[i][j].uu = 1;
                board[i][j].vv =  (str[1] - '0') ;
            }

        }
    }
    in.close();
    return true;
}

pii againSearch(vector<vector<pii>> board) {


    for(int i = 0 ; i < N ; i++ ) {
        for(int  j =0 ; j < N ; j++) {

            if( board[i][j].uu == 2 && board[i][j].vv < critVal[i][j] ) {
                return pii(i,j);
            }
        }
    }
}


int main(int argc, char *argv[])
{
    vector<vector<pii>> board(N, vector<pii>(N));
    precalCritical();

    char me = argv[1][0];

    while(1) {

        if( !myTurn(me, board) ) continue;

        pii nextCell = getPos(board);
        if( nextCell == pii(-1,-1) || board[nextCell.uu][nextCell.vv].uu==1 ) {
            nextCell = againSearch(board);
        }
        writeMove(nextCell.uu , nextCell.vv);
    }
    return 0;
}



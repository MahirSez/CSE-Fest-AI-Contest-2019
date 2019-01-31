import time
import random
import sys
import copy

grid_size = 8
INF: int = 100000000
list16 = [1,2,3,4,5,6]
maxx = 8

#----------------------------------------------------------------------------------------------------------------------------------------------

def read_file(player_color):
    with open("shared_file.txt") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return None
    if lines[0].strip('\n') == str(player_color):
        temp_grid = []
        for line in lines[1:]:
            temp_grid.append(line.strip('\n').split(" ")[:-1])
        return temp_grid
    return None

#----------------------------------------------------------------------------------------------------------------------------------------------

def grid_updater(grid, x, y, color):
    q = []
    q.append([x,y])

    timeout = time.time() + 5

    while len(q) is not 0 and time.time() < timeout:
        #print(len(q))
        x,y = q[0]
        del q[0]

        if grid[x][y] == 'No':
            grid[x][y] = color + '1'
            continue
        elif grid[x][y][1] == '1':
            if x in [0, 7] and y in [0, 7]:
                grid[x][y] = 'No'
                xx = 1 if x == 0 else 6
                yy = 1 if y == 0 else 6
                q.append([x,yy])
                q.append([xx,y])
                continue
            else:
                grid[x][y] = color + '2'
                continue
        elif grid[x][y][1] == '2':
            if x in [0, 7]:
                grid[x][y] = 'No'
                xx = 1 if x == 0 else 6
                q.append([x,y-1])
                q.append([x,y+1])
                q.append([xx,y])
                continue
            elif y in [0, 7]:
                grid[x][y] = 'No'
                yy = 1 if y == 0 else 6
                q.append([x-1,y])
                q.append([x+1,y])
                q.append([x,yy])
                continue
            else:
                grid[x][y] = color + '3'
                continue
        elif grid[x][y][1] == '3':
            grid[x][y] = 'No'
            q.append([x,y-1])
            q.append([x,y+1])
            q.append([x-1,y])
            q.append([x+1,y])
            continue

#----------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------

def is_safe(grid, x, y, myclr):
    #print('in is')
    opclr = 'G' if myclr == 'R' else 'R'

    if(grid[x][y][0] == opclr):
        return False

    myorbs = 0 if grid[x][y][0] == 'N' else int(grid[x][y][1])

    if x > 0:
        if grid[x-1][y][0] == opclr and int(grid[x-1][y][1]) > myorbs and not is_explosive(grid, x, y):
            return False
    if x < 7:
        if grid[x+1][y][0] == opclr and int(grid[x+1][y][1]) > myorbs and not is_explosive(grid, x, y):
            return False
    if y > 0:
        if grid[x][y-1][0] == opclr and int(grid[x][y-1][1]) > myorbs and not is_explosive(grid, x, y):
            return False
    if y < 7:
        if grid[x][y+1][0] == opclr and int(grid[x][y+1][1]) > myorbs and not is_explosive(grid, x, y):
            return False
    return True

#----------------------------------------------------------------------------------------------------------------------------------------------

def is_sound(grid, x, y):
    #print('in iss')
    if x > 0:
        if grid[x-1][y] != 'No':
            return False
    if x < 7:
        if grid[x+1][y] != 'No':
            return False
    if y > 0:
        if grid[x][y-1] != 'No':
            return False
    if y < 7:
        if grid[x][y+1] != 'No':
            return False
    return True

#----------------------------------------------------------------------------------------------------------------------------------------------

def has_opposite_explosive_cells(grid, x, y):
    #print('in hoe')
    myclr = grid[x][y][0]

    if myclr == 'N':
        return 0

    opclr = 'G' if myclr == 'R' else 'R'

    res = 0

    if x > 0:
        if grid[x-1][y][0] == opclr:
            if grid[x-1][y][1] == '3':
                res += 1
            elif grid[x-1][y][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x-1][y][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if x < 7:
        if grid[x+1][y][0] == opclr:
            if grid[x+1][y][1] == '3':
                res += 1
            elif grid[x+1][y][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x+1][y][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if y > 0:
        if grid[x][y-1][0] == opclr:
            if grid[x][y-1][1] == '3':
                res += 1
            elif grid[x][y-1][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x][y-1][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if y < 7:
        if grid[x][y+1][0] == opclr:
            if grid[x][y+1][1] == '3':
                res += 1
            elif grid[x][y+1][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x][y+1][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1
    return res

#----------------------------------------------------------------------------------------------------------------------------------------------

def has_own_explosive_cells(grid, x, y):
    #print('in hwe')
    myclr = grid[x][y][0]

    if myclr == 'N':
        return 0

    res = 0

    if x > 0:
        if grid[x - 1][y][0] == myclr:
            if grid[x - 1][y][1] == '3':
                res += 1
            elif grid[x - 1][y][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x - 1][y][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if x < 7:
        if grid[x + 1][y][0] == myclr:
            if grid[x + 1][y][1] == '3':
                res += 1
            elif grid[x + 1][y][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x + 1][y][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if y > 0:
        if grid[x][y - 1][0] == myclr:
            if grid[x][y - 1][1] == '3':
                res += 1
            elif grid[x][y - 1][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x][y - 1][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1

    if y < 7:
        if grid[x][y + 1][0] == myclr:
            if grid[x][y + 1][1] == '3':
                res += 1
            elif grid[x][y + 1][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
                res += 1
            elif grid[x][y + 1][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
                res += 1
    return res

#----------------------------------------------------------------------------------------------------------------------------------------------

def is_explosive(grid, x, y):
    #print('in ie')
    if grid[x][y][1] == '3':
        return True
    elif grid[x][y][1] == '2' and (x == 0 or y == 0 or x == 7 or y == 7):
        return True
    elif grid[x][y][1] == '1' and (x == 0 or x == 7) and (y == 0 or y == 7):
        return True
    else:
        return False

#----------------------------------------------------------------------------------------------------------------------------------------------

def find_chain(grid, x, y):
    #print('in fc')
    chain = []
    if not is_explosive(grid, x, y):
        return chain
    chain.append([x,y])

    q = []
    q.append([x,y])

    for i in range(100):
        if len(q) == 0:
            break
        x,y = q[0]
        del q[0]

        if x > 0 and is_explosive(grid, x-1, y):
            q.append([x-1,y])
            chain.append([x-1,y])
        if x < 7 and is_explosive(grid, x+1, y):
            q.append([x+1,y])
            chain.append([x+1,y])
        if y > 0 and is_explosive(grid, x, y-1):
            q.append([x,y-1])
            chain.append([x,y-1])
        if y < 7 and is_explosive(grid, x, y+1):
            q.append([x,y+1])
            chain.append([x,y+1])

#----------------------------------------------------------------------------------------------------------------------------------------------

def generate_list(grid, myclr, maxsize):
    #print('in gl')
    xylist = []
    templist = []
    chains = []
    opclr = 'G' if myclr == 'R' else 'R'

    for i in range(8):
        for j in range(8):
            if grid[i][j] == 'No' or grid[i][j][0] == myclr:
                templist.append([i,j])

    if(len(templist) <= maxsize):
        return templist

    for i in [0,7]:
        for j in [0,7]:
            if len(xylist) >= maxsize/4:
                break
            if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                xylist.append([i,j])
                chains.append(find_chain(grid, i, j))
        if len(xylist) >= maxsize/4:
            break
    for i in [0,7]:
        for j in list16:
            if len(xylist) >= maxsize/2:
                break
            if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                xylist.append([i,j])
                chains.append(find_chain(grid, i, j))
        if len(xylist) >= maxsize/2:
            break
    for j in [0,7]:
        for i in list16:
            if len(xylist) >= maxsize*3/4:
                break
            if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                xylist.append([i,j])
                chains.append(find_chain(grid, i, j))
        if len(xylist) >= maxsize*3/4:
            break
    for i in list16:
        for j in list16:
            if len(xylist) >= maxsize:
                break
            if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                xylist.append([i,j])
                chains.append(find_chain(grid, i, j))
        if len(xylist) >= maxsize:
            break

    if len(xylist) < maxsize:
        for [x,y] in templist:
            if grid[x][y] == 'No' or grid[x][y][0] == myclr and [i, j] not in chains and [i, j] not in xylist:
                xylist.append([i, j])
                chains.append(find_chain(grid, i, j))
                if len(xylist) >= maxsize:
                    break

    while len(xylist) < maxsize:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if grid[x][y] == 'No' or grid[x][y][0] == myclr and [i,j] not in chains and [i,j] not in xylist:
            xylist.append([i, j])
            chains.append(find_chain(grid, i, j))

    while len(xylist) < maxsize:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if grid[x][y] == 'No' or grid[x][y][0] == myclr and [i,j] not in xylist:
            xylist.append([i, j])

    return xylist



def aux_move_4(grid, player_color): #p1's move
    #print('in a4')
    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'

    xylist = generate_list(grid, myclr, 8)
    #print(len(xylist))

    diff4 = -INF
    for i,j in xylist:
        if grid[i][j] == 'No' or grid[i][j][0] == myclr:
            newgrid = copy.deepcopy(grid)
            grid_updater(newgrid, i, j, myclr)

            mycells = 0
            opcells = 0
            for i in range(8):
                for j in range(8):
                    if newgrid[i][j][0] == myclr:
                        mycells += 1
                    elif newgrid[i][j][0] == opclr:
                        opcells += 1

            diff = mycells - opcells
            if opcells == 0:
                return INF
            elif diff > diff4:
                diff4 = diff
    return diff4


def aux_move_3(grid, player_color): #p2's move
    #print('in a3')
    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'

    xylist = generate_list(grid, opclr, 8)
    #print(len(xylist))

    diff3 = INF
    for i,j in xylist:
        if grid[i][j] == 'No' or grid[i][j][0] == opclr:
            newgrid = copy.deepcopy(grid)
            grid_updater(newgrid, i, j, opclr)
            diff4 = aux_move_4(newgrid, myclr)

            if diff4 == -INF:
                return -INF
            if diff4 < diff3:
                diff3 = diff4
    return diff3

def aux_move_2(grid, player_color): #p1's move
    #print('in a2')
    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'

    xylist = generate_list(grid, myclr, 8)
    #print(len(xylist))

    diff2 = -INF
    for i,j in xylist:
        if grid[i][j] == 'No' or grid[i][j][0] == myclr:
            newgrid = copy.deepcopy(grid)
            grid_updater(newgrid, i, j, myclr)
            diff3 = aux_move_3(newgrid, myclr)
            if diff3 == INF:
                return INF
            if diff3 > diff2:
                diff2 = diff3
    return diff2

def aux_move_1(grid, player_color): #p2's move
    #print('in a1')
    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'

    xylist = generate_list(grid, opclr, 8)
    #print(len(xylist))

    diff1 = INF
    for i,j in xylist:
        if grid[i][j] == 'No' or grid[i][j][0] == opclr:
            newgrid = copy.deepcopy(grid)
            grid_updater(newgrid, i, j, opclr)
            diff2 = aux_move_2(newgrid, myclr)
            if diff2 == -INF:
                return -INF
            if diff2 < diff1:
                diff1 = diff2
    return diff1


def get_move(grid, player_color):
    #print('in getmove')

    maxmoves = 8

    x = 0
    y = 0

    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'

    xylist = []
    templist = []
    chains = []

    for i in range(8):
        for j in range(8):
            if grid[i][j] == 'No' or grid[i][j][0] == myclr:
                templist.append([i,j])

    if(len(templist) < maxmoves):
        xylist = templist
    else:
        for i in [0,7]:
            for j in [0,7]:
                if len(xylist) >= 2:
                    break
                if grid[i][j][0] == myclr and (has_opposite_explosive_cells(grid,i,j) > 0) and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= 2:
                break
        for i in [0,7]:
            for j in list16:
                if len(xylist) >= maxmoves/4:
                    break
                if grid[i][j][0] == myclr and has_opposite_explosive_cells(grid,i,j) > 1 and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves/4:
                break
        for j in [0,7]:
            for i in list16:
                if len(xylist) >= maxmoves*5/8:
                    break
                if grid[i][j][0] == myclr and has_opposite_explosive_cells(grid,i,j) > 1 and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves*5/8:
                break
        for i in list16:
            for j in list16:
                if len(xylist) >= maxmoves*6/8:
                    break
                if grid[i][j][0] == myclr and has_opposite_explosive_cells(grid,i,j) > 2 and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves*6/8:
                break

        #print(xylist)

        for i in [0,7]:
            for j in [0,7]:
                if len(xylist) >= maxmoves*7/8:
                    break
                if grid[i][j][0] == 'N' and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves*7/8:
                break
        for i in [0,7]:
            for j in list16:
                if len(xylist) >= maxmoves*7/8:
                    break
                if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves*7/8:
                break
        for j in [0,7]:
            for i in list16:
                if len(xylist) >= maxmoves*7/8:
                    break
                if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves*7/8:
                break
        for i in list16:
            for j in list16:
                if len(xylist) >= maxmoves:
                    break
                if grid[i][j][0] != opclr and is_safe(grid,i,j,myclr) and [i,j] not in chains and [i,j] not in xylist:
                    xylist.append([i,j])
                    chains.append(find_chain(grid, i, j))
            if len(xylist) >= maxmoves:
                break
        for [i, j] in templist:
            if len(xylist) >= maxmoves:
                break
            if len(xylist) < maxmoves and grid[i][j][0] != opclr and is_safe(grid, i, j, myclr) and [i, j] not in chains and [i, j] not in xylist:
                xylist.append([i, j])
                if len(xylist) >= maxmoves:
                    break

    #print(xylist)

    diff = -INF
    for [i,j] in xylist:
        #print(i,j)
        if grid[i][j] == 'No' or grid[i][j][0] == myclr:
            newgrid = copy.deepcopy(grid)
            grid_updater(newgrid, i, j, myclr)

            #if not opclr+'1' in newgrid and not opclr+'2' in newgrid and not opclr+'3' in newgrid:
                #return i * 10 + j

            mycells = 0
            opcells = 0
            for ii in range(8):
                for jj in range(8):
                    if newgrid[ii][jj][0] == myclr:
                        mycells += 1
                    elif newgrid[ii][jj][0] == opclr:
                        opcells += 1
            if opcells == 0:
                return i*10+j

            diff1 = aux_move_1(newgrid, myclr)
            if diff1 == INF:
                return i*10 + j
            if diff1 > diff:
                x = i
                y = j
                diff = diff1
    #print(x, y)
    return x*10+y


def select_move(grid, player_color):
    #print('in sl')
    myclr = player_color
    opclr = 'G' if myclr == 'R' else 'R'
    #print(myclr)

    xy = get_move(grid, player_color)
    x = int(xy / 10)
    y = xy % 10
    #print(x,y, xy)
    #print(grid[x][y][0] == opclr)

    if grid[x][y][0] == opclr:
        while True:
            x = random.randint(0,7)
            y = random.randint(0,7)
            if grid[x][y] == 'No' or grid[x][y][0] == player_color:
                return x, y

    #if grid[x][y] == 'No' or grid[x][y][0] == player_color:
    return x, y


def write_move(move):
    str_to_write = '0\n' + str(move[0]) + " " + str(move[1])
    with open("shared_file.txt", 'w') as f:
        f.write(str_to_write)


def main():
    player_color = sys.argv[1]
    while True:
        while True:
            # grid = read_file(player_color)
            grid = read_file(player_color)
            if grid is not None:
                break
            time.sleep(.01)
        move = select_move(grid, player_color)
        write_move(move)


if __name__ == "__main__":
    main()

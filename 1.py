import re
from itertools import combinations


def read_file(file_name):
    grid = []  # grid list from the bff file
    ac = 0  # number of reflect blocks
    bc = 0  # number of opqaue blocks
    cc = 0  # number of refract blocks
    xc = 0
    oc = 0

    file = open(file_name, "r")
    lines = file.readlines()
    grid_start = lines.index('GRID START\n')
    grid_end = lines.index('GRID STOP\n')
    y_length = grid_end - grid_start - 1
    first_line = lines[grid_start + 1].replace(' ', '')
    x_length = int((len(first_line) - 1))
    grid = [[0 for i in range(2 * x_length + 1)]
            for j in range(2 * y_length + 1)]

    y = 0
    for k in range(y_length):
        y = y + 1
        x = 0
        each_line = lines[grid_start + 1 + k].replace(' ', '')
        for p in each_line:
            x = x + 1
            if p == 'o':
                oc = oc + 1
                grid[2 * y - 1][2 * x - 1] = 1
            elif p == 'x':
                xc = xc + 1
                grid[2 * y - 1][2 * x - 1] = 2
            elif p == 'A':
                ac = ac + 1
                grid[2 * y - 1][2 * x - 1] = 3
            elif p == 'B':
                bc = bc + 1
                grid[2 * y - 1][2 * x - 1] = 4
            elif p == 'C':
                cc = cc + 1
                grid[2 * y - 1][2 * x - 1] = 5

    if list(filter(re.compile('A \\d').match, lines)) != []:
        Ablock = int(list(filter(re.compile('A').match, lines))[0][2])
    else:
        Ablock = 0
    if list(filter(re.compile('B \\d').match, lines)) != []:
        Bblock = int(list(filter(re.compile('B').match, lines))[0][2])
    else:
        Bblock = 0
    if list(filter(re.compile('C \\d').match, lines)) != []:
        Cblock = int(list(filter(re.compile('C').match, lines))[0][2])
    else:
        Cblock = 0
    block = [Ablock, Bblock, Cblock]

    lazorposition = []
    lazorstr = list(filter(re.compile('L \\d').match, lines))
    for string in range(len(lazorstr)):
        lazornum = lazorstr[string].split()
        for z in range(1, 5):
            lazorposition.append(lazornum[z])

    point = []
    pointstr = list(filter(re.compile('P \\d').match, lines))
    for strin in range(len(pointstr)):
        pointnum = pointstr[strin].split()
        for v in range(1, 3):
            point.append(pointnum[v])
    return grid, block, lazorposition, point


class lazor:
    def __init__(self, grid, block, lazorposition, point):
        self.grid = tuple(tuple(sub) for sub in grid)
        self.g = grid
        self.Ablock = block[0]
        self.Bblock = block[1]
        self.Cblock = block[2]
        self.lazorposition = lazorposition
        self.point = point
        self.pointnum = int(len(point) / 2)
        self.lazornum = int(len(lazorposition) / 4)

    def lazorbeam(self):
        c = 0
        lo = []
        di = []
        for i in range(self.lazornum):
            lo.append([int(self.lazorposition[c]),
                       int(self.lazorposition[c + 1])])
            di.append([int(self.lazorposition[c + 2]),
                       int(self.lazorposition[c + 3])])
            c = c + 4
        return lo, di

    def pointpos(self):
        c = 0
        pp = []
        for i in range(self.pointnum):
            pp.append([int(self.point[c]),
                       int(self.point[c + 1])])
            c = c + 2
        return pp

    def pos_ava(self, position):
        x = position[0]
        y = position[1]
        yd = len(self.grid)
        xd = len(self.grid[0])
        if x < xd and y < yd and x > 0 and y > 0 and self.grid[y][x] == 1:
            return True
        else:
            return False

    def pos_chk(self, position):
        x = position[0]
        y = position[1]
        yd = len(self.grid)
        xd = len(self.grid[0])
        if x < xd and y < yd and x >= 0 and y >= 0:
            return True
        else:
            return False

    def init_path(self):
        path = []
        location, direction = self.lazorbeam()
        for i in range(self.lazornum):
            lo, di = location[i], direction[i]
            path.append(lo)
            while self.pos_chk(path[-1]) is True and path[-1][0] > 0 and path[-1][1] > 0:
                path.append([path[-1][0] + di[0], path[-1][1] + di[1]])
        return path

    def block_in_path(self, path):
        block_path = []
        block_in_path = []
        print(len(path))
        for i in range(len(path) - 1):
            x = 0
            y = 0
            for k in range(2):
                if path[i + k][0] % 2 == 1:
                    x = path[i + k][0]
                elif path[i + k][1] % 2 == 1:
                    y = path[i + k][1]
            if self.pos_ava([x, y]) is True:
                block_in_path.append([x, y])
            block_path = [j for n, j in enumerate(
                block_in_path) if j not in block_in_path[:n]]
        return block_path

    def availble_position(self):
        grid = self.grid
        avaliblepos = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if self.pos_ava([x, y]) is True:
                    avaliblepos.append([x, y])
        return avaliblepos

    def availble_grid(self):
        g = self.g
        a = self.Ablock
        c = self.Cblock
        solution_set = []
        cc = 0
        totblock = a + c
        avaliblepos = self.availble_position()
        comb = list(combinations(avaliblepos, totblock))
        for i in range(len(comb)):
            block_position = comb[i]
            block_comb = list(combinations(block_position, a))
            for j in range(len(block_comb)):
                g = [list(x) for x in self.grid]
                abp = block_comb[j]
                cc = cc + 1
                for k in range(a):
                    x, y = abp[k]
                    g[y][x] = 3
                if c > 0:
                    for bl in comb[i]:
                        if bl not in abp:
                            bx, by = bl
                            g[by][bx] = 5
                solution_set.append(g)
        return solution_set

    def reflect_block_location(self, x, y, dx, dy):
        if y % 2 == 1:
            return [[x + dx, y], [dx * -1, dy]]
        elif x % 2 == 1:
            return [[x, y + dy], [dx, dy * -1]]

    def path(self, grid):
        location, direction = self.lazorbeam()
        total_path = []
        pp = self.pointpos()
        result = False
        counter = 0
        pointnum = self.pointnum
        for i in range(len(location)):
            lazor_path = [location[i]]
            dx, dy = direction[i][0], direction[i][1]
            g = grid
            refract = False
            refractpos = []
            refractdir = []
            xdimension = len(grid[0])
            ydimension = len(grid)
            state = True
            while state is True:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                if x >= 0 and y >= 0 and x < xdimension and y < ydimension:
                    block = self.reflect_block_location(x, y, dx, dy)
                    bx = block[0][0]
                    by = block[0][1]
                    if self.pos_chk([bx, by]) is True:
                        if g[by][bx] == 3:
                            dx = block[1][0]
                            dy = block[1][1]
                            nx = x + dx
                            ny = y + dy
                        elif g[by][bx] == 1 or g[by][bx] == 2:
                            nx = x + dx
                            ny = y + dy
                        elif g[by][bx] == 5:
                            refract = True
                            refractdir = self.reflect_block_location(
                                x, y, dx, dy)
                            rex = refractdir[1][0]
                            rey = refractdir[1][1]
                            refractpos = [[x, y], [rex, rey]]
                            nx = x + dx
                            ny = y + dy
                        elif g[by][bx] == 4:
                            state = False
                            break
                    else:
                        state = False
                    if self.pos_chk([nx, ny]) is True:
                        lazor_path.append([nx, ny])
                else:
                    state = False
            for element in lazor_path:
                total_path.append(element)
        if refract is True:
            refract_path = self.refract(grid, refractpos)
            for rp in refract_path:
                total_path.append(rp)
        for elem in pp:
            if elem in total_path:
                counter = counter + 1
            else:
                counter = counter
        if counter == pointnum:
            result = True
        return result, total_path

    def refract(self, grids, refractpos):
        location, direction = refractpos[0], refractpos[1]
        total_path = []
        grid = grids
        for i in range(len(location)):
            lazor_path = [location]
            dx, dy = direction[0], direction[1]
            g = grid
            xdimension = len(grid[0])
            ydimension = len(grid)
            state = True
            while state is True:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                if x != 0 and y != 0 and x < xdimension - 1 and y < ydimension - 1:
                    block = self.reflect_block_location(x, y, dx, dy)
                    bx = block[0][0]
                    by = block[0][1]
                    if g[by][bx] == 3 or g[by][bx] == 5:
                        dx = block[1][0]
                        dy = block[1][1]
                        nx = x + dx
                        ny = y + dy
                    elif g[by][bx] == 1 or g[by][bx] == 2:
                        nx = x + dx
                        ny = y + dy
                    elif g[by][bx] == 4:
                        state = False
                    if self.pos_chk([nx, ny]) is True:
                        lazor_path.append([nx, ny])
                else:
                    state = False
            for element in lazor_path:
                total_path.append(element)
        return total_path

    def put_b_block(self, grid):
        grid = tuple(tuple(sub) for sub in grid)
        num = self.Bblock
        avaliblepos = []
        bbl = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    avaliblepos.append([x, y])
        comb = list(combinations(avaliblepos, num))
        for i in range(len(comb)):
            g = [list(x) for x in grid]
            for j in range(num):
                bx = comb[i][j][0]
                by = comb[i][j][1]
                g[by][bx] = 4
            bbl.append(g)
        return bbl

    def text(self, grid):
        f = open('solution.txt', "w")
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    f.write('o')
                elif grid[y][x] == 2:
                    f.write('x')
                elif grid[y][x] == 3:
                    f.write('A')
                elif grid[y][x] == 4:
                    f.write('B')
                elif grid[y][x] == 5:
                    f.write('C')
                elif grid[y][x] == 0:
                    f.write('')
                f.write(' ')
            f.write("\n")
        f.close()
        return


if __name__ == "__main__":
    # get the information from the bff file and use them as input to
    # create lazor class object
    grid, block, lazorposition, point = read_file("mad_7.bff")
    a = lazor(grid, block, lazorposition, point)
    # get all the possible configurations of the grid when consider
    # only A and C blocks, B block does not change or continue path of
    # lazor, so treat B block as additional block to put after getting
    # solution grid (which mean all the target points) are in path
    solution_set = a.availble_grid()
    # 
    for i in range(len(solution_set)):
        g = solution_set[i]
        result, path = a.path(g)
        if result is True:
            if a.Bblock == 0:
                print('The solution grid is', g)
                a.text(g)
            elif a.Bblock != 0:
                path_with_b = a.put_b_block(g)
                for j in range(len(path_with_b)):
                    B_grid = path_with_b[j]
                    TF, solution = a.path(B_grid)
                    if TF is True:
                        print('The solution grid is', B_grid)
                        a.text(B_grid)

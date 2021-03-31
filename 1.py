import re
from itertools import combinations


def read_file(file_name):
    grid = []  # grid list from the bff file
    ac = 0  # number of reflect blocks
    bc = 0  # number of opqaue blocks
    cc = 0  # number of refract blocks
    xc = 0
    oc = 0
    sc = 0

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
            else:
                sc = sc + 1

    # print(grid)
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

    def printer(self):
        print("grid:", self.grid)
        print("Ablock:", self.Ablock)
        print("Bblock:", self.Bblock)
        print("Cblock:", self.Cblock)
        print("lazorposition:", self.lazorposition)
        print("point:", self.point)
        print("pointnum:", self.pointnum)
        print("lazornum:", self.lazornum)
        print('g', self.g)

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
        #print(path)
        return path

    def block_in_path(self, path):
        # print("b", path)
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
        numseq = list(range(totblock))
        #print(totblock, a, numseq, len(avaliblepos))
        for i in range(len(comb)):
            block_position = comb[i]
            block_comb = list(combinations(block_position, a))
            for j in range(len(block_comb)):
                g = [list(x) for x in self.grid]
                abp = block_comb[j]
                cc = cc + 1
                # print(block_position, 'a', block_comb[j])
                for k in range(a):
                    x, y = abp[k]
                    g[y][x] = 3
                if c > 0:
                    b_list = []
                    for bl in comb[i]:
                        if bl not in abp:
                            # print('bl',bl)
                            bx, by = bl
                            g[by][bx] = 5
                #print(g)
                solution_set.append(g)
        # print(x, y)
        #print(len(block_comb) , len(comb))
        #print(cc)
        #print(len(solution_set))
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
            #print(len(location))
            #print(i)
            lazor_path = [location[i]]
            #print('s', lazor_path)
            dx, dy = direction[i][0], direction[i][1]
            g = grid
            refract = False
            refractpos = []
            refractdir = []
            xdimension = len(grid[0])
            ydimension = len(grid)
            state = True
            while state is True:
            # for i in range(1):
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                #print(x, y, "shit")
                #if x != 0 and y != 0 and x < xdimension and y < ydimension:
                if x >= 0 and y >= 0 and x < xdimension and y < ydimension:
                    #print("yes")
                    # print(x, y, dx, dy)
                    block = self.reflect_block_location(x, y, dx, dy)
                    # print(block)
                    bx = block[0][0]
                    by = block[0][1]
                    #print(bx, by, 'bb')
                    if self.pos_chk([bx, by]) is True:
                    #if 1 + 1 == 2:

                        if g[by][bx] == 3:
                            dx = block[1][0]
                            dy = block[1][1]
                            nx = x + dx
                            ny = y + dy
                            #print('Y')
                        elif g[by][bx] == 1 or g[by][bx] == 2:
                            #print("a")
                            nx = x + dx
                            ny = y + dy
                        elif g[by][bx] == 5:
                            refract = True
                            refractdir = self.reflect_block_location(x, y, dx, dy)
                            rex = refractdir[1][0]
                            rey = refractdir[1][1]
                            refractpos = [[x, y],[rex, rey]]
                            nx = x + dx
                            ny = y + dy
                            #print("5")
                            #print(refract, refractpos, refractdir,"11", rex, rey)
                        elif g[by][bx] == 4:
                            #nx = x
                            #ny = y
                            state = False
                            break
                    else:
                        state = False
                    if self.pos_chk([nx, ny]) is True:
                        lazor_path.append([nx, ny])
                        #print(lazor_path)
                else:
                    state = False
            for element in lazor_path:
                total_path.append(element)
        if refract is True:
            #print('111')
            refract_path = self.refract(grid, refractpos)
            for rp in refract_path:
                total_path.append(rp)
        #print('rsnm', total_path)
        #print('pp',pp)
        # result = all(elem in total_path for elem in pp)
        for elem in pp:
            if elem in total_path:
                #print("Yes", elem)
                counter = counter + 1
            else:
                counter = counter
                # print("no", elem)
        if counter == pointnum:
            result = True
        # print(result)
        return result, total_path

    def refract (self, grids, refractpos):
        location, direction = refractpos[0], refractpos[1]
        total_path = []
        grid = grids
        #print(location, direction,'f')
        for i in range(len(location)):
            lazor_path = [location]
            dx, dy = direction[0], direction[1]
            g = grid
            xdimension = len(grid[0])
            ydimension = len(grid)
            state = True
            while state is True:
            # for i in range(1):
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                if x != 0 and y != 0 and x < xdimension - 1 and y < ydimension - 1:
                    block = self.reflect_block_location(x, y, dx, dy)
                    #print('n',block)
                    bx = block[0][0]
                    by = block[0][1]
                    #if self.pos_ava([bx, by]) is True:
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
                        #print(lazor_path)
                else:
                    state = False
            for element in lazor_path:
                total_path.append(element)
        #print(total_path)
        return total_path

    def put_b_block(self, grid):
        grid = tuple(tuple(sub) for sub in grid)
        num = self.Bblock
        #print(num, '1ga')
        #print('gl', g)
        avaliblepos = []
        bbl = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    avaliblepos.append([x, y])
        #print('ss',avaliblepos)
        comb = list(combinations(avaliblepos, num))
        #print(comb)
        for i in range(len(comb)):
            g = [list(x) for x in grid]
            for j in range(num):
                bx = comb[i][j][0]
                by = comb[i][j][1]
                g[by][bx] = 4
            bbl.append(g)
        # print('123',bbl[-1])
        return bbl

if __name__ == "__main__":
    grid, block, lazorposition, point = read_file("yarn_5.bff")
    a = lazor(grid, block, lazorposition, point)
    # a.printer()
    solution_set = a.availble_grid()
    cc = 0
    cb = 0
    for i in range(len(solution_set)):
        g = solution_set[i]
        result, path = a.path(g)
        if result is True:
            if a.Bblock == 0:
                cc = cc + 1
                print(g)
                print(path)
                #bip = a.block_in_path(path)
                #print(bip)
            #print(a.Bblock, 's')
            elif a.Bblock != 0:
                path_with_b = a.put_b_block(g)
                #print('11232', len(path_with_b))
                for j in range(len(path_with_b)):
                    final_path = path_with_b[j]
                    #print(final_path)
                    TF, solution = a.path(final_path)
                    if TF is True:
                        print(final_path)
                        print(solution)
                        cb = cb + 1


    print('cc',cc)
    print('cb',cb)
    # tiny5
    #g = [[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 4, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [
    #    0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 5, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]

    #g = [[0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 4, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 5, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
    #g = [[0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 4, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 5, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0]]
    #result = a.path(g)

    #print(result)

    # mad7
    #grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 3, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 3, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 1, 0, 3, 0, 1, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 3, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 3, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    #if grid in solution_set:
    #    print('aaaa')
    #a.path(grid)
    # a.check_solution(grid)
    # a.refract(grid)
    # print(a.reflect_block_location(4, 5, -1, -1))

    # mad 7
    # g = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 3, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # 6
    # g = [[0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 2, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 2, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
    # print('23',a.path(g))
    #if g in path_with_b:
    #    print('gg')

    # dark 1
    #g = [[0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 4, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 4, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0]]
    #print('23',a.path(g))
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
        print("Bblock:", self.  Bblock)
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
        print(path)
        return path

    def block_in_path(self, path):
        print("b", path)
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
        cc = 0
        totblock = a + c
        avaliblepos = self.availble_position()
        comb = list(combinations(avaliblepos, totblock))
        # print(totblock, a, numseq, 'ss',len(comb))
        for i in range(len(comb)):
            g = []
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
                    for bl in comb[i]:
                        if bl not in abp:
                            # print('bl',bl)
                            bx, by = bl
                            g[by][bx] = 5
                # print(g)
                # print(x, y)
        print(len(block_comb) * len(comb))
        print(cc)
        return

    def lazor_path(self, grid):
        location, direction = self.lazorbeam()
        lazor_path = location
        grid = grid
        refract = False
        for i in range(2):
            # reflect occurs on left or right of the block
            if lazor_path[-1][0] % 2 == 0:
                x = lazor_path[-1][0] + direction[0][0]
                y = lazor_path[-1][1]
                print(x, y)

                if grid[y][x] == 3:
                    direction[0][0] = - 1 * direction[0][0]
                    lx = lazor_path[-1][0] + direction[0][0]
                    ly = lazor_path[-1][1] + direction[0][1]
                    lazor_path.append([lx, ly])
                elif grid[y][x] == 5:
                    refract = True
                    refract_path = []
                    rx = lazor_path[-1][0] + direction[0][0]
                    ry = lazor_path[-1][1] + direction[0][1]
                    refract_path.append([rx, ry])

                    direction[0][0] = - 1 * direction[0][0]
                    lx = lazor_path[-1][0] + direction[0][0]
                    ly = lazor_path[-1][1] + direction[0][1]
                    lazor_path.append([lx, ly])
                    print(refract_path, lazor_path)
                elif grid[y][x] == 1 or grid[y][x] == 2:
                    rx = lazor_path[-1][0] + direction[0][0]
                    ry = lazor_path[-1][1] + direction[0][1]
            elif lazor_path[-1][1] % 2 == 0:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1] + direction[0][1]
                print(x, y)
        return

    def reflect_block_location(self, x, y, dx, dy):
        if y % 2 == 1:
            return {(x + dx, y): [dx * -1, dy]}
        elif x % 2 == 1:
            return {(x, y + dy): [dx, dy * -1]}

if __name__ == "__main__":
    grid, block, lazorposition, point = read_file("Tiny_5.bff")
    a = lazor(grid, block, lazorposition, point)
    # b = a.printer()
    c = a.init_path()
    # print(c)
    # print('a',a.block_in_path(c))
    print(a.availble_position())
    a.availble_grid()
    # a.printer()
    # a.lazor_path()
    grid = [[0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 4, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [
        0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 5, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
    a.lazor_path(grid)
    print(a.reflect_block_location(4, 5, -1, -1))

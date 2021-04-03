# Lazor Project for Software Carpentry
# Fan Wu, Heon Joon Lee, Vincent Clark
import re
from itertools import combinations


def read_file(file_name):
    '''
    Reads in a bff file and breaks down the file
    into different blocks which are represented by
    A, B, C, X, and O. After the data is processed
    the code will return the grid, type and number of blocks available,
    initial lazor position and direction, and list of target points.

    **Parameters**

        file_name: *str*
            The bff file from the Lazor game

    **Returns**
        grid: *list*
            List of list to represent available points and occupied
            points.

        block: *list*
            List of blocks that fall into A, B or C category. A meaning
            reflect block, B meaning opaque block, C meaning refract block.

        lazorposition: *list*
            List of integers representing the position and direction
            inside of the grid the lazor is.

        point: *list*
            List of integers representing the target points
            inside of the grid.
    '''
    grid = []  # grid list from the bff file
    ac = 0  # number of reflect blocks
    bc = 0  # number of opqaue blocks
    cc = 0  # number of refract blocks
    xc = 0  # number of blocks cannot place blocks
    oc = 0  # number of blocks can place blocks

    file = open(file_name, "r")
    lines = file.readlines()
    grid_start = lines.index('GRID START\n')
    grid_end = lines.index('GRID STOP\n')
    y_length = grid_end - grid_start - 1
    first_line = lines[grid_start + 1].replace(' ', '')
    x_length = int((len(first_line) - 1))

    # Grid will start at top left being 0, 0
    # Step size is by half blocks
    # Thus, this leads to even numbers indicating
    # the rows/columns between blocks, and odd numbers
    # intersecting blocks.

    grid = [[0 for i in range(2 * x_length + 1)]
            for j in range(2 * y_length + 1)]

    # Generate the list of list as the grid, 1 represents
    # available space for block; 2 represents no blovks allowed,
    # 3 represents fixed reflected block; 4 represents fixed opaque
    # blocks; and 5 represents fixed refract block
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

    # count the number of A, B, and C block and store
    # them into block list
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

    # create a list store the information of lazor position
    # and direction
    lazorposition = []
    lazorstr = list(filter(re.compile('L \\d').match, lines))
    for string in range(len(lazorstr)):
        lazornum = lazorstr[string].split()
        for z in range(1, 5):
            lazorposition.append(lazornum[z])

    # create a list store the information of target point position
    # and direction
    point = []
    pointstr = list(filter(re.compile('P \\d').match, lines))
    for strin in range(len(pointstr)):
        pointnum = pointstr[strin].split()
        for v in range(1, 3):
            point.append(pointnum[v])
    return grid, block, lazorposition, point


class lazor:
    '''
    Class object that contains functions to
    calculate changes in lazor position, check available
    positions, edit the path of the lazor and movement of blocks.
    '''

    def __init__(self, grid, block, lazorposition, point):
        '''
        This function initalizes the self, grid, block,
        lazor position, point, and number of points and lazors

        **Parameters**

            grid: *list*
                List of binary numbers to represent available points
                and occupied points.

            block: *list*
                List of number of reflect, opaque, and refract blocks

            lazorposition: *list*
                List of integers representing the position inside of
                the grid the lazor is.

            point: *list*
                List of integers representing the available points
                inside of the grid.

            pointnum: *list, int*
                Total number of points in point list divided by 2.

            lazornum: *list, int*
                Total number of entries in lazorposition divided by 4

            **Returns**

            None
            '''
        self.grid = tuple(tuple(sub) for sub in grid)
        self.g = grid
        self.Ablock = block[0]
        self.Bblock = block[1]
        self.Cblock = block[2]
        self.lazorposition = lazorposition
        self.point = point
        self.pointnum = int(len(point) / 2)
        self.lazornum = int(len(lazorposition) / 4)
        return

    def lazorbeam(self):
        '''
        Function that identifies the location and direction of the
        lazor beam within the grid.

        **Parameters**

        self: *object*
            Calls the lazor position and lazor num variable which represent
            the current location of the lazor in the grid and the number of
            lazors in the grid

        **Returns**

        lo: *list*
            List of integers representing the location of the lazor.

        di: *list*
            List of integers representing the direction of the lazor.

        '''
        # c is the counter add by for for each loop
        # lo is location list
        # di is direction list
        c = 0
        lo = []
        di = []
        for i in range(self.lazornum):
            # For every four integers in the list, append location
            # wih first two element, and append direction with 3rd
            # and 4th element.
            lo.append([int(self.lazorposition[c]),
                       int(self.lazorposition[c + 1])])
            di.append([int(self.lazorposition[c + 2]),
                       int(self.lazorposition[c + 3])])
            # switch to next four intergers group
            c = c + 4
        return lo, di

    def pointpos(self):
        '''
        Function to create a list of intersect coordinates of our target lazor.

        **Parameters**

        self: *object*
            Pointnum variable and point variable are called which represent
            the number of target points and a list of those target points.

        **Returns**

        pp: *list, int*
            List of point position.

        '''
        # c is the counter switch for every 2 intergers
        # pp is the list of point position
        c = 0
        pp = []
        for i in range(self.pointnum):
            pp.append([int(self.point[c]),
                       int(self.point[c + 1])])
            c = c + 2
        return pp

    def pos_ava(self, position):
        '''
        Function to check if a position is available to put a block
        on the grid. If the position is available, True is
        returned, otherwise False is returned.

        **Paramaters**

        self: *object*
            Object to call position check function and grid object.

        position: *tuple of 2 int*
            The coordinates of a possible move.

        **Returns**

        True or False: *bool*
        '''
        x = position[0]
        y = position[1]
        yd = len(self.grid)
        xd = len(self.grid[0])
        # The criteria is x and y is between 0 and their length
        # and this position in the grid is equal to 1 (availble space
        # to put block)
        if x < xd and y < yd and x > 0 and y > 0 and self.grid[y][x] == 1:
            return True
        else:
            return False

    def pos_chk(self, position):
        '''
        Function that checks if lazor can go through a postion in
        the grid. If True, the position is valid and within the grid
        if False, then position is not valid for lazor to go throug.

        **Parameters**

        self: *object*
            self object of grid.

        position: *tuple of 2 int*
            The coordinates of a position.

        **Returns**

        True or False: *bool*
        '''
        x = position[0]
        y = position[1]
        yd = len(self.grid)
        xd = len(self.grid[0])
        # The criteria is x and y value are between 0 and lenth
        # of their dimensions.
        if x < xd and y < yd and x >= 0 and y >= 0:
            return True
        else:
            return False

    def init_path(self):
        '''
        Function that defines the initial path of the lazor.

          **Parameters**

          self: *object*
            self object for the grid, lazorbeam, and
            position check function from above

          **Returns**

          path: *list, int*
            list of integers defining the coordinates of path of the
            lazor within the grid

        '''
        path = []
        location, direction = self.lazorbeam()
        for i in range(self.lazornum):
            lo, di = location[i], direction[i]
            path.append(lo)
            # append the path list from the initial lazor position
            # with their direction until the lazor hit the
            # boundary of the grid
            while self.pos_chk(path[-1]) is True and path[-1][0] > 0 and path[-1][1] > 0:
                path.append([path[-1][0] + di[0], path[-1][1] + di[1]])
        return path

    def block_in_path(self, path):
        '''
        Function to creat a list of block positions the lazor go
        through given a specific lazor path of points

        **Parameters**

        self: *object*
            Position available function is called to check if the
            spaces beyond the block are available.

        path: *list, int*
            List of integers representing the point the lazor go through.

        **Returns**

        block_path: *list, int*
            List of integers representing coordinates of blocks in path.
        '''
        block_path = []
        block_in_path = []
        for i in range(len(path) - 1):
            x = 0
            y = 0
            # Between two adjacent points the lazor go through, the block
            # between them has the position with odd x and y postion
            # from each of them
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
        '''
        Function to generate all possible position to place block inside
        the grid

        **Parameters**

        self: *object*
            Grid object is called which represents list of binary numbers
            to represent available points and occupied points.

        **Returns**

        availablepos: *list, int*
            List of integers representing x, y coordinates
            of possible grid positions
        '''
        grid = self.grid
        avaliblepos = []
        # append the position if the position is true in pos_ava function
        # for all points in the grid
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if self.pos_ava([x, y]) is True:
                    avaliblepos.append([x, y])
        return avaliblepos

    def availble_grid(self):
        '''
        Function to generate all possible comfiguration of grid by getting
        all the possible combination of the A blocks and C blocks.

        B block (opaque) is treated as extra block since they are not going
        to make useful change to the lazor path, so add B blocks later after
        finding the solution.

        C block (refract) is decomposed as two path, one is treated as
        reflect block, and another is treated as no block there, the lazor
        path of these two paths are added to make the total path

        Each grid is used to generate the lazor path of the grid to checked
        if the lazor path contains all the targeted points, and if yes,
        then the grid is added to our solution_set list.

        **Parameters**

        self: *object*
            g, Ablock, Cblock variables are used which stand for
            a temporary grid, the amount of reflect blocks, and refract blocks
            present in a bff file.

        **Returns**
            solution_set: *list, int*
                List of integers representing the correct grid.
        '''
        g = self.g
        a = self.Ablock
        c = self.Cblock
        solution_set = []
        # cc is the counter for debuging use
        cc = 0
        # total number of blocks of A and C to place here
        totblock = a + c
        # get all availble postion can place blocks
        avaliblepos = self.availble_position()
        # gives all the combination of different position to place blocks
        comb = list(combinations(avaliblepos, totblock))
        for i in range(len(comb)):
            block_position = comb[i]
            # gives all the combinations of blocks sequences inside
            # a given set of position chosen
            block_comb = list(combinations(block_position, a))
            for j in range(len(block_comb)):
                # g is the corresponding grid
                g = [list(x) for x in self.grid]
                # abp is the A block position
                abp = block_comb[j]
                # ignaore cc, debuging use
                cc = cc + 1
                for k in range(a):
                    # get the x, y cordinate for each A blocks
                    x, y = abp[k]
                    # Change the A block to 3 in the grid
                    g[y][x] = 3
                # if there is c block needed to place
                if c > 0:
                    for bl in comb[i]:
                        if bl not in abp:
                            # find the position of b block and
                            # change the cordinate in grid to 5
                            bx, by = bl
                            g[by][bx] = 5
                # get all the solution set here
                solution_set.append(g)
        return solution_set

    def reflect_block_location(self, x, y, dx, dy):
        '''
        Function to take in a lazor path and reflect the path according to
        the current path. If block type is A, the path is changed based
        on east/west or north/south surface. If x coordinate of path is even,
        laser hits east/west surface, thus x coordinate of path is switched
        left/right. Else, y coordinate of path hits the north/south surface
        of A block and path is switched up/down.

        **Parameters**

        self: *object*
            self object to represent the label of the block

        position: *tuple of 2 int*
            The coordinates of a possible move.

        **Returns**

        List of integers defining the coordinates and direction
        of the lazor path
        '''
        if y % 2 == 1:
            return [[x + dx, y], [dx * -1, dy]]
        elif x % 2 == 1:
            return [[x, y + dy], [dx, dy * -1]]

    def path(self, grid):
        '''
        Function to trace the path of the lazorbeam, this function treat
        B block as nothing in the block, the refract function treat B block
        as the reflect block, the total path is the sum of these two paths

        **Parameters**

        grid: *list*
            List of list to represent a specific grid

        **Returns**

        result: *bool*
            Result will equal True if the path contains all the target points
            in bff file, and false if it does not.

        total_path: *list, int*
            List of integers represent the lazor path.

        '''
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
            # refract is true when there is 5 in the grid
            refract = False
            refractpos = []
            refractdir = []
            xdimension = len(grid[0])
            ydimension = len(grid)
            # quit while loop when it reach bounday
            state = True
            while state is True:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                if x >= 0 and y >= 0 and x < xdimension and y < ydimension:
                    block = self.reflect_block_location(x, y, dx, dy)
                    bx = block[0][0]
                    by = block[0][1]
                    if self.pos_chk([bx, by]) is True:
                        # when the block is reflect, get new direction
                        # and move forward
                        if g[by][bx] == 3:
                            dx = block[1][0]
                            dy = block[1][1]
                            nx = x + dx
                            ny = y + dy
                        # move forward when the block is empty or
                        # no block allowed but lazor can go through
                        elif g[by][bx] == 1 or g[by][bx] == 2:
                            nx = x + dx
                            ny = y + dy
                        # when meet a refract block, act there is no
                        # block here and move forward, turn on the refract,
                        # store the refract direction and postion
                        elif g[by][bx] == 5:
                            refract = True
                            refractdir = self.reflect_block_location(
                                x, y, dx, dy)
                            rex = refractdir[1][0]
                            rey = refractdir[1][1]
                            refractpos = [[x, y], [rex, rey]]
                            nx = x + dx
                            ny = y + dy
                        # quit the loop when meet a fixed opaque block
                        elif g[by][bx] == 4:
                            state = False
                            break
                    # if the position out of boundary, quit the while loop
                    else:
                        state = False
                    # if the new next position is defined in the grid,
                    # append the path with new position
                    if self.pos_chk([nx, ny]) is True:
                        lazor_path.append([nx, ny])
                else:
                    state = False
            # append the lazor path when treat refract as no block
            # to total path
            for element in lazor_path:
                total_path.append(element)
        # if there is refract block, get another path when treat refract
        # as reflect block by refract block position and direction
        if refract is True:
            refract_path = self.refract(grid, refractpos)
            # append the lazor path when treat refract as reflect block
            # to total path
            for rp in refract_path:
                total_path.append(rp)
        # counter the number of target points inside the lazor path
        for elem in pp:
            if elem in total_path:
                counter = counter + 1
            else:
                counter = counter
        # if the number of target points inside the lazor path is same
        # as the total number of the target point, this is the solution grid
        if counter == pointnum:
            result = True
        return result, total_path

    def refract(self, grids, refractpos):
        '''
        Function to map the path of the lazor by treat refract block as a
        relect block. The path will start at the point of refract and end
        when it hit the boundary or fixed opaque

        **Parameters**

        grids: *list*
            List of lists to represent a specific grid

        refractpos: *list, int*
            List of integers representing the position of refract blocks
            inside of the grid.

        **Returns**

         total_path: *list, int*
            List of integers represent the lazor path when treat refract
            block as reflect block.

        '''
        # The code here is very similar to the path function, the different
        # is when a position in grid is 5, treat it as reflect block
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
                    # here is the different mechanism, treat refract block
                    # same as reflect block
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
        '''
        After getting the solution set, if there are extra opaque blocks,
        this is function to find all the possible configuration of opaque
        block position and put them in grid when applicable. The opaque
        block does not change or continue the path of the lazor so it was
        treated as useless block to lazor path and put back into the grid
        after the solution was formed.

        **Parameters**

        grid: *list*
            List of lists to represent available points and occupied
            points

        **Returns**

        bbl: *list, int*
            Final solution grid if there are opaque block inside the grid.
        '''
        # This is solution grid without opaque block
        grid = tuple(tuple(sub) for sub in grid)
        num = self.Bblock
        # List of availble position after putting reflect and refract block
        avaliblepos = []
        # Final solution grid with opaque block
        bbl = []
        # Get all the available point to put opaque block
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    avaliblepos.append([x, y])
        # Find all the combination of position for opaque block
        comb = list(combinations(avaliblepos, num))
        # change the position in grid to 4, get all the grids
        for i in range(len(comb)):
            g = [list(x) for x in grid]
            for j in range(num):
                bx = comb[i][j][0]
                by = comb[i][j][1]
                g[by][bx] = 4
            bbl.append(g)
        return bbl

    def text(self, grid):
        '''
        Function that opens and writes in a text file with a visual
        representation for where blocks should be for the solution.

        o = blank space but blocks are allowed

        x = blank space but no blocks are allowed

        A = reflect block

        B = opaque block

        C = refract block

        **Parameters**

        grid:  *list*
            List of list of number represent different blocks

        **Returns**

        Solution.txt: *txt file*
            File containing the solutions.
        '''
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
    grid, block, lazorposition, point = read_file("mad_1.bff")
    a = lazor(grid, block, lazorposition, point)

    # get all the possible configurations of the grid when consider
    # only A and C blocks, B block does not change or continue path of
    # lazor, so treat B block as additional block to put after getting
    # solution grid (which mean all the target points) are in path
    solution_set = a.availble_grid()
    # test every possible grid inside the solution set
    # state_AC and state_B are indicators to show if there is a solution
    state = False
    for i in range(len(solution_set)):
        # get the specific one testing grid
        g = solution_set[i]
        # get the result and path from the path function
        result, path = a.path(g)
        # for the solution set which all the targeted points are passed
        # by lazor, check if it has a opaque block
        if result is True:
            # if there is no opaque block, print the solution and make
            # solution text file
            if a.Bblock == 0:
                state = True
                print('The solution grid is', g)
                a.text(g)
            # if there is opaque block, call the put_b_function to update
            # final grids with opaque blocks, use path function to test if
            # the updated final grid go through all the targeted points
            # if true, print the solution and make solution test file
            elif a.Bblock != 0:
                path_with_b = a.put_b_block(g)
                for j in range(len(path_with_b)):
                    B_grid = path_with_b[j]
                    TF, solution = a.path(B_grid)
                    if TF is True:
                        state = True
                        print('The solution grid is', B_grid)
                        a.text(B_grid)
    if state is False:
        print("This is no solution for this game.")

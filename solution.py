'''Sudoku solution.'''

POINT_RECT = [
    (2, 2), (2, 5), (2, 8),
    (5, 2), (5, 5), (5, 8),
    (8, 2), (8, 5), (8, 8)
]
POINTER_ROW = [(_, 8) for _ in range(9)]
POINTER_COL = [(8, _) for _ in range(9)]

def print_result(mat):
    '''Print matrix.

    Args:
        mat: An 9*9 matrix of sudoku.

    Returns:
        A matrix with sudoku tips.
    '''
    from prettytable import PrettyTable

    mix = PrettyTable()
    mix.field_names = [str(_) for _ in range(1, 10)]
    for i in range(9):
        mix.add_row(mat[i])

    print(mix)

def get_tips(mat):
    '''Print sudoku tips.

    Args:
        mat: An 9*9 matrix of sudoku.

    Returns:
        A matrix with sudoku tips.
    '''
    ans = [[None] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if mat[i][j] is not None:
                ans[i][j] = (mat[i][j])
                continue

            remian = list(range(1, 10))
            # Lookup column
            for row in range(9):
                if mat[row][j] is not None and mat[row][j] in remian:
                    remian.remove(mat[row][j])

            # Lookup row
            for col in range(9):
                if mat[i][col] is not None and mat[i][col] in remian:
                    remian.remove(mat[i][col])

            # Lookup rect
            rect_x, rect_y = i // 3 * 3, j // 3 * 3
            for rect_row in range(3):
                rect_row = rect_x+rect_row
                for rect_col in range(3):
                    rect_col = rect_y+rect_col
                    if mat[rect_row][rect_col] is not None and mat[rect_row][rect_col] in remian:
                        remian.remove(mat[rect_row][rect_col])

            ans[i][j] = tuple(remian)

            # if (i, j) in POINTER_ROW:
            #     for x in range(9):

    # Print the tips
    print('Here is the tips:')
    for i in range(9):
        for j in range(9):
            if isinstance(ans[i][j], tuple):
                ans[i][j] = '(' + '|'.join(map(str, ans[i][j])) + ')'

    print_result(ans)

    return ans

def get_answer(mat):
    '''Print sudoku answer.

    References: https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku.

    Args:
        mat: An 9*9 matrix of sudoku.

    Returns:
        A matrix with sudoku answer.
    '''
    def find_next_cell_to_fill(grid, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if grid[x][y] == None:
                    return x, y
        for x in range(0, 9):
            for y in range(0, 9):
                if grid[x][y] == None:
                    return x, y
        return -1, -1

    def is_valid(grid, i, j, e):
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != grid[x][j] for x in range(9)])
            if columnOk:
                # finding the top left x,y co-ordinates of the section containing the i,j cell
                secTopX, secTopY = 3 *(i//3), 3 *(j//3) # floored quotient should be used here.
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    def solve_sudoku(grid, i=0, j=0):
        i, j = find_next_cell_to_fill(grid, i, j)
        if i == -1:
            return True
        for e in range(1, 10):
            if is_valid(grid, i, j, e):
                grid[i][j] = e
                if solve_sudoku(grid, i, j):
                    return True
                # Undo the current cell for backtracking
                grid[i][j] = None
        return False

    ans = [[col for col in row] for row in mat]
    solve_sudoku(ans)

    # Print the answer
    print('Here is the answer:')
    print_result(ans)

    return ans

if __name__ == '__main__':
    mat_test = [
        [5, 6, 8, 4, 2, 7, None, None, None],
        [3, 4, 2, None, 1, None, 7, None, None],
        [1, 9, 7, None, None, 3, None, None, 2],
        [None, None, None, None, 6, None, None, None, 5],
        [7, None, None, None, None, None, 2, None, None],
        [6, None, 5, 1, 3, None, 9, None, None],
        [9, None, None, None, None, 1, 5, None, None],
        [None, None, None, None, 4, None, None, 2, None],
        [None, 7, None, None, None, None, None, None, 8]
    ]

    get_tips(mat_test)
    get_answer(mat_test)

from math import sqrt

# get input initial sudoku square from user
def sudoku():
    '''
    print()
    dim = int(input('What is the size of sudoku square (n x n)? '))
    assert dim > 0, 'Dimension must be positive'
    assert round(sqrt(dim)) == sqrt(dim), 'Dimension must be a perfect sqaure'

    # get numbers
    print('\n\nENTER NUMBERS IN SUDOKU SQUARE:')
    print('Note: if the square is empty, press \'enter\' \n')
    sudoku_square = []
    row = []
    for i in range(dim):
        row = []
        for j in range(dim):
            x = input('Number at row ' + str(i + 1) + ' and column ' + str(j + 1) + ': ')
            if x != '':
                assert x.isdigit() and int(x) % 1 == 0 and int(x) <= dim and int(x) >= 1, 'Entry must be an integer between 1 and dim (inclusive)'
                row.append(int(x))
            else:
                row.append('')
            #print(row)
        sudoku_square.append(row)
    '''
    sudoku_square = [['',4,1,'',9,2,7,3,8],['',7,6,'',1,'',2,'',''],['','',2,'','','','',5,''],['',6,'','',5,1,8,'',4],['',8,3,4,'','','','',''],['','','',2,8,'',1,'',''],['',1,'',9,4,'',3,'',''],[6,'','','','',8,4,7,5],['',2,8,'',7,'',9,'',6]]
    dim = len(sudoku_square)

    # check for duplicate values
    # also, generate rows, columns, and squares
    all_rows, all_cols, all_squares = gen_arrays(sudoku_square)
    
    print('\n\nSOLVING THE FOLLOWING SQUARE...\n')
    print_square(sudoku_square)
    print()

    #####
    ##### WHILE LOOP STARTS HERE
    #####
    '''
    Functions implemented so far:
    - only one value left for each cell
    '''
    
    # solve the square
    
    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
    while not check_solved(sudoku_square):
        # print_square(sudoku_square)
        # if there is only one possible value for a cell, that must be the cell's value:
        for i in range(dim):
            for j in range(dim):
                if len(values[i][j]) == 1:
                    sudoku_square[i][j] = values[i][j][0]
                    all_rows, all_cols, all_squares = gen_arrays(sudoku_square)
                    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)

        # if a number can only go in one place for each row, column, or square, it must go in that cell:
        # check each row
        for i in range(dim):
            count_num = 0
            index = 0
            for rr in all_rows:
                if i + 1 in rr:
                    continue
                row_vals = values[all_rows.index(rr)]
                for vals in row_vals:
                    if i + 1 in vals:
                        count_num += 1
                        index = row_vals.index(vals)
                assert count_num > 0, 'Sudoku square cannot be solved' #, number='+str(i+1)
                if count_num == 1:
                    sudoku_square[all_rows.index(rr)][index] = i + 1
                    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
                    all_rows, all_cols, all_squares = gen_arrays(sudoku_square)
                    #print_square(sudoku_square)

        # check each column
        for i in range(dim):
            count_num = 0
            index = 0
            for cc in all_cols:
                if i + 1 in cc:
                    continue
                for row in range(dim):
                    if i + 1 in values[row][all_cols.index(cc)]:
                        count_num += 1
                        index = row
                assert count_num > 0, 'Sudoku square cannot be solved' #, number/col='+str(i+1)+' '+str(col)
                if count_num == 1:
                    sudoku_square[index][all_cols.index(cc)] = i + 1
                    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
                    all_rows, all_cols, all_squares = gen_arrays(sudoku_square)
                    #print_square(sudoku_square)

        
        # check each square
        square_values = []
        for i in range(dim):
            count_num = 0
            index_r = 0
            index_c = 0
            for sq in all_squares:
                if i + 1 in sq:
                    continue
                for c in range(int(sqrt(dim))):
                    col_start = c * int(sqrt(dim))
                    add_val = 0
                    for r in range(int(sqrt(dim))):
                        for k in range(int(sqrt(dim))):
                            for j in range(int(sqrt(dim))):
                                if i + 1 in values[col_start + k][j + add_val]:
                                    count_num += 1
                                    index_r = col_start + k
                                    index_c = j + add_val
                        add_val += int(sqrt(dim))
                assert count_num > 0, 'Sudoku square cannot be solved'
                if count_num == 1:
                    sudoku_square[index_r][index_c] = i + 1
                    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
                    all_rows, all_cols, all_squares = gen_arrays(sudoku_square)
                       
        # print_square(sudoku_square)
    
        # check for naked pairs
        row_pairs, col_pairs, sq_pairs = gen_arrays(values, check=False)
        for r in row_pairs:
            print(r)
        # rows
        z = 0
        for row_pair in row_pairs:
            z = naked_pairs(row_pair)
            if z:
                for pair in row_pair:
                    if pair != z and pair[::-1] != z:
                        if z[0] in pair:
                            values[row_pairs.index(row_pair)][row_pair.index(pair)].remove(z[0])
                        if z[1] in pair:
                            values[row_pairs.index(row_pair)][row_pair.index(pair)].remove(z[1])
        ### FUNCTIONAL UNTIL HERE ###
        # columns
        z = naked_pairs(row_pairs)
        if z:
            for pair in row_pairs:
                if pair != z and pair[::-1] != z:
                    if z[0] in pair:
                        values[row_pairs.index(pair)].remove(z[0])
                        
                    if z[1] in pair:
                        row_pairs[row_pairs.index(pair)].remove(z[1])
        # rows
        z = naked_pairs(row_pairs)
        if z:
            for pair in row_pairs:
                if pair != z and pair[::-1] != z:
                    if z[0] in pair:
                        row_pairs[row_pairs.index(pair)].remove(z[0])
                    if z[1] in pair:
                        row_pairs[row_pairs.index(pair)].remove(z[1])
        
        row_pairs, col_pairs, sq_pairs = gen_arrays(values, check=False)
        
        '''          
        # if a number is in a certain row/column, that same number should be eliminated from other cells in that row/column:
        for i in range(dim):
            for r in values:
                count_num = 0
                found = False
                index_of_num = 0
                if i + 1 in all_rows[values.index(r)]:
                    found = True
                for j in r:
                    if i + 1 in j:
                        count_num += 1
                        index_in_num = r.index(j)
                if (not found) and count_num == 1:
                    sudoku_square[values.index(r)][index_in_num] = i + 1
                    values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
        '''
        values = gen_possible_vals(sudoku_square, all_rows, all_cols, all_squares)
        all_rows, all_cols, all_squares = gen_arrays(sudoku_square)

    return sudoku_square                

  



# check that there are no duplicate values in a list of numbers
def unique_vals(x):
    for i in range(len(x)):
        for j in range(len(x)):
            if i != j and x[i] == x[j] and x[i] != '':
                return False
    return True





# generate rows, columns, and squares arrays for sudoku square and check for no duplicate values
def gen_arrays(sudoku_square, check=True):
    dim = len(sudoku_square)
    all_rows = []
    all_cols = []
    all_squares = []
    
    # rows
    for row in sudoku_square:
        if check:
            assert unique_vals(row), 'Each row can only have one of each number'
        all_rows.append(row)
    # columns
    for i in range(len(sudoku_square)):
        col = []
        for j in sudoku_square:
            col.append(j[i])
        # print(col)
        if check:
            assert unique_vals(col), 'Each column can only have one of each number'
        all_cols.append(col)
    # squares
    for c in range(int(sqrt(dim))):
        col_start = c * int(sqrt(dim))
        add_val = 0
        for r in range(int(sqrt(dim))):
            square = []
            for i in range(int(sqrt(dim))):
                for j in range(int(sqrt(dim))):
                    square.append(sudoku_square[col_start + i][j + add_val])
            if check:
                assert unique_vals(square), 'Each square can only have one of each number'
            all_squares.append(square)
            add_val += int(sqrt(dim))
    return all_rows, all_cols, all_squares





# print out a square
def print_square(square):
    dim = int(len(square))
    print(' ', end = '')
    for i in range(2*dim - 1):
        print('-', end = '')
    print()
    for i in square:
        print('|', end = '')
        for j in i:
            if j == '':
                print(' ', end = '')
            else:
                print(j, end = '')
            print('|', end = '')
        print()
    print(' ', end = '')
    for i in range(2*dim - 1):
        print('-', end = '')
    print()






# returns square assignment
def square_of_cell(row, col, dim):
    i = 0
    assert row < dim, 'Row number cannot be greater than the sudoku matrix dimension'
    assert col < dim, 'Column number cannot be greater than the sudoku matrix dimension'
    row_count = 0
    while i <= row:
        i += int(sqrt(dim))
        row_count += 1

    j = 0
    col_count = 0
    while j <= col:
        j += int(sqrt(dim))
        col_count += 1

    square_num = 0
    r = 0
    c = 0
    while r != row_count - 1:
        square_num += int(sqrt(dim))
        r += 1
    while c != col_count - 1:
        square_num += 1
        c += 1
    return square_num





# generate lists of the possible values of each square
def gen_possible_vals(square, rows, columns, squares):
    dim = int(sqrt(len(square)))
    square_values = []
    for i in range(dim**2):
        row_vals = []   
        for j in range(dim**2):
            vals = []
            if square[i][j] == '':
                for k in range(1,dim**2+1):
                    if not (rows[i].count(k) > 0 or columns[j].count(k) > 0 or squares[square_of_cell(i,j,dim**2)].count(k) > 0):
                        vals.append(k)
                assert len(vals), 'Sudoku square is overconstrained and therefore cannot be solved'
                row_vals.append(vals)
            else:
                row_vals.append([])
        square_values.append(row_vals)
    return square_values





# check for and return naked pairs in a list of lists of values
def naked_pairs(list):
    pairs = []
    for x in list:
        if len(x) == 2:
            pairs.append(x)
    if len(pairs) < 2:
        return []
    for i in range(len(pairs) - 1):
        # print(pairs[i], pairs[i][::-1], pairs[i + 1:])
        if pairs[i] in pairs[i + 1:] or pairs[i][::-1] in pairs[i + 1:]:
            return pairs[i]
    return []





# check if the given sudoku square is solved
def check_solved(square):
    for i in square:
        for j in i:
            if j == '':
                return False
    return True





result = sudoku()
print('SOLVED SQUARE:')
print()
print_square(result)

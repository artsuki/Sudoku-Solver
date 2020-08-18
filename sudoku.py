# encoding = utf-8
# editor: ARTSUKI
# 2020-08-18

import numpy as np


# this obj is only for the storage of the sudoku puzzle and all its solutions
# sudoku puzzle is a 9x9 np matrix
# the solutions are 9x9 np matrix either, and all saved in a list
class Sudoku:
    def __init__(self):
        self.sudoku = np.zeros([9, 9, ], dtype=np.int8)
        self.sudoku_final = []

    # input a 81 length number string, then get the sudoku number matrix
    def start_puzzle(self, sequence):
        if isinstance(sequence, str):
            if len(sequence) == 81:
                for index, number in enumerate(sequence):
                    num = int(number)
                    if num > 0:
                        self.sudoku[index // 9][index - index // 9 * 9] = num
            else:
                raise Exception("sequence lenth is not 81")
        else:
            raise Exception("sequence type error, need 81 lenth string of numbers")
        return

    # input number one by one
    # use column , row, number order
    def set_number(self, column, row, number):
        self.sudoku[row - 1][column - 1] = number
        return

    # print the sudoku numpy matrix
    # if default, print origine sudoku puzzle
    def print_sudoku(self, sudoku=False):
        if isinstance(sudoku, bool):
            sudoku = self.sudoku
        for index, array in enumerate(sudoku):
            if index % 3 == 0:
                print('-----+-' * 3)
            item = array.astype(str)
            print(f'{" ".join(item[:3])}| {" ".join(item[3:6])}| {" ".join(item[6:])}|')
        return

    # It is default to print all the solutions
    def print_answers(self):
        if len(self.sudoku_final) == 0:
            print('Failed to find any solution, sorry~')
            return
        elif len(self.sudoku_final) == 1:
            print('There is only 1 solution')
        else:
            print(f'There are {len(self.sudoku_final)} solutions')
        for solution in self.sudoku_final:
            self.print_sudoku(solution)
        return


# draft is a 9x9x9 matrix,
# it contains every possible number for each cell
# this means in 9x9 sudoku, each cell is a 9 array,
# for example,:
# if a cell is a given number such as 8, then cell is a numpy array as [0,0,0,0,0,0,0,1,0]
# if a cell has possible number for 1,3,9, then cell is as [1,0,1,0,0,0,0,0,1]
class Draft:
    def __init__(self):
        self.sudoku = np.ones([9, 9, 9, ], dtype=np.int8)
        self.alter = False

    def initiation(self, sudoku):
        for y, array in enumerate(sudoku):
            for x, number in enumerate(array):
                if number != 0:
                    self.sudoku[y][x] = np.zeros([9, ], dtype='int8')
                    #                     self.sudoku[y,:,number-1] = 0
                    #                     self.sudoku[:,x,number-1] = 0
                    #                     self.sudoku[y-y%3:y-y%3+3, x-x%3:x-x%3+3,number-1] = 0
                    self.sudoku[y, x, number - 1] = 1
        return

    def duplicate(self):
        new_draft = Draft()
        new_draft.sudoku = self.sudoku + 1 - 1
        return new_draft

    def translate(self):
        pos_list = []
        for y, matrix in enumerate(self.sudoku):
            row_list = []
            for x, array in enumerate(matrix):
                number = ''
                for index, num in enumerate(array):
                    if num == 1:
                        number += str(index + 1)
                row_list.append(number)
            pos_list.append(row_list)
        for y, row in enumerate(pos_list):
            if y % 3 == 0:
                print('--------------------------+-------------------------+-------------------------+-')
            for x, num in enumerate(row):
                if x % 3 == 0:
                    print('|', end=' ')
                print(num.ljust(7, ' '), end=' ')
            print('|')
        return

    def possibility_print(self):
        """This method is only used for debug"""
        # to test how many possible number in each cell
        # so if there is an 0 shows up, it means that there many be mistakes in algorithm
        progress = np.sum(self.sudoku, axis=2)
        progress[progress > 1] = 0
        solution = np.array2string(progress.ravel())[1:-1]
        while ' ' in solution:
            solution = solution.replace(' ', '')
        while '\n' in solution:
            solution = solution.replace('\n', '')
        print(solution)
        return

    def add_solution(self, sudoku):
        """the result must be checked"""
        index = np.where(self.sudoku == 1)[2]
        index += 1
        solution = index.flatten()
        solution.resize((9, 9))
        sudoku.sudoku_final.append(solution)
        return

    def finish_check(self):
        draft_array = np.sum(self.sudoku, axis=2).ravel()
        if (draft_array == 1).all():
            return True
        else:
            return False

    def _set_origin(self):
        origin = self.sudoku + 1
        origin -= 1
        return origin

    def alter_check(self, origin):
        return (origin != self.sudoku).any()

    # to find the last number and fill it
    # last number means in line or column or 3x3 grid, from 1 to 9,
    # only one number failed to appear,then this cell fill by this one
    def last_number(self):
        matrix = np.sum(self.sudoku, axis=2)
        if (matrix == 0).any():
            return False
        origin = self._set_origin()
        index = np.where(matrix == 1)
        for i in range(len(index[0])):
            y = index[0][i]
            x = index[1][i]
            position = np.where(self.sudoku[y, x] == 1)
            if not len(position[0]):
                return False
            number = position[0][0]
            self.sudoku[y, x, number] = 0
            self.sudoku[y, :, number] = 0
            self.sudoku[:, x, number] = 0
            self.sudoku[y - y % 3:y - y % 3 + 3, x - x % 3:x - x % 3 + 3, number] = 0
            self.sudoku[y, x, number] = 1
        if self.alter_check(origin):
            self.alter = True
        else:
            self.alter = False
        return True

    def depletion_last_number(self):
        """A while loop to deplete the 'last number'"""
        result = True
        self.alter = True
        while self.alter:
            self.alter = False
            result = self.last_number()
            if not result:
                break
        return result

    def least_possible_cell(self):
        """choose a cell with least possible number"""
        possible_matrix = np.sum(self.sudoku, axis=2)
        for possibility in range(2, 8):
            if (possible_matrix == possibility).any():
                positions = np.where(possible_matrix == possibility)
                y = positions[0][0]
                x = positions[1][0]
                return y, x

    def propose_hypothesis(self, y, x, index):
        """duplicate a draft and propose the hypothesis"""
        new_draft = self.duplicate()
        new_draft.sudoku[y][x] = np.zeros([9, ], dtype='int8')
        new_draft.sudoku[y][x][index] = 1
        return new_draft

    def backtrack(self, sudoku):
        """backtracking method to the exhaustion of any possibilities"""
        # find a cell with least possible number
        # propose a hypothesis for a possible solution
        # constrain the hypothesis
        # if get result, add solution
        # if error, return False
        # if uncertain, propose another hypothesis
        y, x = self.least_possible_cell()
        hypo_index = np.where(draft.sudoku[y][x] == 1)
        for index in hypo_index[0]:
            new_draft = self.propose_hypothesis(y, x, index)
            new_draft.constrain(sudoku)
        return

    def constrain(self, sudoku):
        """constrain the possibliity"""
        result = self.depletion_last_number()
        if not result:
            return
        finish = self.finish_check()
        if finish:
            self.add_solution(sudoku)
            return
        self.backtrack(puzzle)
        return


# test puzzle
puzzle = ['001039000095600000006000780708450900000970305100000000000800020002000400900000500',
          '001039000095680000006000780708451900000978315150000800000800020002000400900000500',
          ]
solver = Sudoku()
solver.start_puzzle(puzzle[0])
solver.print_sudoku()

draft = Draft()
draft.initiation(solver.sudoku)
draft.constrain(solver)

solver.print_answers()

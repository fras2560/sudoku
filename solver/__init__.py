"""
-------------------------------------------------------
solver
a sudoku solver package
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-07
-------------------------------------------------------
"""
from solver.graph import Graph

class Solver():
    def __init__(self):
        self.graph = Graph(9)
        self.n = 9

    def load(self, file):
        '''
        loads the sudoku puzzle from a file
        Parameters:
            file: the file path
        Returns:
            none
        Raised:
            Exception if can't be opened
        '''
        loaded = False
        with open(file) as f:
            loaded = True
            row = 0
            for line in f:
                colors = line.replace("\n","").replace(" ","").split(",")
                column = 0
                for color in colors:
                    if self.is_int(color):
                        self.graph.set_node_color(row, column, int(color))
                    column += 1
                row += 1
        if not loaded:
            raise Exception("Did not load file")

    def is_int(self, number):
        '''
        checks if the given number is an int or not
        Paramteres:
            number:
            
        '''
        try:
            
            n = int(number)
            valid = True
        except:
            valid = False
        return valid

    def solve(self):
        '''
        a function that loops until it solves the puzzle or does
        know how to process on next move
        Parameters:
            None
        Returns:
            True if finished
            False if ran out of moves
        '''
        done = False
        iterations = -1
        while not done:
            iterations += 1
            print("Iteration:", iterations)
            done = True
            # look at each node
            for row in range(0, self.n):
                for column in range(0, self.n):
                    color_palette = self.graph.get_available_colors(row, column)
                    if len(color_palette) == 1:
                        self.graph.set_node_color(row, column, color_palette[0])
                        print("OBVSIOUS MOVE HIT:",row,column)
                        done = False
                    else:
                        column_colors = self.graph.get_column_colors(row,
                                                                     column)
                        exempt = self.a_not_in_b(color_palette, column_colors)
                        if iterations == 3:
                            print("(%d,%d)"%(row,column),color_palette, column_colors)
                        if len(exempt) == 1:
                            self.graph.set_node_color(row, column, exempt[0])
                            print("COLUMN HIT:",row,column)
                            done = False
                        else:
                            row_colors = self.graph.get_row_colors(row,
                                                                     column)
                            exempt = self.a_not_in_b(color_palette, row_colors)
                            if len(exempt) == 1:
                                self.graph.set_node_color(row, column,
                                                          exempt[0])
                                print("ROW HIT:",row,column)
                                done = False
        return

    def a_not_in_b(self, a, b):
        '''
        a method that check fors any elements from a not in b
        Parameters:
            a: a list of elements (list)
            b: a list of element (list)
        Returns:
            result: the elements from a not in b (list)
        '''
        result = []
        for x in a:
            if x not in b:
                result.append(x)
        return result

import unittest
import os
class Test(unittest.TestCase):
    def setUp(self):
        self.solver = Solver()
        self.test_directory = os.path.dirname(os.getcwd())
        self.test_file = os.path.join(self.test_directory, "tests", 'test.txt')

    def tearDown(self):
        pass

    def testIsInt(self):
        self.assertEqual(self.solver.is_int("a"), False)
        self.assertEqual(self.solver.is_int(1), True)


    def testLoad(self):
        self.solver.load(self.test_file)
        result = self.solver.graph.to_list()
        expect = [
                  [4, ' ', 7, 2, 8, 5, 6, ' ', ' '],
                  [' ', ' ', 5, ' ', 6, ' ', 2, 4, 8],
                  [' ', 6, 2, ' ', ' ', 9, ' ', 3, ' '],
                  [' ', 1, 9, 8, ' ', ' ', 7, ' ', ' '],
                  [7, ' ', ' ', ' ', 9, 6, 8, 2, ' '],
                  [2, 8, ' ', 5, 3, 7, ' ', ' ', 9],
                  [3, 7, ' ', 9, ' ', ' ', ' ', 8, 2],
                  [' ', ' ', 8, 3, 7, 4, ' ', ' ', 6],
                  [9, 4, ' ', ' ', 2, ' ', 3, ' ', 5]]
        self.assertEqual(expect, result)

    def testLoadColors(self):
        self.solver.load(self.test_file)
        r = self.solver.graph.get_available_colors(1, 0)
        expect = [0, 1]
        self.assertEqual(expect, r)

    def testSolve(self):
        self.solver.load(self.test_file)
        self.solver.solve()
        result = self.solver.graph.to_list()
        self.solver.graph.output()
        expect = [[3, 2, 6, 1, 7, 4, 5, 8, 0],
                  [0, 8, 4, 6, 5, 2, 1, 3, 7],
                  [7, 5, 1, 3, 0, 8, 4, 2, 6],
                  [5, 0, 8, 7, 3, 1, 6, 4, 2],
                  [6, 4, 2, 0, 8, 5, 7, 1, 3],
                  [1, 7, 3, 4, 2, 6, 0, 5, 8],
                  [2, 6, 5, 8, 4, 0, 3, 7, 1],
                  [4, 1, 7, 2, 6, 3, 8, 0, 5],
                  [8, 3, 0, 5, 1, 7, 2, 6, 4]]
        self.assertEqual(result, expect)

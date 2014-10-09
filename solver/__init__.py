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
        while not done:
            done = True
            # basic play
            for row in range(0, self.graph.rows):
                for column in range(0, self.graph.columns):
                    neighbors = self.graph.get_node_colors(row, column)
                    print(len(neighbors))
                    if len(neighbors) == 1:
                        done = False
                        for color in neighbors:
                            self.graph.set_node_color(row, column, color)
        return
                
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

    def testSolve(self):
        self.solver.load(self.test_file)
        self.solver.solve()
        result = self.solver.graph.to_list()
        print(result)
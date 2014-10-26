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
import logging

class Solver():
    def __init__(self, logger=None):
        self.n = 9
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.graph = Graph(9, logger)

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
        return loaded

    def is_int(self, number):
        '''
        checks if the given number is an int or not
        Parameters:
            number: a number to check (?)
        Returns:
            True if valid
            False otherwise
            
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
            self.logger.info("-----------------------------")
            self.logger.info("Iteration: %d" % iterations)
            self.logger.info("-----------------------------")
            done = True
            # look at each node
            for row in range(0, self.n):
                for column in range(0, self.n):
                    move = self.graph.make_move(row, column)
                    if move:
                        if not self.graph.validate():
                            self.logger.error("Wrong Move was played")
                        else:
                            print()
                            self.graph.output()
                            print()
                            done = False
            if iterations > 10:
                break
        return

import unittest
import os
class Test(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename="testing.log", level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.solver = Solver(logger=self.logger)
        self.test_directory = os.path.dirname(os.getcwd())
        self.test_files = []
        self.test_files.append(os.path.join(self.test_directory,
                                            "tests", 'test.txt'))
        self.test_files.append(os.path.join(self.test_directory,
                                            "tests", 'test2.txt'))
        self.test_files.append(os.path.join(self.test_directory,
                                            "tests", 'test3.txt'))

    def tearDown(self):
        pass

    def testIsInt(self):
        self.assertEqual(self.solver.is_int("a"), False)
        self.assertEqual(self.solver.is_int(1), True)

    def testLoad(self):
        self.solver.load(self.test_files[0])
        result = self.solver.graph.to_list()
        expect = [
                  [3, ' ', 6, 1, 7, 4, 5, ' ', ' '],
                  [' ', ' ', 4, ' ', 5, ' ', 1, 3, 7],
                  [' ', 5, 1, ' ', ' ', 8, ' ', 2, ' '],
                  [' ', 0, 8, 7, ' ', ' ', 6, ' ', ' '],
                  [6, ' ', ' ', ' ', 8, 5, 7, 1, ' '],
                  [1, 7, ' ', 4, 2, 6, ' ', ' ', 8],
                  [2, 6, ' ', 8, ' ', ' ', ' ', 7, 1],
                  [' ', ' ', 7, 2, 6, 3, ' ', ' ', 5],
                  [8, 3, ' ', ' ', 1, ' ', 2, ' ', 4]
                ]
        self.assertEqual(expect, result)

    def testLoadColors(self):
        self.solver.load(self.test_files[0])
        r = self.solver.graph.get_available_colors(1, 0)
        expect = [0]
        self.assertEqual(expect, r)
        r = self.solver.graph.get_available_colors(0, 1)
        expect = [2, 8]
        self.assertEqual(expect, r)

    def testSolve(self):
        self.solver.load(self.test_files[0])
        self.solver.solve()
        valid = self.solver.graph.validate()
        self.assertEqual(valid, True)
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

    def testSolve2(self):
        self.solver.load(self.test_files[1])
        self.solver.solve()
        valid = self.solver.graph.validate()
        self.assertEqual(valid, True)
        result = self.solver.graph.to_list()
        self.solver.graph.output()
        expect = [[1, 8, 0, 5, 7, 4, 6, 2, 3],
                  [2, 6, 7, 3, 0, 1, 4, 8, 5],
                  [5, 3, 4, 8, 2, 6, 1, 0, 7],
                  [7, 2, 3, 1, 4, 0, 8, 5, 6],
                  [8, 4, 1, 6, 3, 5, 0, 7, 2],
                  [6, 0, 5, 7, 8, 2, 3, 1, 4],
                  [0, 5, 6, 2, 1, 3, 7, 4, 8],
                  [3, 1, 8, 4, 5, 7, 2, 6, 0],
                  [4, 7, 2, 0, 6, 8, 5, 3, 1]]
        for i1, row in enumerate(result):
            for i2, column in enumerate(row):
                if column != ' ':
                    self.assertEqual(expect[i1][i2], column)

    def testSolve3(self):
        self.solver.load(self.test_files[2])
        self.solver.solve()
        valid = self.solver.graph.validate()
        self.assertEqual(valid, True)
        result = self.solver.graph.to_list()
        self.solver.graph.output()
        print(result)
        expect = [[0, 8, 6, 7, 5, 1, 2, 4, 3],
                  [7, 2, 1, 6, 3, 4, 0, 5, 8],
                  [4, 5, 3, 8, 0, 2, 1, 6, 7],
                  [1, 7, 0, 3, 2, 5, 6, 8, 4],
                  [5, 4, 8, 1, 7, 6, 3, 2, 0],
                  [6, 3, 2, 4, 8, 0, 5, 7, 1],
                  [3, 6, 5, 0, 4, 7, 8, 1, 2],
                  [8, 1, 7, 2, 6, 3, 4, 0, 5],
                  [2, 0, 4, 5, 1, 8, 7, 3, 6]]
        for i1, row in enumerate(result):
            for i2, column in enumerate(row):
                if column != ' ':
                    self.assertEqual(expect[i1][i2], column)


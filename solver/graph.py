"""
-------------------------------------------------------
graph
contains a Graph class
and a Node Class used by Graph class
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-10-07
-------------------------------------------------------
"""
import networkx as nx
import logging

class Graph():
    '''
    Graph
        a sudoku graph object
    '''
    def __init__(self, n, logger=None):
        '''
        constructor
            constructs a sudoku graph (n by n)
            Parameters:
                n: the size of the graph (int)
        '''
        self._graph = nx.Graph()
        self.columns = n
        self.rows = n
        index = 0
        while index < n:
            inside_column = 0
            # add all horizontal row
            while inside_column < index:
                self.add_node(Node(index, inside_column))
                inside_column += 1
            # add all vertical columns
            inside_row = 0
            while inside_row < index:
                self.add_node(Node(inside_row, index))
                inside_row += 1
            self.add_node(Node(index, index))
            index += 1
        if n == 9:
            # assume standard sudoku board
            for row  in range(0, 9, 3):
                for column in range(0, 9, 3):
                    node_list = self.assemble_square(row, column)
                    self.connect_node_list(node_list)
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger

    def assemble_square(self, row, column):
        '''
        a method that assembles a square given the row and column index
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Returns
            node_list: a list of the node id that make the square (list)
        '''
        node_list = []
        node_list.append(column + self.columns * row)
        node_list.append(column + self.columns * (row + 1))
        node_list.append(column + self.columns * (row + 2))
        node_list.append(column + 1 + self.columns * row)
        node_list.append(column + 1 + self.columns * (row + 1))
        node_list.append(column + 1 + self.columns * (row + 2))
        node_list.append(column + 2 + self.columns * row)
        node_list.append(column + 2 + self.columns * (row + 1))
        node_list.append(column + 2 + self.columns * (row + 2))
        return node_list

    def connect_node_list(self, nodes):
        '''
        a method that connect the node list together
        Parameters:
            nodes: the list of nodes to connect
        Returns:
            none
        Notes:
            some edges are added twice but using a simple graph
            so it has no effect
        '''
        while len(nodes) > 0:
            source = nodes.pop()
            for target in nodes:
                self._graph.add_edge(source, target)
        return

    def add_node(self, node):
        '''
        a method that add a node to the graph and connects to nodes accordingly
        Parameters:
            node: the node to add (Node)
        Returns:
            none
        '''
        row, column = node.get_index()
        if row > self.rows or column > self.columns:
            raise Exception("Invalid Node")
        node_id = column + row * self.columns
        self._graph.add_node(node_id, node=node)
        # connect to all previous nodes in its column
        for x in range(0, column):
            self._graph.add_edge(node_id, x + row * self.columns)
        # connect to all previous nodes in its row
        for x in range(0, row):
            self._graph.add_edge(node_id, column + x * self.columns)

    def set_node_color(self, row, column, color):
        '''
        a method that sets the Node color
        Parameters:
            row: the row index (int)
            column: the column index (int)
            color: the integer value of the color (int)
        Returns:
            none
        Raises:
            Exception: if color is already set or color is not an int
        '''
        node_id = column + self.columns * row
        nodes = nx.get_node_attributes(self._graph, 'node')
        check = nodes[node_id].get_color()
        if check is not None:
            raise Exception("Set a Node Color which already set")
        nodes[node_id].set_color(color)
        # remove that color from his neighbor color palette 
        for neighbor in self._graph.neighbors(node_id):
            nodes[neighbor].remove_available_color(color)

    def get_available_colors(self, row, column):
        '''
        a method that finds all the available colors for one node
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Returns:
            : list of available colors (list)
        '''
        node_id = column + self.columns * row
        nodes = nx.get_node_attributes(self._graph, 'node')
        return nodes[node_id].get_available_colors()

    def output(self):
        '''
        outputs the graph to the console
        Parameters:
            None
        Returns:
            None
        '''
        nodes = nx.get_node_attributes(self._graph, 'node')
        index = 0
        line_end = self.columns
        end = self.columns * self.rows
        while line_end <= end:
            line = []
            while index < line_end:
                color = nodes[index].get_color()
                if color is not None:
                    line.append(str(color))
                else:
                    line.append(" ")
                index += 1
            print(", ".join(line))
            self.logger.info(", ".join(line))
            line_end += self.columns

    def to_list(self):
        '''
        converts the nodes to a list of colors
        Parameters:
            None
        Returns:
            square matrix of the sudoku board with the colored nodes
        '''
        result = []
        nodes = nx.get_node_attributes(self._graph, 'node')
        row = 0
        while row < self.rows:
            result.append([])
            index = row* self.rows
            while index < self.columns * (row+1):
                color = nodes[index].get_color()
                if color is not None:
                    result[row].append(color)
                else:
                    result[row].append(" ")
                index += 1
            row += 1
        return result

    def get_nodes(self):
        '''
        a getter function for the Graphs' nodes
        Parameters:
            None
        Returns:
            a list of graph nodes (list)
        '''
        return self._graph.nodes()

    def same_square(self, c1,c2,r1,r2):
        '''
        a method that determines if the values given are in the same square
        Parameters:
            c1: the first column index
            c2: the second column index
            r1: the first row index
            r2: the second row index
        Returns:
            True if in same square
            False otherwise
        '''
        same = False
        if (c1 // 3 == c2 // 3) and (r1 // 3 == r2 // 3):
            same = True
        return same
 
    def two_color_move(self, node_id):
        '''
        a method to use to make a move on a cell that only has two colors
        Parameters:
            node_id: the node identifier (int)
        Returns:
            move: True if able to make a move
                  False otherwise
        '''
        row, column = self.get_row_column(node_id)
        nodes = nx.get_node_attributes(self._graph, 'node')
        palette = nodes[node_id].get_available_colors()
        move = False
        square_colors = []
        row_colors = []
        column_colors = []
        naked_pair = None
        for neighbor in self._graph.neighbors(node_id):
            n_palette = nodes[neighbor].get_available_colors()
            n_row, n_column = self.get_row_column(neighbor)
            if n_palette == palette:
                naked_pair = neighbor
            self.logger.debug("(%d, %d)'s Palette - %s"
                              %(n_row, n_column, self.list_to_string(n_palette)))
            if column == n_column:
                column_colors += n_palette
            elif row == n_row:
                row_colors += n_palette
            if self.same_square(n_column, column, n_row, row):
                # must be in same square
                square_colors += n_palette
        if naked_pair is not None:
            # found a naked pair
            move = True
            n_row, n_column = self.get_row_column(naked_pair)
            c1 = palette[1]
            c2 = palette[0]
            pair = [naked_pair, node_id]
            if n_row == row:
                # share row
                for c in range(0, self.columns):
                    n_id = self.get_node_id(row, c)
                    if n_id not in pair:
                        nodes[n_id].remove_available_color(c1)
                        nodes[n_id].remove_available_color(c2)
            elif n_column == column:
                # share column
                for r in range(0, self.rows):
                    n_id = self.get_node_id(r, column)
                    if n_id not in pair:
                        n = nodes[n_id]
                        n.remove_available_color(c1)
                        n.remove_available_color(c2)
            if self.same_square(column, n_column, n_row,row):
                # share square
                r = row - (row % 3)
                c = column - (column % 3)
                square = self.assemble_square(r, c)
                for node in square:
                    if node not in pair:
                        nodes[node].remove_available_color(c1)
                        nodes[node].remove_available_color(c2)
        expect = self.a_not_in_b(palette, row_colors)
        if len(expect) == 1:
            self.logger.debug("Row Move:(%d,%d)" %(row,column))
            self.set_node_color(row, column, expect[0])
            move = True
        else:
            expect = self.a_not_in_b(palette, column_colors)
            if len(expect) == 1:
                self.logger.debug("Column Move:(%d,%d)" %(row,column))
                self.set_node_color(row, column, expect[0])
                move = True
            else:
                expect = self.a_not_in_b(palette, square_colors)
                if len(expect) == 1:
                    self.logger.debug("Square Move:(%d,%d)" %(row,column))
                    self.set_node_color(row, column, expect[0])
                    move = True
        return move

    def three_color_move(self, node_id):
        '''
        a method that makes a move if the cell has three colors
        Parameters:
            node_id: the node identifier (int)
        Returns:
            move: True move was made
                  False otherwise
        '''
        row, column = self.get_row_column(node_id)
        nodes = nx.get_node_attributes(self._graph, 'node')
        palette = nodes[node_id].get_available_colors()
        move = False
        square_colors = []
        row_colors = []
        column_colors = []
        naked_row = []
        naked_column = []
        naked_square = []
        naked_trio = None
        for neighbor in self._graph.neighbors(node_id):
            n_palette = nodes[neighbor].get_available_colors()
            n_row, n_column = self.get_row_column(neighbor)
            self.logger.debug("(%d, %d)'s Palette - %s"
                              %(n_row, n_column, self.list_to_string(n_palette)))
            if column == n_column:
                column_colors += n_palette
                naked_trio = naked_column
            elif row == n_row:
                row_colors += n_palette
                naked_trio = naked_row
            if self.same_square(column, n_column, row, n_row):
                self.logger.debug("Same Square")
                square_colors += n_palette
                if n_palette == palette:
                    naked_square.append(neighbor)
                    if len(naked_square) == 2:
                        move = True
            if n_palette == palette:
                naked_trio.append(neighbor)
                if len(naked_trio) == 2:
                    move = True
        if move:
            # found a naked trio
            move = True
            c1 = palette[1]
            c2 = palette[0]
            c3 = palette[2]
            if len(naked_square) == 2:
                naked_trio = naked_square
                # share square
                naked_square.append(node_id)
                self.logger.debug("Naked Trio Share Square: %s" %
                                  (self.list_to_string(naked_square)))
                r = row - (row % 3)
                c = column - (column % 3)
                square = self.assemble_square(r, c)
                for node in square:
                    if node not in naked_square: 
                        nodes[node].remove_available_color(c1)
                        nodes[node].remove_available_color(c2)
                        nodes[node].remove_available_color(c3)
            n_row, n_column = self.get_row_column(naked_trio[0])
            if len(naked_row) == 2:
                # share row
                naked_row.append(node_id)
                self.logger.debug("Naked Trio Share Row: %s" %
                                  (self.list_to_string(naked_row)))
                for c in range(0, self.columns):
                    n_id = self.get_node_id(n_row, c)
                    if n_id not in naked_row:
                        nodes[n_id].remove_available_color(c1)
                        nodes[n_id].remove_available_color(c2)
                        nodes[n_id].remove_available_color(c3)
            elif len(naked_column) == 2:
                # share square
                naked_column.append(node_id)
                self.logger.debug("Naked Trio Share Column: %s" %
                                  (self.list_to_string(naked_square)))
                for r in range(0, self.rows):
                    n_id = self.get_node_id(r, n_column)
                    self.logger.debug(n_id)
                    if n_id not in naked_column:
                        n = nodes[n_id]
                        n.remove_available_color(c1)
                        n.remove_available_color(c2)
                        n.remove_available_color(c3)
        expect = self.a_not_in_b(palette, row_colors)
        if len(expect) == 1:
            self.logger.debug("Row Move:(%d,%d)" %(row,column))
            self.set_node_color(row, column, expect[0])
            move = True
        else:
            expect = self.a_not_in_b(palette, column_colors)
            if len(expect) == 1:
                self.logger.debug("Column Move:(%d,%d)" %(row,column))
                self.set_node_color(row, column, expect[0])
                move = True
            else:
                expect = self.a_not_in_b(palette, square_colors)
                if len(expect) == 1:
                    self.logger.debug("Square Move:(%d,%d)" %(row,column))
                    self.set_node_color(row, column, expect[0])
                    move = True
        return move

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

    def make_move(self, row, column):
        '''
        a method that try to color the node given
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Returns:
            True if move was available
            False otherwise
        '''
        nodes = nx.get_node_attributes(self._graph, 'node')
        node_id = self.get_node_id(row, column)
        palette = nodes[node_id].get_available_colors()
        number_colors = len(palette)
        move = False
        if number_colors != 0:
            if number_colors == 1:
                self.logger.info("Obvious Move: (%d, %d)"
                                 % self.get_row_column(node_id))
                move = True
                self.set_node_color(row, column, palette[0])
            elif number_colors == 2:
                self.logger.info("Two Color Move: (%d, %d) "
                                 % self.get_row_column(node_id))
                move = self.two_color_move(node_id)
            elif number_colors == 3:
                self.logger.info("Three Color Move: (%d, %d)"
                                 % self.get_row_column(node_id))
                move = self.three_color_move(node_id)
        return move

    def log(self, output):
        '''
        a method that logs the info
        Parameters:
            output: the output to log
        Returns:
            None
        '''
        if self.logger.debugging:
            print(output)

    def validate(self):
        '''
        a method that checks the coloring of the graph is valid
        Parameters:
            None
        Returns:
            True if valid
            False otherse
        '''
        nodes = nx.get_node_attributes(self._graph, 'node')
        valid = True
        index = 0
        while valid and index < len(nodes):
            color = nodes[index].get_color()
            if color is not None:
                for neighbor in self._graph.neighbors(index):
                    if nodes[neighbor].get_color() == color:
                        r1,c1 = self.get_row_column(index)
                        r2,c2 = self.get_row_column(neighbor)
                        self.logger.error('''
                                            Invalid graph:
                                            (%d, %d) & (%d, %d) have same color
                                          '''
                                          % (r1, c1, r2, c2))
                        valid = False
                        break 
            index += 1
        return valid

    def get_node_id(self, row, column):
        '''
        a method that finds the node id for the(row, column)
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Returns:
            node_id: the node id (int)
        '''
        node_id = column + self.columns * row
        return node_id

    def get_row_column(self, node_id):
        '''
        a method that finds the (row, column) from the node id
        Parameters:
            node_id: the node id
        Returns:
            (row, column): a tuple of the row and column (int)
        '''
        column = node_id % self.columns
        row = int((node_id - column) / self.columns)
        return (row, column)

    def list_to_string(self, l):
        '''
        a method that takes a list turns into a string for printing
        Parameters:
            l: the list to convert
        Returns:
            : the resulting string (string)
        '''
        e = []
        for element in l:
            e.append(str(element))
        return ",".join(e)
 
class Node():
    '''
    Node
        the nodes that make up a Graph
    '''
    def __init__(self, row, column, size=9, color=None, logger=None):
        self._column = column
        self._row = row
        self._color = color
        self._available_colors = [x for x in range(size)]
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger

    def get_index(self):
        '''
        a method that get the row and column indexes in the Graph
        Parameters:
            none
        Returns:
            : (row index, row columns) (tuple)
        '''
        return (self._row, self._column)

    def set_color(self, color):
        '''
        a method that sets the color of the Node
        Parameters:
            color: the int color of the Node (int)
        Returns:
            none
        Raises:
            Exception: if color is not an int
        '''
        if type(color) is int:
            self._color = color
            self.logger.info("Setting Node(%d,%d) to Color %d" %
                             (self._row, self._column, color))
            self._available_colors = []
        else:
            raise Exception("Node given non-int color")

    def get_color(self):
        '''
        a method that gets the color of the Node
        Parameters:
            none
        Returns:
            : color of the Node (int)
        '''
        return self._color

    def get_available_colors(self):
        '''
        a method that gets all the available colors for that node
        Parameters:
            none
        Returns:
            : list of available colors
        '''
        return self._available_colors

    def remove_available_color(self, color):
        '''
        a method that removes one color from the available color list
        Parameters:
            color: the int value of the color to remove
        Returns:
            none
        '''
        index = len(self._available_colors)
        done = False
        self.logger.debug("Removing color %d from node (%d, %d)"
                          % (color, self._row, self._column))
        while index > 0 and not done:
            index -= 1
            if self._available_colors[index] == color:
                self._available_colors.pop(index)
                done = True

        return

import unittest

class ThreeColorTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.g = Graph(9, logger=self.logger)
        # self.g.logger.debugging = True

    def testNakedTrioMoveSquare(self):
        column = 0
        for r in range(3, self.g.rows):
            self.g.set_node_color(r, column, r)
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        move = self.g.three_color_move(0)
        result = self.g.to_list()
        expect = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [3, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [4, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [5, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [7, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        expect_colors = [3, 4, 5, 6, 7, 8]
        checks = [1,2, 10, 11, 19, 20]
        for node in checks:
            self.assertEqual(nodes[node].get_available_colors(), expect_colors)
        self.assertEqual(move, True)
        self.assertEqual(expect, result)

    def testNakedTrioMoveColumn(self):
        self.g.set_node_color(0,1, 2)
        self.g.set_node_color(0,2, 3)
        self.g.set_node_color(1,1, 4)
        self.g.set_node_color(1,2, 5)
        self.g.set_node_color(2,1, 7)
        self.g.set_node_color(2,2, 8)
        move = self.g.three_color_move(0)
        result = self.g.to_list()
        expect = [[' ', 2, 3, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 4, 5, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 7, 8, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)
        self.assertEqual(move, True)
        checks = [27, 36, 45, 54, 63, 72]
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        expect_colors = [2, 3, 4, 5, 7, 8]
        for node in checks:
            self.assertEqual(expect_colors, nodes[node].get_available_colors())

    def testNakedTrioMoveRow(self):
        self.g.set_node_color(1,0, 2)
        self.g.set_node_color(1,1, 4)
        self.g.set_node_color(1,2, 5)
        self.g.set_node_color(2,0, 6)
        self.g.set_node_color(2,1, 7)
        self.g.set_node_color(2,2, 8)
        move = self.g.three_color_move(0)
        result = self.g.to_list()
        expect = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [2, 4, 5, ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, 7, 8, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        self.assertEqual(result, expect)
        self.assertEqual(move, True)
        checks = [3, 4, 5, 6, 7, 8]
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        expect_colors = [2, 4, 5, 6, 7, 8]
        for node in checks:
            self.assertEqual(expect_colors, nodes[node].get_available_colors())

    def testColumnMove(self):
        column = 0
        for r in range(3, self.g.rows ):
            self.g.set_node_color(r, column, r)
        self.g.set_node_color(1 , self.g.columns - 1, 0)
        self.g.set_node_color(2 , self.g.columns - 4, 0)
        move = self.g.three_color_move(0)
        self.assertEqual(move, True)
        result = self.g.to_list()
        expect = [[0, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 0],
                  [' ', ' ', ' ', ' ', ' ', 0, ' ', ' ', ' '],
                  [3, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [4, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [5, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [7, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)

    def testRowMove(self):
        row = 0
        for c in range(3, self.g.columns ):
            self.g.set_node_color(row, c, c)
        self.g.set_node_color(self.g.rows - 1 ,1 , 0)
        self.g.set_node_color(self.g.rows - 4 ,2 , 0)
        move = self.g.three_color_move(0)
        result = self.g.to_list()
        expect = [[0, ' ', ' ', 3, 4, 5, 6, 7, 8],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', 0, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 0, ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)
        self.assertEqual(move, True)

    def testSquareMove(self):
        self.g.set_node_color(0,2,2)
        self.g.set_node_color(1,0,3)
        self.g.set_node_color(1,1,4)
        self.g.set_node_color(1,2,5)
        self.g.set_node_color(2,0,6)
        self.g.set_node_color(2,1,7)
        self.g.set_node_color(2, self.g.columns - 1, 0)
        self.g.set_node_color(8,1,0)
        move = self.g.three_color_move(0)
        result = self.g.to_list()
        expect = [[0, ' ', 2, ' ', ' ', ' ', ' ', ' ', ' '],
                  [3, 4, 5, ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, 7, ' ', ' ', ' ', ' ', ' ', ' ', 0],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 0, ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)
        self.assertEqual(move, True)

class TwoColorTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.g = Graph(9, logger=self.logger)
        self.logger = logging
        #self.g.logger.debugging = True

    def testNakedPairMoveSquare(self):
        column = 0
        for r in range(2, self.g.rows):
            self.g.set_node_color(r, column, r)
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        move = self.g.two_color_move(0)
        result = self.g.to_list()
        expect = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [2, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [3, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [4, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [5, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [7, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        expect_colors = [3, 4, 5, 6, 7, 8]
        checks = [1,2, 10, 11, 19, 20]
        for node in checks:
            self.assertEqual(nodes[node].get_available_colors(), expect_colors)
        self.assertEqual(move, True)
        self.assertEqual(expect, result)

    def testNakedPairMoveColumn(self):
        self.g.set_node_color(0,1, 2)
        self.g.set_node_color(0,2, 3)
        self.g.set_node_color(1,1, 4)
        self.g.set_node_color(1,2, 5)
        self.g.set_node_color(2,0, 6)
        self.g.set_node_color(2,1, 7)
        self.g.set_node_color(2,2, 8)
        move = self.g.two_color_move(0)
        result = self.g.to_list()
        expect = [[' ', 2, 3, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 4, 5, ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, 7, 8, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)
        self.assertEqual(move, True)
        checks = [27, 36, 45, 54, 63, 72]
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        expect_colors = [2, 3, 4, 5, 7, 8]
        for node in checks:
            self.assertEqual(expect_colors, nodes[node].get_available_colors())

    def testNakedPairMoveRow(self):
        self.g.set_node_color(1,0, 2)
        self.g.set_node_color(0,2, 3)
        self.g.set_node_color(1,1, 4)
        self.g.set_node_color(1,2, 5)
        self.g.set_node_color(2,0, 6)
        self.g.set_node_color(2,1, 7)
        self.g.set_node_color(2,2, 8)
        move = self.g.two_color_move(0)
        result = self.g.to_list()
        expect = [[' ', ' ', 3, ' ', ' ', ' ', ' ', ' ', ' '],
                  [2, 4, 5, ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, 7, 8, ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)
        self.assertEqual(move, True)
        checks = [3, 4, 5, 6, 7, 8]
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        expect_colors = [2, 4, 5, 6, 7, 8]
        for node in checks:
            self.assertEqual(expect_colors, nodes[node].get_available_colors())

    def testColumnMove(self):
        column = 0
        for r in range(2, self.g.rows ):
            self.g.set_node_color(r, column, r)
        self.g.set_node_color(1 , self.g.columns - 1, 0)
        move = self.g.two_color_move(0)
        self.assertEqual(move, True)
        result = self.g.to_list()
        expect = [[0, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 0],
                  [2, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [3, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [4, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [5, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [6, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [7, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)

    def testRowMove(self):
        row = 0
        for c in range(2, self.g.columns ):
            self.g.set_node_color(row, c, c)
        self.g.set_node_color(self.g.rows - 1 ,1 , 0)
        move = self.g.two_color_move(0)
        self.assertEqual(move, True)
        result = self.g.to_list()
        expect = [[0, ' ', 2, 3, 4, 5, 6, 7, 8],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 0, ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)

    def testSquareMove(self):
        self.g = Graph(9, self.logger)
        self.g.set_node_color(0,1,1)
        self.g.set_node_color(0,2,2)
        self.g.set_node_color(1,0,3)
        self.g.set_node_color(1,1,4)
        self.g.set_node_color(1,2,5)
        self.g.set_node_color(2,0,6)
        self.g.set_node_color(2,1,7)
        self.g.set_node_color(2, self.g.columns - 1, 0)
        move = self.g.two_color_move(0)
        self.assertEqual(move, True)
        result = self.g.to_list()
        expect = [[0, 1, 2, ' ', ' ', ' ', ' ', ' ', ' '], 
                  [3, 4, 5, ' ', ' ', ' ', ' ', ' ', ' '], 
                  [6, 7, ' ', ' ', ' ', ' ', ' ', ' ', 0], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(result, expect)

class GraphTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.n = 3
        self.g = Graph(self.n, logger=self.logger)

    def tearDown(self):
        pass

    def testAssembleSquare(self):
        node_list = self.g.assemble_square(0, 0)
        expected = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        self.assertEqual(expected, node_list)

    def testConnectNodeList(self):
        node_list = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        self.g.connect_node_list(node_list)
        for clique in nx.find_cliques(self.g._graph):
            expect = len(clique)
            break
        self.assertEqual(expect, self.n**2)

    def testGetNodeColors(self):
        self.g = Graph(9)
        expect =  [0, 1, 2, 3, 4,  5, 6, 7, 8]
        available = self.g.get_available_colors(0, 1)
        self.assertEqual(expect, available)
        
        # set one color
        self.g.set_node_color(0, 0, 0)
        available = self.g.get_available_colors(0, 1)
        expect =  [1, 2, 3, 4,  5, 6, 7, 8]
        self.assertEqual(expect, available)

    def testSetNodeColors(self):
        color = 0
        self.g.set_node_color(0, 0, color)
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        result = nodes[0].get_color()
        self.assertEqual(result, color)
        # check neighbors color were updated
        for neighbor in self.g._graph.neighbors(0):
            self.assertEqual(color in nodes[neighbor].get_available_colors(),
                             False)
            
        try:
            self.g.set_node_color(0, 0, color)
            self.assertEqual(True, False,
                             "SetNodeColor should have raised Exception")
        except:
            pass

    def testAddNode(self):
        # no test need since called in constructor
        pass

    def testSameSquare(self):
        self.assertEqual(self.g.same_square(0, 4, 3, 4), False)
        self.assertEqual(self.g.same_square(0, 0, 3, 4), True)
        self.assertEqual(self.g.same_square(0, 0, 3, 4), True)
        self.assertEqual(self.g.same_square(0, 0, 0, 4), False)

    def testANotInB(self):
        l1 = [1, 2, 3]
        l2 = [2, 3, 4, 5]
        result = self.g.a_not_in_b(l1, l2)
        expect = [1]
        self.assertEqual(result, expect)
        result = self.g.a_not_in_b(l2, l1)
        expect = [4, 5]
        self.assertEqual(result, expect)
        result = self.g.a_not_in_b(l2, l2)
        expect = []
        self.assertEqual(result, expect)

    def testValidate(self):
        self.g.set_node_color(0, 1, 0)
        valid = self.g.validate()
        self.assertEqual(valid, True, ' Valid Graph was said to not be valid')
        self.g.set_node_color(0, 2, 0)
        valid = self.g.validate()
        self.assertEqual(valid, False, ' InValid Graph was said to be valid')

    def testGetNodeId(self):
        result = self.g.get_node_id(0, 0)
        self.assertEqual(result, 0)
        result = self.g.get_node_id(1, 0)
        self.assertEqual(result, 3)
        result = self.g.get_node_id(1, 1)
        self.assertEqual(result, 4)

    def testGetRowColumn(self):
        result = self.g.get_row_column(0)
        self.assertEqual(result, (0, 0))
        result = self.g.get_row_column(3)
        self.assertEqual(result, (1, 0))
        result = self.g.get_row_column(4)
        self.assertEqual(result, (1, 1))

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.row = 2
        self.column = 2
        self.node = Node(self.row, self.column)

    def tearDown(self):
        pass

    def testGetIndex(self):
        row, column = self.node.get_index()
        self.assertEqual(self.row, row)
        self.assertEqual(self.column, column)

    def testGetSetColor(self):
        color = self.node.get_color()
        self.assertEqual(color, None)
        color = 1
        self.node.set_color(color)
        result = self.node.get_color()
        self.assertEqual(color, result)
        try:
            self.node.set_color("XX")
            self.assertEqual(True, False,
                             "Set Color: Failed to raise exception")
        except:
            pass

    def testGetRemoveAvailableColors(self):
        available = self.node.get_available_colors()
        expect = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(available, expect)
        self.node.remove_available_color(1)
        available = self.node.get_available_colors()
        expect = [0]
        self.node.set_color(0)
        available = self.node.get_available_colors()
        expect = []
        self.assertEqual(available, expect)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
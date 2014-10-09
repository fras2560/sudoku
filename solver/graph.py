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

class Graph():
    '''
    Graph
        a sudoku graph object
    '''
    def __init__(self, n):
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

    def get_node_colors(self, row, column):
        '''
        a method that gets all the available colors for the Node at
        index (row, column)
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Returns:
            result: a list of available colors (list)
        '''
        node_id = column + self.columns * row
        nodes = nx.get_node_attributes(self._graph, 'node')
        color = nodes[node_id].get_color()
        available_colors = {}
        if color is None:
            # initial all colors are available
            for x in range(0, self.columns):
                available_colors[x] = "available"
            # check each neighbor
            for neighbor in self._graph.neighbors(node_id):
                color = nodes[neighbor].get_color() 
                if color is not None and color in available_colors:
                    del available_colors[color]
        else:
            available_colors = {}
        result = []
        for key, value in available_colors.items():
            result.append(key)
        return result

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

class Node():
    '''
    Node
        the nodes that make up a Graph
    '''
    def __init__(self, row, column, color=None):
        self._column = column
        self._row = row
        self._color = color

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

import unittest

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.n = 3
        self.g = Graph(self.n)

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
        available = self.g.get_node_colors(0, 1)
        self.assertEqual(expect, available)
        
        # set one color
        nodes = nx.get_node_attributes(self.g._graph,'node')
        nodes[0].set_color(0)
        available = self.g.get_node_colors(0, 1)
        expect =  [1, 2, 3, 4,  5, 6, 7, 8]
        self.assertEqual(expect, available)

    def testSetNodeColors(self):
        color = 0
        self.g.set_node_color(0, 0, color)
        nodes = nx.get_node_attributes(self.g._graph, 'node')
        result = nodes[0].get_color()
        self.assertEqual(result, color)
        try:
            self.g.set_node_color(0, 0, color)
            self.assertEqual(True, False,
                             "SetNodeColor should have raised Exception")
        except:
            pass

    def testAddNode(self):
        # no test need since called in constructor
        pass

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.row = 1
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
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
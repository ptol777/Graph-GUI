from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from PyQt5.QtWidgets import QSizePolicy


class PlotCanvas(FigureCanvas):
    """
    class for plotting graphs in a canvas that can be used by GUI libraries
    """
    def __init__(self, parent=None):
        fig = plt.figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.graph = nx.Graph()
        self.nodeLabel = iter(range(100, 200))

    def getNodesString(self):
        """
        returns a list of all nodes as string data type
        :return: list of all nodes as strings
        """
        return [str(node) for node in self.graph.nodes]

    def setGraphMatrix(self, adj_matrix):
        """
        create a graph from a file containing an adjacency matrix
        :param matrix: path of the file containing the adjacency matrix
        :return:
        """
        self.graph = nx.from_numpy_matrix(adj_matrix)
        self.figure.clf()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos=pos, with_labels=True)
        self.draw()

    def setGraphList(self, adj_list):
        """
        create a graph from a file containing an adjacency list
        :param adj_list: path of the file containing the adjacency list
        :return:
        """
        self.graph = nx.read_adjlist(adj_list, nodetype=int)
        self.figure.clf()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos=pos, with_labels=True)
        self.draw()

    def addNode(self):
        """
        adds a node labeled as an integer starting from 100 to avoid confusion with file loaded nodes
        :return:
        """
        self.figure.clf()
        self.graph.add_node(next(self.nodeLabel))
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos=pos, with_labels=True)
        self.draw()

    def addEdge(self, node1, node2):
        """
        adds edge between node1 and node2
        :param node1:
        :param node2:
        :return:
        """
        self.figure.clf()
        self.graph.add_edge(node1, node2)
        pos = nx.spring_layout(self.graph)  # layouts make rendering more beautiful
        nx.draw_networkx(self.graph, pos=pos, with_labels=True)
        self.draw()
        print(self.graph.nodes)

    def findShortestPath(self, node1, node2):
        """
        computes a shortest path from node1 to node2 and color the nodes along the path
        :param node1: source node
        :param node2: destination node
        :return:
        """
        shortest_path = nx.shortest_path(self.graph, node1, node2)
        node_colors = ["blue" if n in shortest_path else "red" for n in self.graph.nodes()]  # colors nodes along path
        self.figure.clf()
        pos = nx.spring_layout(self.graph)
        # Each component of the graph is drawn separately to color some nodes
        nx.draw_networkx_nodes(self.graph, pos=pos, node_color=node_colors)
        nx.draw_networkx_edges(self.graph, pos=pos)
        nx.draw_networkx_labels(self.graph, pos=pos)
        self.draw()

    def writeList(self, file_name):
        """
        writes the adjacency list of the graph to a file
        :param file_name: path of the file where the adjacency list will be exported
        :return:
        """
        nx.write_adjlist(self.graph, file_name)

    def writeMatrix(self, file_name):
        """
        writes the adjacency matrix of the graph to a file
        :param file_name: path of the file where the adjacency graph will be exported
        :return: 
        """
        matrix = nx.to_numpy_matrix(self.graph, dtype="int")
        np.savetxt(file_name, matrix, fmt='%.d')
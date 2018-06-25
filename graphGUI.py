import sys

from PyQt5.QtWidgets import *

import numpy as np

import plotCanvas
import networkx as nx


class MyMainWindow(QMainWindow):
    """
    GUI app for building and studying graphs
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes all the UI elements
        :return:
        """
        # Window attributes
        self.setGeometry(100, 100, 900, 600)
        self.setFixedSize(self.size())
        self.center()
        self.setWindowTitle('Graph PTOL')

        # Main widget: toolWidget for the tools, canvas for plotting
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        self.toolWidget = QWidget()
        self.initToolWidget()
        self.canvas = plotCanvas.PlotCanvas(self)  # Where we display the plot

        # Layout
        hbox = QHBoxLayout()
        mainWidget.setLayout(hbox)
        hbox.addWidget(self.canvas)
        hbox.addWidget(self.toolWidget)

        self.show()

    def initToolWidget(self):
        """
        Initializes the tools
        :return:
        """
        # UI elements of the tool widget
        self.comboEdge1 = QComboBox()
        self.comboEdge2 = QComboBox()
        self.comboSP1 = QComboBox()
        self.comboSP2 = QComboBox()

        self.loadFileMatrixButton = QPushButton("Load Adjacency Matrix File")
        self.loadFileListButton = QPushButton("Load Adjacency List File")
        self.writeFileMatrixButton = QPushButton("Write Adjacency Matrix File")
        self.writeFileMatrixButton.setEnabled(False)
        self.writeFileListButton = QPushButton("Write Adjacency List File")
        self.writeFileListButton.setEnabled(False)
        self.addNodeButton = QPushButton("Add Node")
        self.addEdgeButton = QPushButton("Add Edge")
        self.addEdgeButton.setEnabled(False)
        self.shortestPathButton = QPushButton("Find Shortest Path")
        self.shortestPathButton.setEnabled(False)

        # Signals and slot
        self.loadFileMatrixButton.clicked.connect(self.loadFileMatrix)
        self.loadFileListButton.clicked.connect(self.loadFileList)
        self.writeFileMatrixButton.clicked.connect(self.writeFileMatrix)
        self.writeFileListButton.clicked.connect(self.writeFileList)
        self.addNodeButton.clicked.connect(self.addNode)
        self.addEdgeButton.clicked.connect(self.addEdge)
        self.shortestPathButton.clicked.connect(self.shortestPath)

        # Layout
        grid = QGridLayout()
        grid.addWidget(self.loadFileListButton, 0, 0)
        grid.addWidget(self.loadFileMatrixButton, 1, 0)
        grid.addWidget(self.addNodeButton, 2, 0)
        grid.addWidget(self.comboEdge1, 3, 0)
        grid.addWidget(self.comboEdge2, 3, 1)
        grid.addWidget(self.addEdgeButton, 3, 2)
        grid.addWidget(self.comboSP1, 4, 0)
        grid.addWidget(self.comboSP2, 4, 1)
        grid.addWidget(self.shortestPathButton, 4, 2)
        grid.addWidget(self.writeFileListButton, 5, 0)
        grid.addWidget(self.writeFileMatrixButton, 6, 0)
        self.toolWidget.setLayout(grid)


    def loadFileMatrix(self):
        print("Loading File")
        fileName = QFileDialog.getOpenFileName(self, filter="Text files (*.txt)")[0]
        print(fileName)
        adjacencyMatrix = np.loadtxt(fileName)
        print(adjacencyMatrix)
        self.canvas.setGraphMatrix(adjacencyMatrix)
        self.updateNodeList()

    def loadFileList(self):
        print("Loading File")
        fileName = QFileDialog.getOpenFileName(self, filter="Text files (*.txt)")[0]
        print(fileName)
        self.canvas.setGraphList(fileName)
        self.updateNodeList()

    def writeFileMatrix(self):
        print("Writing")
        fileName = QFileDialog.getSaveFileName(self, filter="Text files (*.txt)")[0]
        print(fileName)
        self.canvas.writeMatrix(fileName)

    def writeFileList(self):
        print("Writing")
        fileName = QFileDialog.getSaveFileName(self, filter="Text files (*.txt)")[0]
        print(fileName)
        self.canvas.writeList(fileName)

    def addNode(self):
        print("Adding node")
        self.canvas.addNode()
        self.updateNodeList()

    def updateNodeList(self):
        nodeList = self.canvas.getNodesString()
        self.comboEdge1.clear()
        self.comboEdge2.clear()
        self.comboEdge1.addItems(nodeList)
        self.comboEdge2.addItems(nodeList)
        self.comboSP1.clear()
        self.comboSP2.clear()
        self.comboSP1.addItems(nodeList)
        self.comboSP2.addItems(nodeList)

        if len(nodeList) > 1:
            self.addEdgeButton.setEnabled(True)
            self.shortestPathButton.setEnabled(True)
            self.writeFileMatrixButton.setEnabled(True)
            self.writeFileListButton.setEnabled(True)

    def addEdge(self):
        print("Adding edge")
        node1 = int(self.comboEdge1.currentText())
        node2 = int(self.comboEdge2.currentText())
        self.canvas.addEdge(node1, node2)

    def shortestPath(self):
        """
        displays the shortest path by coloring the nodes along the path
        :return:
        """
        node1 = int(self.comboSP1.currentText())
        node2 = int(self.comboSP2.currentText())
        try:
            self.canvas.findShortestPath(node1, node2)
        except nx.exception.NetworkXNoPath:
            print("NO PATH")
            message = QMessageBox()
            message.setIcon(QMessageBox.Warning)
            message.setText("No path between the nodes !")
            message.setWindowTitle("Warning")
            message.setStandardButtons(QMessageBox.Ok)
            message.exec_()

    def center(self):
        """
        centers the application main window
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())

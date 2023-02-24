from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QApplication,
    QPushButton,
    QWidget,
)
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
)
# from PyQt5.QtGui import QVector3D

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.pgcollections import OrderedDict

import numpy as np

from multiprocessing import Queue, Process, Event
import sys
import random
import time


def dataGeneartor(dataQ: Queue):
    while True:
        new_data = {
            'xs': [random.uniform(-10, 10) for _ in range(6)],
            'ys': [random.uniform(-10, 10) for _ in range(6)],
            'zs': [random.uniform(-10, 10) for _ in range(6)]
        }
        dataQ.put(new_data)
        time.sleep(0.1)

class Update3DGraphThread(QThread):
    done = pyqtSignal(dict)

    def __init__(self, radarDataQ: Queue):
        super(Update3DGraphThread, self).__init__()
        self.dataQ = radarDataQ
        
    def run(self):
        while True:
            data = self.dataQ.get()
            self.done.emit(data)

    def exit(self):
        self.terminate()

class RadarGraphWindow(QDialog):
    def __init__(self):
        super(RadarGraphWindow, self).__init__()
        self.setWindowTitle('mmWave Data')
        self.setMinimumSize(900, 700)

        self.dataQ = Queue()

        self.xs = []
        self.ys = []
        self.zs = []
        # self.xRange = (0, 10)
        # self.yRange = (0, 10)
        # self.zRange = (0, 10)

        self.initPlot3DGraph()
        self.initButtons()
        self.initUpdateThread()

        self.layout = QGridLayout()
        self.layout.addWidget(self.pcplot)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)

        self.setLayout(self.layout)
    
    def initUpdateThread(self):
        '''
        Initialise 3D graph update thread.
        '''
        self.updateThread = Update3DGraphThread(self.dataQ)
        self.updateThread.done.connect(self.update3DGraph)
        self.updateThread.start()

    def initButtons(self):
        '''
        Initialise start and stop buttons for data harvesting.
        '''
        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.startProcess)
        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopProcess)

    def startProcess(self):
        '''
        Start getting data.
        '''
        self.data_generate_process = Process(target=dataGeneartor, args=(self.dataQ,))
        self.data_generate_process.start()

    def stopProcess(self):
        '''
        Stop getting data.
        '''
        self.data_generate_process.terminate()

    def initPlot3DGraph(self):
        dummy = np.zeros((1, 3))

        self.pcplot = gl.GLViewWidget()

        # Background grid
        self.gz = gl.GLGridItem()
        self.gz.translate(0, 0, -2)
        # self.boundaryBoxViz = [gl.GLLinePlotItem(), gl.GLLinePlotItem()]
        # self.bottomSquare = [gl.GLLinePlotItem(), gl.GLLinePlotItem()]
        # for box in self.boundaryBoxViz:
        #     box.setVisible(False)
        self.scatter = gl.GLScatterPlotItem(size=5)
        self.scatter.setData(pos=dummy)
        # Axis
        self.axis = gl.GLAxisItem()
        self.axis.setSize(x=10, y=10, z=10)
        self.pcplot.addItem(self.gz)
        self.pcplot.addItem(self.axis)
        #Labels

        # 3D Scatter
        self.plotItems = []
        self.plot3DGraph()

        self.pcplot.addItem(self.scatter)

    def initStatistics(self):
        for plotItem in self.plotItems:
            plotItem

    def update3DGraph(self, data):
        # self.xs = [random.random() * 10 for _ in range(6)]
        # self.ys = [random.random() * 10 for _ in range(6)]
        # self.zs = [random.random() * 10 for _ in range(6)]

        self.xs = data['xs']
        self.ys = data['ys']
        self.zs = data['zs']
        self.clear3DGraph()
        self.plot3DGraph()
    
    def plot3DGraph(self):
        for x, y, z in zip(self.xs, self.ys, self.zs):
            print(f'({x}, {y}, {z})')
            scatterItem = gl.GLScatterPlotItem(size=5)
            scatterData = np.array([[x, y, z]])
            color = np.array([[255, 0, 0]])
            scatterItem.setData(pos=scatterData, color=color)

            self.pcplot.addItem(scatterItem)
            self.plotItems.append(scatterItem)
        print()
    
    def clear3DGraph(self):
        plotItems_copy = self.plotItems
        for plotItem in plotItems_copy:
            self.pcplot.removeItem(plotItem)
            self.plotItems.remove(plotItem)
    
if __name__ == '__main__':
    app = QApplication([])
    main = RadarGraphWindow()
    main.show()
    app.exec()

        

    
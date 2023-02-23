from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QApplication,
)
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
)
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.pgcollections import OrderedDict

import numpy as np

from multiprocessing import Queue
import sys

class Update3DGraphThread(QThread):
    done = pyqtSignal()

    def __init__(self, radarDataQ: Queue, fps: int):
        while True:
            data = radarDataQ.get()

    def run(self):
        
        self.done.emit('Done')
        pass

    def exit(self):
        self.terminate()

class RadarGraphWindow(QDialog):
    def __init__(self):
        super(RadarGraphWindow, self).__init__()
        self.setWindowTitle('mmWave Data')
        self.setMinimumSize(900, 700)

        self.xs = [1, 2, 3, 2, 1, 1, 1, 4]
        self.ys = [5, 3, 2, -1, 5, 7, 9, 6]
        self.zs = [7, 5, 4, 2, 1, 5, 6, 7]
        # self.xRange = (0, 10)
        # self.yRange = (0, 10)
        # self.zRange = (0, 10)

        self.setPlot3DGraph()

        self.layout = QGridLayout()
        self.layout.addWidget(self.pcplot)

        self.setLayout(self.layout)
    
    def setPlot3DGraph(self):
        dummy = np.zeros((1, 3))

        self.pcplot = gl.GLViewWidget()

        # Background grid
        self.gz = gl.GLGridItem()
        self.gz.translate(0, 0, -2)
        self.boundaryBoxViz = [gl.GLLinePlotItem(), gl.GLLinePlotItem()]
        self.bottomSquare = [gl.GLLinePlotItem(), gl.GLLinePlotItem()]
        for box in self.boundaryBoxViz:
            box.setVisible(False)
        self.scatter = gl.GLScatterPlotItem(size=5)
        self.scatter.setData(pos=dummy)
        self.pcplot.addItem(self.gz)
        # self.pcplot.addItem(self.boundaryBoxViz[0])
        # self.pcplot.addItem(self.boundaryBoxViz[1])
        # self.pcplot.addItem(self.bottomSquare[0])
        # self.pcplot.addItem(self.bottomSquare[1])

        # 3D Scatter
        for x in self.xs:
            for y in self.ys:
                for z in self.zs:
                    plotItem = gl.GLScatterPlotItem()
                    plotItem.setData(x, y, z)
                    self.pcplot.addItem(plotItem)


        self.pcplot.addItem(self.scatter)

    def update3DGraph(self, xs, ys, zs):
        self.xs = xs
        self.ys = ys
        self.zs = zs
    
if __name__ == '__main__':
    app = QApplication([])
    main = RadarGraphWindow()
    main.show()
    app.exec()

        

    
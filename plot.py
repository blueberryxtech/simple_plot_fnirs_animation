import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import argparse
import pandas as pd

settings = {
                "channel" : "c1",
                "path" : "short_path",
                "color" : "#00FF00",
                "width" : 10,
        }

class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        #  line plot
        self.otherplot = self.canvas.addPlot()
        self.h2 = self.otherplot.plot(pen=pg.mkPen(settings["color"], width=settings["width"]))

        #### Set Data  #####################

        self.x = x_data #np.linspace(0,50., num=200)
        self.y = y_data #np.meshgrid(self.x,self.x)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):
        if ((self.counter + 200) < len(self.x)):
            QtCore.QTimer.singleShot(99, self._update)
        else:
            print("DONE, ITERATED THROUGH ENTIRE FILE")

        #compute FPS
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)

        self.ydata = self.y[self.counter:self.counter+200]

        self.h2.setData(self.ydata)

        self.counter += 1


if __name__ == '__main__':
    global start_time, x_data, y_data
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', "--start_time", "--st", "-t", "-s", type=int,
                        help='an integer in unix time when you want to start at', required=True)

    parser.add_argument('--data', "--file", "--input", "-i", "-d", "-f", type=str,
                        help='the location of the data file CSV', required=True)


    args = parser.parse_args()
    start_time = args.time
    file_name = args.data
    df = pd.read_csv(file_name)
    data = df.loc[(df['timestamp'] >= start_time) & (df["path"] == settings["path"])]
    x_data = data["timestamp"].to_numpy()
    y_data = data[settings["channel"]].to_numpy()

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())

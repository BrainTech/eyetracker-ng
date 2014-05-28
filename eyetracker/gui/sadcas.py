from PyQt4 import QtGui, QtCore
from functools import partial


class Window(QtGui.QWidget):
    def __init__(self, mapping):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        self.buttons = []
        for key, value in mapping.items():
            self.buttons.append(QtGui.QPushButton(key, self))
            self.buttons[-1].clicked.connect(partial(handleButton, data=value))
            layout.addWidget(self.buttons[-1])



def handleButton(self, data="\n"):
    print (data)


if __name__ == '__main__':
    import sys

    buttons = {'foo': 'bar', 'something': 'other', 'a': 'a'}
    app = QtGui.QApplication(sys.argv)
    window = Window(buttons)
    window.show()
    sys.exit(app.exec_())

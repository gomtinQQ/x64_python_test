

from PyQt6.QtWidgets import *



#class MainWindow(QMainWindow, form_class):
#    def __init__(self):
#        super().__init__()




if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()
    app.exec()


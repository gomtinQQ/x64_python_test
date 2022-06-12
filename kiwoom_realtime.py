
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from kiwoom.KHOpenApi import *


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, header_text):
        super(TableModel, self).__init__()
        self._data = data
        self.header_text = header_text

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole:
            return QtGui.QColor(240,240,240)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignRight
        if role == Qt.ForegroundRole:
            col = index.column()
            if index.column() == 1 or index.column() == 2:
                row = index.row()
                scr = self._data[row][4]
                if (scr > 0) :
                    return QtGui.QColor('red')
                else:
                   if (scr < 0) : return QtGui.QColor('blue')

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.header_text)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header_text[section]

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [])
            return True
        return False

    def addRow(self, newdata):
        self._data.append(newdata)

    #@QtCore.pyqtSlot(int, int, str)
    #def update_item(self, row, col, value):
    #    ix = self.index(row, col)
    #    self.setData(ix, value)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = KHOpenApi()
        self.kiwoom.ocx.OnEventConnect[int].connect(self.OnEventConnect)
        self.kiwoom.CommConnect()

        #data = []
        #header_text = ['종목코드', '종목명', '현재가', '상승율', '거래량']
        #self.table = QtWidgets.QTableView()
        #self.model = TableModel(data, header_text)
        #self.table.setModel(self.model)
        #self.model.addRow(['005930','삼성전자',0,0,0])
        #self.setCentralWidget(self.table)

        self.resize(430, 600)
        self.setWindowTitle("kiwoom realtime")



    def OnEventConnect(self, nErrCode):
        print("OnEventConnect received")
        if nErrCode == 0:
            # 연결 OK, 조건검색식 불러오기
            item_count = 0;
            data = []
            codes = self.kiwoom.GetCodeListByMarket(0).split(';')
            for x in codes:
                if len(x) > 0:
                    item_count += 1
                    data.append([
                        item_count,
                        x,
                        self.kiwoom.GetMasterCodeName(x),
                        int(self.kiwoom.GetMasterLastPrice(x)),
                        0,
                        0
                        ])
            kospi_count = len(data)
            print('kospi count = ', kospi_count)
            codes = self.kiwoom.GetCodeListByMarket(10).split(';')
            for x in codes:
                if len(x) > 0:
                    item_count += 1
                    data.append([
                        item_count,
                        x,
                        self.kiwoom.GetMasterCodeName(x),
                        int(self.kiwoom.GetMasterLastPrice(x)),
                        0,
                        0
                        ])
            kosdaq_count = len(data) - kospi_count
            print('kosdaq count = ', kosdaq_count)
            header_text = ['No', '종목코드', '종목명', '현재가', '상승율', '거래량']
            self.table = QtWidgets.QTableView()
            self.model = TableModel(data, header_text)
            self.table.setModel(self.model)
            self.setCentralWidget(self.table)

            pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
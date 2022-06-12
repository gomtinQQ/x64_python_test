# requirements
# pip install PyQt5
# pip install requests
# pip install websocket-client
# Save as UNICODE UTF-8 signature

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import requests
import websocket
import json

class ListenWebsocket(QtCore.QThread):
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)
        #websocket.enableTrace(True)

        self.WS = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                on_open = self.on_open,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close ) 

    def run(self):
        self.WS.run_forever()


    def on_open(self, ws):
        window.on_open(ws)

    def on_message(self, ws, message):
       window.on_message(ws, message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")


class SignalManager(QtCore.QObject):
    fooSignal = QtCore.pyqtSignal(int, int, str)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, mother):
        super(TableModel, self).__init__()
        self._data = data
        self.mother = mother
        self.column_text = ['코인명','현재가','전일대비','거래대금']

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
                scr = self.mother.snap_datas[row][2]
                if (scr > 0) :
                    return QtGui.QColor('red')
                else:
                   if (scr < 0) : return QtGui.QColor('blue')

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.column_text[section]

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [])
            return True
        return False

    @QtCore.pyqtSlot(int, int, str)
    def update_item(self, row, col, value):
        ix = self.index(row, col)
        self.setData(ix, value)


class MyProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, mother):
        super(MyProxyModel, self).__init__()
        self.mother = mother

    def lessThan(self, left, right):
        colIndex = left.column()
        left_val = self.mother.snap_datas[left.row()][colIndex]
        right_val = self.mother.snap_datas[right.row()][colIndex]
        if colIndex == 0:
            return left_val < right_val
        return left_val > right_val


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        all_items = requests.get('https://api.upbit.com/v1/market/all').json()
        self.dictno = {}
        self.snap_datas = []
        self.krw_names = []
        self.krw_codes = []
        array_index = 0
        for x in all_items:
            if x['market'][0:4] == 'KRW-':
                name = x['korean_name']
                code = x['market']
                self.krw_names.append(name)
                self.krw_codes.append(code)
                self.dictno[code] = array_index
                array_index += 1
                pass
            pass

        data = []
        for x in self.krw_names:
            data.append([x, '', '', ''])
            self.snap_datas.append([x,0,-1000,0])
            pass

        self.foo = SignalManager()

        self.table = QtWidgets.QTableView()
        self.model = TableModel(data, self)
        self.foo.fooSignal.connect(self.model.update_item)

        sortermodel = MyProxyModel(self)
        sortermodel.setSourceModel(self.model)
        sortermodel.setDynamicSortFilter(False)
        self.table.setModel(sortermodel)

        # enable sorting
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)

        self.resize(430, 600)
        self.setCentralWidget(self.table)
        self.setWindowTitle("upbit realtime")

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["ty"] == "ticker":
            code = data["cd"]
            tp = data['tp'];
            scr = data['scr']
            atp24h = data['atp24h']
            idx = self.dictno[code]
            if self.snap_datas[idx][2] != scr:
                self.snap_datas[idx][1] = tp
                self.snap_datas[idx][2] = scr
                int_tp = int(tp)
                if tp == float(int_tp):
                    self.foo.fooSignal.emit(idx, 1, '{:,}'.format(int_tp))
                else:
                    self.foo.fooSignal.emit(idx, 1, '{:,}'.format(tp))
                self.foo.fooSignal.emit(idx, 2, f'{scr:2.2%}')
            if self.snap_datas[idx][3] != atp24h:
                self.snap_datas[idx][3] = atp24h
                self.foo.fooSignal.emit(idx, 3, '{:,}백만'.format(int(atp24h/1000000+0.5)))

    def on_open(self, ws):
        data = [{
                "ticket": "test"
                }, {
                    "type": "ticker",
                    "codes": self.krw_codes
                }, {"format": "SIMPLE"}]
        ws.send(json.dumps(data))





app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
thread = ListenWebsocket()
thread.start()
app.exec_()

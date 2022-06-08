
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import requests
import websocket
import json

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    def flags(self, index):
        fl = super(self.__class__,self).flags(index)
        fl |= Qt.ItemIsEditable
        fl |= Qt.ItemIsSelectable
        fl |= Qt.ItemIsEnabled
        fl |= Qt.ItemIsDragEnabled
        fl |= Qt.ItemIsDropEnabled
        return fl

    def setData(self, row, col, value, role=Qt.EditRole):
        index = self.index(row, col)
        if index.isValid():
            self._data[row][col] = value
            self.dataChanged.emit(index, index, []) #, (Qt.DisplayRole, ))
            return True
        return False

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



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()
        all_items = requests.get('https://api.upbit.com/v1/market/all').json()
        self.dictno = {}
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
                array_index = array_index + 1
                pass
            pass

        data = []
        for x in self.krw_names:
            data.append([x, '', ''])
            pass

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


        self.thread = ListenWebsocket()
        self.thread.start()

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["ty"] == "ticker":
            code = data["cd"]
            self.model.setData(self.dictno[code], 1, str(data["tp"]))
            pass

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
app.exec_()

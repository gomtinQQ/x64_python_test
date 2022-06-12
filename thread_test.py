import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from multiprocessing import Queue
import threading
import pythoncom
from PyQt5.QAxContainer import *


class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI64.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveTrData.connect(self._handler_tr)
        print("Kiwoom Object", threading.current_thread().getName())

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        print("CommConnect", threading.current_thread().getName())

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def CommRqData(self, rqname, trcode, next, screen):
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)

    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()

    def _handler_login(self, err_code):
        print(err_code)
        print("로그인 완료")

    def _handler_tr(self, screen, rqname, trcode, record, next):
        종목코드 = self.GetCommData(trcode, rqname, 0, "종목코드")
        종목명 = self.GetCommData(trcode, rqname, 0, "종목명")
        print(종목코드, 종목명)
 

class Worker(QThread):
    def __init__(self, q):
        # 여기는 main thread에서 실행됨
        print("Worker: ", threading.current_thread().getName())
        super().__init__()
        self.q = q

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        print("run: ", threading.current_thread().getName())
        pythoncom.CoInitialize()

        self.kiwoom= Kiwoom()
        self.kiwoom.CommConnect()

        while True:
            if not self.q.empty():
                print("queue pop")
                data = self.q.get()
                self.request_tr(data)
                self.sleep(0.01)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()

    def request_tr(self, data):
        self.kiwoom.SetInputValue("종목코드", "005930")
        self.kiwoom.CommRqData("TR요청", "opt10001", 0, "1")
    

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # queue 
        #self.queue = Queue()
        #self.worker = Worker(self.queue)
        #self.worker.start()
        self.kiwoom= Kiwoom()
        self.kiwoom.CommConnect()

        self.btn = QPushButton("TR 요청", self)
        self.btn.clicked.connect(self.request_tr)

    def request_tr(self):
        data = "dummy"
        self.queue.put(data)
        print("queue push")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

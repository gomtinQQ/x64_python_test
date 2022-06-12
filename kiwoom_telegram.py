# ext librarys
# pip install PyQt5
# pip install requests
# Save as UNICODE UTF-8 signed

import sys
import configparser
import requests
import json
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QAxContainer import *
from PyQt5 import uic

from kiwoom.KHOpenApi import *

form_class = uic.loadUiType("main_window.ui")[0]



class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """
        OpenApi 이벤트 핸들 연결
        버튼 클릭 이벤트 핸들 연결
        ini파일에서 보관된 토큰, 챗아이디 불러오기
        """

        self.axWindow = KHOpenApi()
        self.axWindow.ocx.OnReceiveTrData[str, str, str, str, str, int, str, str, str].connect(self.OnReceiveTrData)
        self.axWindow.ocx.OnReceiveRealData[str, str, str].connect(self.OnReceiveRealData)
        self.axWindow.ocx.OnReceiveMsg[str, str, str, str].connect(self.OnReceiveMsg)
        self.axWindow.ocx.OnReceiveChejanData[str, int, str].connect(self.OnReceiveChejanData)
        self.axWindow.ocx.OnEventConnect[int].connect(self.OnEventConnect)
        self.axWindow.ocx.OnReceiveRealCondition[str, str, str, str].connect(self.OnReceiveRealCondition)
        self.axWindow.ocx.OnReceiveTrCondition[str, str, str, int, int].connect(self.OnReceiveTrCondition)
        self.axWindow.ocx.OnReceiveConditionVer[int, str].connect(self.OnReceiveConditionVer)

        self.btn_login.clicked.connect(self.btn_login_Clicked)
        self.btn_logout.clicked.connect(self.btn_logout_Clicked)
        self.btn_start.clicked.connect(self.btn_start_Clicked)
        self.btn_stop.clicked.connect(self.btn_stop_Clicked)

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        if self.config.has_section('telegram'):
            self.lineEdit_telegram_token.setText(self.config['telegram']['token'])
            self.lineEdit_telegram_chat_ID.setText(self.config['telegram']['chatID'])
            pass

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print("OnReceiveTrData received")

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        print("OnReceiveRealData  received")

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print("OnReceiveMsg received")

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        print("OnReceiveChejanData received")

    def OnEventConnect(self, nErrCode):
        print("OnEventConnect received")
        if nErrCode == 0:
            # 연결 OK, 조건검색식 불러오기
            self.axWindow.GetConditionLoad()
            pass

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        #print("OnReceiveRealCondition received")
        # 실시간 검색종목 전송
        if (self.act_condName == strConditionName):
            text = "실시간"
            if strType == "I":
                text += '편입: '
            else:
                text += '이탈: '
            text += strConditionName
            text += "\r\n[{code}] {name}\r\n".format(code=strCode, name=self.axWindow.ocx.GetMasterCodeName(strCode))
            self.send_telegram(text)
            pass

    def OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        """
        조건검색결과 리스트박스에 세팅, 텔레그램 전송
        """
        print("OnReceiveTrCondition received : " + strConditionName)
        code_list = strCodeList.split(';')
        names = []
        self.list_findItems.clear()
        for x in code_list:
            code_price = x.split('^')
            if len(code_price[0]):
                itemName = self.axWindow.GetMasterCodeName(code_price[0])
                self.list_findItems.addItem(itemName)
                names.append(itemName)
                pass
            pass
        find_count = len(names)
        self.label_findCount.setText(str(find_count))
        sned_text = "조건검색결과: {condname} ({count})\r\n".format(condname=strConditionName, count = find_count)
        for x in range(len(names)):
            sned_text += "[{code}] {name}\r\n".format(code=code_list[x], name=names[x])
            pass
        self.send_telegram(sned_text)

    def OnReceiveConditionVer(self, lRet, sMsg):
        """
        조건검색 목록 읽기, 콤보박스에 세팅
        """
        print("OnReceiveConditionVer received")
        self.cond_lists = self.axWindow.GetConditionNameList().split(';')
        self.comboBox_condList.clear()
        for x in self.cond_lists:
            name_index = x.split('^')
            if len(name_index) == 2:
                self.comboBox_condList.addItem(name_index[1])
                pass
            pass

    def btn_login_Clicked(self):
        """
        로그인 요청
        이미 로그인 되어있으면 패스
        """
        if self.axWindow.GetConnectState() != 1:
            self.axWindow.CommConnect()
            pass

    def btn_logout_Clicked(self):
        """
        로그아웃 요청
        로그인 되어 있는 경우에만 호출
        """
        tmStart = time.perf_counter_ns()
        ret = self.axWindow.GetFutureList()
        tmStop = time.perf_counter_ns()
        print(tmStart)
        print(ret)
        print(tmStop - tmStart)

        #if self.axWindow.GetConnectState() == 1:
        #    self.axWindow.CommTerminate()
        #    pass

    def btn_start_Clicked(self):
        """
        조건검색 요청
        1. 토큰과 챗아이디 보관
        2. SendCondition 호출
        """
        write_config = configparser.ConfigParser()
        write_config['telegram'] = {}
        write_config['telegram']['token'] = self.lineEdit_telegram_token.text()
        write_config['telegram']['chatID'] = self.lineEdit_telegram_chat_ID.text()
        with open('config.ini', 'w') as configfile:
            write_config.write(configfile)
        # 조건검색호출
        if self.axWindow.GetConnectState() == 1:
            name_index = self.cond_lists[self.comboBox_condList.currentIndex()].split('^')
            self.act_condName = name_index[1]
            self.act_condIndex = int(name_index[0])

            # 실시간 조건검색경우 마지막 변수를 1로 설정
            ret = self.axWindow.SendCondition("2001", self.act_condName, self.act_condIndex, 0)
            if ret == 1:
                self.btn_start.setEnabled(False)
                self.btn_stop.setEnabled(True)
            else:
                print(self.act_condName + " : 요청실패")
            pass

    def btn_stop_Clicked(self):
        """
        조건검색 중지
        SendConditionStop 호출, 텔레그램 검색중지 메시지 전송
        """
        self.axWindow.SendConditionStop("2001", self.act_condName, self.act_condIndex)
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.send_telegram("검색중지 : " + self.act_condName)

    def send_telegram(self, text):
        """
        텔레그램 전송
        POST모드 요청
        """
        token = self.lineEdit_telegram_token.text()
        chat_id = self.lineEdit_telegram_chat_ID.text()
        URL = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=token)
        data = {'chat_id' : chat_id,
                'text' : text
            }
        data_json = json.dumps(data).encode()
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(URL, headers=headers, data=data_json)
        if response.status_code != 200:
            print(URL)
            print(response)
            pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


# Save as UNICODE UTF-8 signed

import sys
from PyQt5.QAxContainer import QAxWidget


class KHOpenApi(object):
    """description of class"""
    def __init__(self):
        super().__init__()
        if sys.maxsize > 2**32:
            prog_id = "KHOPENAPI64.KHOpenAPICtrl.1"
        else:
            prog_id = "KHOPENAPI.KHOpenAPICtrl.1"

        self.ocx = QAxWidget(prog_id)

    def CommConnect(self) -> int:
        return self.ocx.dynamicCall("CommConnect()")

    def CommTerminate(self):
        self.ocx.dynamicCall("CommTerminate()")

    def CommRqData(self, sRQName, sTrCode, nPrevNext, sScreenNo) -> int:
        return self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)

    def GetLoginInfo(self, sTag) -> str:
        return self.ocx.dynamicCall("GetLoginInfo(QString)", sTag)

    def SendOrder(self, sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo) -> int:
        return self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                    [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo])

    def SendOrderFO(self, sRQName, sScreenNo, sAccNo, sCode, lOrdKind, sSlbyTp, sOrdTp, lQty, sPrice, sOrgOrdNo) -> int:
        return self.ocx.dynamicCall("SendOrderFO(QString, QString, QString, QString, int, QString, QString, int, QString, QString)",
                                    [sRQName, sScreenNo, sAccNo, sCode, lOrdKind, sSlbyTp, sOrdTp, lQty, sPrice, sOrgOrdNo])

    def SetInputValue(self, sID, sValue):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def SetOutputFID(self, sID) -> int:
        return self.ocx.dynamicCall("SetOutputFID(QString)", sID)

    def CommGetData(self, sJongmokCode, sRealType, sFieldName, nIndex, sInnerFieldName) -> str:
        return self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sJongmokCode, sRealType,
                                    sFieldName, nIndex, sInnerFieldName)

    def DisconnectRealData(self, sScnNo):
        self.ocx.dynamicCall("DisconnectRealData(QString)", sScnNo)

    def GetRepeatCnt(self, sTrCode, sRecordName) -> int:
        return self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRecordName)

    def CommKwRqData(self, sArrCode, bNext, nCodeCount, nTypeFlag, sRQName, sScreenNo) -> int:
        return self.ocx.dynamicCall("CommKwRqData(QString, int, int, int, QString, QString)",
                                    sArrCode, bNext, nCodeCount, nTypeFlag, sRQName, sScreenNo)

    def GetAPIModulePath(self) -> str:
        return self.ocx.dynamicCall("GetAPIModulePath()")

    def GetCodeListByMarket(self, sMarket) -> str:
        return self.ocx.dynamicCall("GetCodeListByMarket(QString)", [sMarket])

    def GetConnectState(self) -> int:
        return self.ocx.dynamicCall("GetConnectState()")

    def GetMasterCodeName(self, strCode) -> str:
        return self.ocx.dynamicCall("GetMasterCodeName(QString)", strCode)

    def GetMasterListedStockCnt(self, strCode) -> int:
        return self.ocx.dynamicCall("GetMasterListedStockCnt(QString)", strCode)

    def GetMasterConstruction(self, strCode) -> str:
        return self.ocx.dynamicCall("GetMasterConstruction(QString)", strCode)

    def GetMasterListedStockDate(self, strCode) -> str:
        return self.ocx.dynamicCall("GetMasterListedStockDate(QString)", strCode)

    def GetMasterLastPrice(self, strCode) -> str:
        return self.ocx.dynamicCall("GetMasterLastPrice(QString)", strCode)

    def GetMasterStockState(self, strCode) -> str:
        return self.ocx.dynamicCall("GetMasterStockState(QString)", strCode)

    def GetDataCount(self, strRecordName) -> int:
        return self.ocx.dynamicCall("GetDataCount(QString)", strRecordName)

    def GetOutputValue(self, strRecordName, nRepeatIdx, nItemIdx) -> str:
        return self.ocx.dynamicCall("GetOutputValue(QString, int, int)", strRecordName, nRepeatIdx, nItemIdx)

    def GetCommData(self, strTrCode, strRecordName, nIndex, strItemName) -> str:
        return self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)",
                                    strTrCode, strRecordName, nIndex, strItemName)

    def GetCommRealData(self, strCode, nFid) -> str:
        return self.ocx.dynamicCall("GetCommRealData(QString, int)", strCode, nFid)

    def GetChejanData(self, nFid) -> str:
        return self.ocx.dynamicCall("GetChejanData(int)", nFid)

    def GetThemeGroupList(self, nType) -> str:
        return self.ocx.dynamicCall("GetThemeGroupList(int)", nType)

    def GetThemeGroupCode(self, strThemeCode) -> str:
        return self.ocx.dynamicCall("GetThemeGroupCode(QString)", strThemeCode)

    def GetFutureList(self) -> str:
        return self.ocx.dynamicCall("GetFutureList()")

    def GetFutureCodeByIndex(self, nIndex) -> str:
        return self.ocx.dynamicCall("GetFutureCodeByIndex(int)", nIndex)

    def GetActPriceList(self) -> str:
        return self.ocx.dynamicCall("GetActPriceList()")

    def GetMonthList(self) -> str:
        return self.ocx.dynamicCall("GetMonthList()")

    def GetOptionCode(self, strActPrice, nCp, strMonth) -> str:
        return self.ocx.dynamicCall("GetOptionCode(QString, int, QString)", strActPrice, nCp, strMonth)

    def GetOptionCodeByMonth(self, sTrCode, nCp, strMonth) -> str:
        return self.ocx.dynamicCall("GetOptionCodeByMonth(QString, int, QString)", sTrCode, nCp, strMonth)

    def GetOptionCodeByActPrice(self, sTrCode, nCp, nTick) -> str:
        return self.ocx.dynamicCall("GetOptionCodeByActPrice(QString, int, int)", sTrCode, nCp, nTick)

    def GetSFutureList(self, strBaseAssetCode) -> str:
        return self.ocx.dynamicCall("GetSFutureList(QString)", strBaseAssetCode)

    def GetSFutureCodeByIndex(self, strBaseAssetCode, nIndex) -> str:
        return self.ocx.dynamicCall("GetSFutureCodeByIndex(QString, int)", strBaseAssetCode, nIndex)

    def GetSActPriceList(self, strBaseAssetGb) -> str:
        return self.ocx.dynamicCall("GetSActPriceList(QString)", strBaseAssetGb)

    def GetSMonthList(self, strBaseAssetGb) -> str:
        return self.ocx.dynamicCall("GetSMonthList(QString)", strBaseAssetGb)

    def GetSOptionCode(self, strBaseAssetGb, strActPrice, nCp, strMonth) -> str:
        return self.ocx.dynamicCall("GetSOptionCode(QString, QString, int, QString)", strBaseAssetGb, strActPrice, nCp, strMonth)

    def GetSOptionCodeByMonth(self, strBaseAssetGb, sTrCode, nCp, strMonth) -> str:
        return self.ocx.dynamicCall("GetSOptionCodeByMonth(QString, QString, int, QString)", strBaseAssetGb, sTrCode, nCp, strMonth)

    def GetSOptionCodeByActPrice(self, strBaseAssetGb, sTrCode, nCp, nTick) -> str:
        return self.ocx.dynamicCall("GetSOptionCodeByActPrice(QString, QString, int, int)", strBaseAssetGb, sTrCode, nCp, nTick)

    def GetSFOBasisAssetList(self) -> str:
        return self.ocx.dynamicCall("GetSFOBasisAssetList()")

    def GetOptionATM(self) -> str:
        return self.ocx.dynamicCall("GetOptionATM()")

    def GetSOptionATM(self, strBaseAssetGb) -> str:
        return self.ocx.dynamicCall("GetSOptionATM(QString)", strBaseAssetGb)

    def GetBranchCodeName(self) -> str:
        return self.ocx.dynamicCall("GetBranchCodeName()")

    def CommInvestRqData(self, sMarketGb, sRQName, sScreenNo) -> int:
        return self.ocx.dynamicCall("CommInvestRqData(QString, QString, QString)", sMarketGb, sRQName, sScreenNo)

    def SendOrderCredit(self, sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sCreditGb, sLoanDate, sOrgOrderNo) -> int:
        return self.ocx.dynamicCall("SendOrderCredit(QString, QString, QString, int, QString, int, int, QString, QString, QString, QString)",
                                    [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sCreditGb, sLoanDate, sOrgOrderNo])

    def KOA_Functions(self, sFunctionName, sParam) -> str:
        return self.ocx.dynamicCall("KOA_Functions(QString, QString)", sFunctionName, sParam)

    def SetInfoData(self, sInfoData) -> int:
        self.ocx.dynamicCall("SetInfoData(QString)", sInfoData)

    def SetRealReg(self, strScreenNo, strCodeList, strFidList, strOptType) -> int:
        return self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", strScreenNo, strCodeList, strFidList, strOptType)

    def GetConditionLoad(self) -> int:
        return self.ocx.dynamicCall("GetConditionLoad()")

    def GetConditionNameList(self) -> str:
        return self.ocx.dynamicCall("GetConditionNameList()")

    def SendCondition(self, strScrNo, strConditionName, nIndex, nSearch) -> int:
        return self.ocx.dynamicCall("SendCondition(QString,QString, int, int)", strScrNo, strConditionName, nIndex, nSearch)

    def SendConditionStop(self, strScrNo, strConditionName, nIndex):
        self.ocx.dynamicCall("SendConditionStop(QString, QString, int)", strScrNo, strConditionName, nIndex)

    def GetCommDataEx(self, strTrCode, strRecordName):
        return self.ocx.dynamicCall("GetCommDataEx(QString, QString)", strTrCode, strRecordName)

    def SetRealRemove(self, strScrNo, strDelCode):
        self.ocx.dynamicCall("SetRealRemove(QString, QString)", strScrNo, strDelCode)

    def GetMarketType(self, sTrCode) -> int:
        return self.ocx.dynamicCall("GetMarketType(QString, QString)", sTrCode)


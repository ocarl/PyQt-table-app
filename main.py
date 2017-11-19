import sys
import os
from PyQt5.QtWidgets import *
from xml.dom.minidom import *
from dicttoxml import dicttoxml


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Position handler'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200
        self.rowCount = 0
        self.labels = ['Name', 'Position', 'Currency', 'Issuer', 'Price', 'Acquirer', 'Counterparty', 'Total']

        self.instrumentList = []

        self.initUI()
        self.dataLoadable = True

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 101*(len(self.labels)+1)+5, self.height)

        self.background = QMainWindow()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.background)
        self.setLayout(self.layout)

        self.createUI()
        self.show()

    def createUI(self):
        self.createTable()
        self.createButtons()
        self.handleLayout()

    def handleLayout(self):
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.button1)
        self.layout2.addWidget(self.button2)
        self.layout2.addWidget(self.button3)

    def createButtons(self):
        self.button1 = QPushButton('Create Instrument', self)
        self.button2 = QPushButton('Trade Instruments', self)
        self.button3 = QPushButton('Load Instruments', self)
        self.button1.setStyleSheet("background-color:rgb(140,199,66); color: white")
        self.button2.setStyleSheet("background-color:rgb(140,199,66); color: white")
        self.button3.setStyleSheet("background-color:rgb(140,199,66); color: white")
        self.button1.move(0, 0)
        self.button2.move(0, 30)
        self.button3.move(0, 60)
        self.button1.clicked.connect(self.createInstrument)
        self.button2.clicked.connect(self.tradeInstruments)
        self.button3.clicked.connect(self.loadData)

    def createTable(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(self.rowCount)
        self.tableWidget.setColumnCount(len(self.labels))
        self.tableWidget.setHorizontalHeaderLabels(self.labels)
        self.tableWidget.setGeometry(self.left + 60, self.top, 90 * (len(self.labels) + 1) + 9, self.height)
        self.tableWidget.move(100, 0)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.show()

    def addRowInTable(self):
        self.rowCount += 1
        self.createUI()

    def createInstrument(self):
        self.instrumentWindow = QWidget()
        self.instrumentWindow.setWindowTitle('New Instrument')
        self.createInstrumentBoxes()
        self.handleLayoutInstrument()
        self.createDoneButton()
        self.instrumentWindow.show()

    def createDoneButton(self):
        self.doneButton = QPushButton('Add', self.instrumentWindow)
        self.textBoxLayout.addWidget(self.doneButton)
        self.doneButton.clicked.connect(self.writeNewInstrument)
        self.doneButton.clicked.connect(self.instrumentWindow.close)

    def createInstrumentBoxes(self):
        self.instrumentNameBox = QLineEdit(self.instrumentWindow)
        self.instrumentPosBox = QLineEdit(self.instrumentWindow)
        self.instrumentCurrencyBox = QLineEdit(self.instrumentWindow)
        self.instrumentIssuerBox = QLineEdit(self.instrumentWindow)
        self.instrumentPricsBox = QLineEdit(self.instrumentWindow)
        self.instrumentCounterPartyBox = QLineEdit(self.instrumentWindow)
        self.instrumentAcquirerBox = QLineEdit(self.instrumentWindow)
        self.instrumentNameBox.setPlaceholderText('Name')
        self.instrumentPosBox.setPlaceholderText('Position')
        self.instrumentCurrencyBox.setPlaceholderText('Currency')
        self.instrumentIssuerBox.setPlaceholderText('Issuer')
        self.instrumentPricsBox.setPlaceholderText('Price')
        self.instrumentCounterPartyBox.setPlaceholderText('Counterparty')
        self.instrumentAcquirerBox.setPlaceholderText('Acquirer')

    def handleLayoutInstrument(self):
        self.textBoxLayout = QVBoxLayout(self.instrumentWindow)
        self.textBoxLayout.addWidget(self.instrumentNameBox)
        self.textBoxLayout.addWidget(self.instrumentPosBox)
        self.textBoxLayout.addWidget(self.instrumentCurrencyBox)
        self.textBoxLayout.addWidget(self.instrumentIssuerBox)
        self.textBoxLayout.addWidget(self.instrumentPricsBox)
        self.textBoxLayout.addWidget(self.instrumentCounterPartyBox)
        self.textBoxLayout.addWidget(self.instrumentAcquirerBox)

    def writeNewInstrument(self):
        self.addRowInTable()
        self.instrumentList.append(generateInstrument(self.instrumentNameBox.text(), self.instrumentPosBox.text(),
                                                      self.instrumentCurrencyBox.text(), self.instrumentIssuerBox.text(),
                                                      self.instrumentPricsBox.text(), self.instrumentAcquirerBox.text(),
                                                      self.instrumentCounterPartyBox.text()))
        for row, instr in enumerate(self.instrumentList):
            for col, text in enumerate(self.labels):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(instr[text])))

    def loadData(self):
        # load data from previous session that has been stored as an xml
        if self.dataLoadable:
            for dirFile in os.listdir('.'):
                valList = []
                if '.xml' in dirFile:
                    self.addRowInTable()
                    xmlInfo = parse(dirFile)
                    for lab in self.labels:
                        valList.append(xmlInfo.getElementsByTagName(lab)[0].firstChild.data)
                    self.instrumentList.append(dict(zip(self.labels, valList)))

            self.updateTable()
            self.dataLoadable = False

    def updateTable(self):
        for row, instr in enumerate(self.instrumentList):
            for col, text in enumerate(self.labels):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(instr[text])))

    def closeEvent(self, event):
        # this overwrites the default behavior of QMainWindow to save the instruments at close
        # and close all other windows
        for instr in self.instrumentList:
            dom = parseString(dicttoxml(instr))
            with open('{}.xml'.format(instr['Name']), 'w') as fid:
                dom.writexml(fid)
        try:
            self.instrumentWindow.close()
        except AttributeError:
            pass
        try:
            self.tradeWindow.close()
        except AttributeError:
            pass

    def tradeInstruments(self):
        self.initiateTradeWindow()
        self.handleTradeLayout()

        # add instruments to
        for instr in self.instrumentList:
            self.whichInstrument.addItem(instr['Name'])

        self.tradeWindow.show()

    def initiateTradeWindow(self):
        self.tradeWindow = QWidget()
        self.tradeWindow.setWindowTitle('Trade')
        self.tradeWindow.setGeometry(300, 300, 100, 30)
        self.whichInstrument = QComboBox(self.tradeWindow)
        self.chooseAction = QComboBox(self.tradeWindow)
        self.chooseAction.addItem('Buy')
        self.chooseAction.addItem('Sell')
        self.goBtn = QPushButton('Go!', self.tradeWindow)
        self.goBtn.clicked.connect(self.doTrade)
        self.goBtn.clicked.connect(self.tradeWindow.close)
        self.instrQuant = QLineEdit(self.tradeWindow)
        self.instrQuant.setPlaceholderText('Quantity')

    def handleTradeLayout(self):
        tradeLayout = QHBoxLayout(self.tradeWindow)
        tradeLayout.addWidget(self.whichInstrument)
        tradeLayout.addWidget(self.chooseAction)
        tradeLayout.addWidget(self.instrQuant)
        tradeLayout.addWidget(self.goBtn)

    def doTrade(self):
        self.instrumentList = trader(self.instrumentList, self.whichInstrument.currentText(),
                                     self.chooseAction.currentText(), self.instrQuant.text())
        self.updateTable()


def generateInstrument(name, position, currency, issuer, price, acquirer, counterParty):

    instrumentDict = {}

    instrumentDict['Name'] = name
    instrumentDict['Position'] = position
    instrumentDict['Currency'] = currency
    instrumentDict['Issuer'] = issuer
    instrumentDict['Price'] = price
    instrumentDict['Acquirer'] = acquirer
    instrumentDict['Counterparty'] = counterParty
    instrumentDict['Total'] = float(price)*int(position)

    return instrumentDict


def trader(allInstr, instr, action, quant):

    currInstr = None
    currIndex = None

    currIndex, currInstr = findInstrumentToTrade(allInstr, currIndex, currInstr, instr)

    actionDict = {
        'Buy': lambda x, y: int(x['Position']) + int(y),
        'Sell': lambda x, y: int(x['Position']) - int(y)
    }

    # do the trade
    currInstr['Position'] = actionDict[action](currInstr, quant)
    allInstr[currIndex] = currInstr

    return allInstr


def findInstrumentToTrade(allInstr, currInd, currInstr, instr):
    for i, instrInd in enumerate(allInstr):
        if instrInd['Name'] == instr:
            currInstr = instrInd
            currInd = i
    return currInd, currInstr


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
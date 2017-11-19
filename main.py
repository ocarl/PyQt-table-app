import sys
from PyQt5.QtWidgets import *
from xml.etree import ElementTree as ET
from xml.dom.minidom import *
from dicttoxml import dicttoxml


class App(QWidget):
    def __init__(self, labels, instrumentList = []):
        super().__init__()
        self.title = 'Position handler'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200
        self.rowCount = 0
        self.labels = labels

        self.instrumentList = instrumentList

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 101*(len(self.labels)+1), self.height)

        self.createBackground()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.background)
        self.setLayout(self.layout)

        self.createUI()

        # Add box layout, add table to box layout and add box layout to widget


        # Show widget
        self.show()

    def createBackground(self):
        self.background = QMainWindow()

    def createUI(self):
        # Create table
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(self.rowCount)
        self.tableWidget.setColumnCount(len(self.labels))
        self.tableWidget.setHorizontalHeaderLabels(self.labels)
        self.tableWidget.setGeometry(self.left+60, self.top, 90*(len(self.labels)+1), self.height)
        self.tableWidget.move(100, 0)

        self.tableWidget.setSortingEnabled(True)

        self.tableWidget.setAlternatingRowColors(True)


        self.tableWidget.show()

        self.layout2 = QVBoxLayout()

        self.button1 = QPushButton('Create Instrument', self)
        self.button2 = QPushButton('Trade Instruments', self)
        self.button3 = QPushButton('Load Instruments', self)

        self.button1.setStyleSheet("background-color:rgb(140,199,66); color: white")
        self.button2.setStyleSheet("background-color:rgb(140,199,66); color: white")
        self.button3.setStyleSheet("background-color:rgb(140,199,66); color: white")

        self.layout2.addWidget(self.button1)
        self.layout2.addWidget(self.button2)
        self.layout2.addWidget(self.button3)

        self.button1.move(0, 0)
        self.button2.move(0, 30)
        self.button3.move(0, 60)

        self.button1.clicked.connect(self.createInstrument)
        self.button2.clicked.connect(self.tradeInstruments)
        self.button3.clicked.connect(self.loadData)

    def addRowInTable(self):
        self.rowCount += 1
        self.createUI()

    def createInstrument(self):
        self.instrumentWindow = QWidget()
        self.instrumentWindow.setWindowTitle('New Instrument')

        self.instrumentNameBox = QLineEdit('Name', self.instrumentWindow)
        self.instrumentPosBox = QLineEdit('Position', self.instrumentWindow)
        self.instrumentCurrencyBox = QLineEdit('Currency', self.instrumentWindow)
        self.instrumentIssuerBox = QLineEdit('Issuer', self.instrumentWindow)
        self.instrumentPricsBox = QLineEdit('Price', self.instrumentWindow)
        self.instrumentCounterPartyBox = QLineEdit('Counterparty', self.instrumentWindow)
        self.instrumentAcquirerBox = QLineEdit('Acquirer', self.instrumentWindow)

        textBoxLayout = QVBoxLayout(self.instrumentWindow)
        textBoxLayout.addWidget(self.instrumentNameBox)
        textBoxLayout.addWidget(self.instrumentPosBox)
        textBoxLayout.addWidget(self.instrumentCurrencyBox)
        textBoxLayout.addWidget(self.instrumentIssuerBox)
        textBoxLayout.addWidget(self.instrumentPricsBox)
        textBoxLayout.addWidget(self.instrumentCounterPartyBox)
        textBoxLayout.addWidget(self.instrumentAcquirerBox)

        self.doneButton = QPushButton('Add', self.instrumentWindow)
        textBoxLayout.addWidget(self.doneButton)

        self.doneButton.clicked.connect(self.writeNewInstrument)
        self.doneButton.clicked.connect(self.instrumentWindow.close)

        self.instrumentWindow.show()

    def writeNewInstrument(self):
        self.addRowInTable()
        self.instrumentList.append(generateInstrument(self.instrumentNameBox.text(), self.instrumentPosBox.text(), self.instrumentCurrencyBox.text(),
                                                      self.instrumentIssuerBox.text(), self.instrumentPricsBox.text(),
                                                      self.instrumentAcquirerBox.text(), self.instrumentCounterPartyBox.text()))
        for i, instr in enumerate(self.instrumentList):
            for j, text in enumerate(self.labels):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(instr[text])))


    def loadData(self):
        for i in range(len(self.instrumentList)):
            self.addRowInTable()
        self.updateTable()

    def updateTable(self):
        for i, instr in enumerate(self.instrumentList):
            for j, text in enumerate(self.labels):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(instr[text])))

    def closeEvent(self, event):
        for instr in self.instrumentList:
            dom = parseString(dicttoxml(instr))
            with open('{}.xml'.format(instr['Name']), 'w') as fid:
                dom.writexml(fid)

    def tradeInstruments(self):
        self.tradeWindow = QWidget()
        self.tradeWindow.setWindowTitle('Trade')
        self.tradeWindow.setGeometry(300,300,100,30)

        self.whichInstrument = QComboBox(self.tradeWindow)
        self.chooseAction = QComboBox(self.tradeWindow)

        for instr in self.instrumentList:
            self.whichInstrument.addItem(instr['Name'])

        self.chooseAction.addItem('Buy')
        self.chooseAction.addItem('Sell')

        self.instrQuant = QLineEdit('How Many?', self.tradeWindow)

        goBtn = QPushButton('Go!', self.tradeWindow)

        tradeLayout = QHBoxLayout(self.tradeWindow)
        tradeLayout.addWidget(self.whichInstrument)
        tradeLayout.addWidget(self.chooseAction)
        tradeLayout.addWidget(self.instrQuant)
        tradeLayout.addWidget(goBtn)

        goBtn.clicked.connect(self.doTrade)

        self.tradeWindow.show()

    def doTrade(self):
        # trader(self.whichInstrument.activated(0), self.chooseAction.activated(0), self.instrQuant.text)
        self.instrumentList = trader(self.instrumentList, self.whichInstrument.currentText(), self.chooseAction.currentText(), self.instrQuant.text())
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
    currInd = None

    for i, instrInd in enumerate(allInstr):
        if instrInd['Name'] == instr:
            currInstr = instrInd
            currInd = i

    actionDict = {
        'Buy': lambda x, y: int(x['Position']) + y,
        'Sell': lambda x, y: int(x['Position']) - y
    }

    currInstr['Position'] = actionDict[action](currInstr, int(quant))

    allInstr[currInd] = currInstr

    return allInstr


if __name__ == '__main__':
    import os

    labels = ['Name', 'Position', 'Currency', 'Issuer', 'Price', 'Acquirer', 'Counterparty', 'Total']

    inputList = []

    for dirFile in os.listdir('.'):
        valList = []
        if '.xml' in dirFile:
            xmlInfo = parse(dirFile)
            for lab in labels:
                valList.append(xmlInfo.getElementsByTagName(lab)[0].firstChild.data)
            inputList.append(dict(zip(labels, valList)))



    app = QApplication(sys.argv)
    ex = App(labels, inputList)
    sys.exit(app.exec_())
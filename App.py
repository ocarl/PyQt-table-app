import os
from PyQt5.QtWidgets import *
from xml.dom.minidom import *
from dicttoxml import dicttoxml
from WidgetSingleton import WidgetSingleton
from Instrument import *

class App(WidgetSingleton, QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Position handler'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200
        self.rowCount = 0
        self.labels = ['ID', 'Name', 'Position', 'Currency', 'Issuer', 'Price', 'Acquirer', 'Counterparty', 'Total']

        self.instrumentDictList = []
        self.instrumentInstanceList = Instrument.allInstrumentsList

        self.initUI()
        self.dataLoadable = True

    def populateInstrumentlist(self):
        self.instrumentDictList.clear()
        for instr in Instrument.allInstrumentsList:
            self.instrumentDictList.append(instr.getDict())

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
        self.instrumentInstanceList.append(createInstrument(self.instrumentNameBox.text(), self.instrumentPosBox.text(),
                                                      self.instrumentCurrencyBox.text(), self.instrumentIssuerBox.text(),
                                                      self.instrumentPricsBox.text(), self.instrumentAcquirerBox.text(),
                                                      self.instrumentCounterPartyBox.text()))
        self.instrumentDictList.append(self.instrumentInstanceList[-1].getDict())
        for row, instr in enumerate(self.instrumentDictList):
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
                    self.instrumentDictList.append(dict(zip(self.labels, valList)))
                    createInstrument(*valList[1:-1])

            self.updateTable()
            self.dataLoadable = False

    def updateTable(self):
        self.populateInstrumentlist()
        for row, instr in enumerate(self.instrumentDictList):
            for col, text in enumerate(self.labels):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(instr[text])))

    def closeEvent(self, event):
        # this overwrites the default behavior of QMainWindow to save the instruments at close
        # and close all other windows
        for instr in self.instrumentDictList:
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
        self.populateInstrumentlist()
        self.initiateTradeWindow()
        self.handleTradeLayout()
        self.tradeWindow.show()

    def initiateTradeWindow(self):
        self.tradeWindow = QWidget()
        self.tradeWindow.setWindowTitle('Trade')
        self.tradeWindow.setGeometry(300, 300, 100, 30)
        self.whichInstrument = QComboBox(self.tradeWindow)
        for instr in self.instrumentDictList:
            self.whichInstrument.addItem('{} ({})'.format(instr['Name'], str(instr['ID'])))
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
        # find instrument with id that matches name
        for instr in self.instrumentInstanceList:
            if instr.getID() in self.whichInstrument.currentText():
                if self.chooseAction.currentText() == 'Buy':
                    instr.updatePosition(int(self.instrQuant.text()))
                elif self.chooseAction.currentText() == 'Sell':
                    instr.updatePosition(-int(self.instrQuant.text()))
        self.updateTable()



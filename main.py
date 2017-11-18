import sys
from PyQt5.QtWidgets import *
from xml.etree import ElementTree as ET

class App(QWidget):
    def __init__(self, instrumentList = []):
        super().__init__()
        self.title = 'Position handler'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 200
        self.rowCount = 0
        self.labels = ['Name', 'Position', 'Currency', 'Issuer', 'Price', 'Acquirer', 'Counterparty', 'Total']

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
        self.button3 = QPushButton('C', self)

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
        self.button3.clicked.connect(self.on_click)

    def tradeInstruments(self):
        self.tradeWindow = QWidget()
        self.tradeWindow.setWindowTitle('Trade')
        self.tradeWindow.setGeometry(300,300,100,30)

        whichInstrument = QComboBox(self.tradeWindow)

        for instr in self.instrumentList:
            whichInstrument.addItem(instr['Name'])

        instrQuant = QTextEdit('How Many?', self.tradeWindow)

        tradeLayout = QHBoxLayout(self.tradeWindow)
        tradeLayout.addWidget(whichInstrument)
        tradeLayout.addWidget(instrQuant)

        self.tradeWindow.show()

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


    def on_click(self):
        pass

    def closeEvent(self, event):

        root = ET.Element("root")
        doc = ET.SubElement(root, "doc")

        ET.SubElement(doc, "field1", name="blah").text = "some value1"
        ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

        tree = ET.ElementTree(root)
        tree.write("filename.xml")
        if can_exit:
            event.accept()  # let the window close
        else:
            event.ignore()

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

def trader():
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
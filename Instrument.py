class Instrument(object):
    allInstrumentsList = []

    def __init__(self, name, position, currency, issuer, price, acquirer, counterParty):
        self.name = name
        self.position     = int(position)
        self.currency     = currency
        self.issuer       = issuer
        self.price        = price
        self.acquirer     = acquirer
        self.counterParty = counterParty
        self.id           = id(self)
        self.total        = self.calcTotal()
        self.allInstrumentsList.append(self)

    def calcTotal(self):
        return float(self.price) * int(self.position)

    def updatePosition(self, amount):
        self.position += amount

    def getDict(self):
        return {'ID': self.id, 'Name': self.name, 'Position': self.position, 'Currency': self.currency,
                'Issuer': self.issuer, 'Price': self.price, 'Acquirer': self.acquirer,
                'Counterparty': self.counterParty, 'Total': self.total}

    def getID(self):
        return str(self.id)

def createInstrument(name, position, currency, issuer, price, acquirer, counterParty):
    return Instrument(name, position, currency, issuer, price, acquirer, counterParty)

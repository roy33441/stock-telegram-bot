class Company:
    def __init__(self, name):
        self.name = name
        self.ma20 = None
        self.ma50 = None
        self.ask = None
        self.ma20Passma50 = False
        self.ma20PassAsk = False
        self.ma50PassAsk = False


COMPANIES = {'AAPL': Company('AAPL'), 'MSFT': Company('MSFT'),
             'GOOG': Company('GOOG'), 'TSLA': Company('TSLA'), 'META': Company('META')}

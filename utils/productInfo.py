class ProductInfo():
    def __init__(self, barCode, name, price, expirationDate, brand, sales = False, salePercentage = 10):
        self.initVariables(barCode, name, price, expirationDate, brand, sales, salePercentage)

    def initVariables(self, barCode, name, price, expirationDate, brand, sales, salePercentage):
        self.barCode = barCode
        self.name = name
        self.price = price
        self.expirationDate = expirationDate
        self.brand = brand
        self.sales = sales
        self.salePercentage = salePercentage
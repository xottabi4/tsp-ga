class City:

    def __init__(self, name, xCoordinate, yCoordinate):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate

    def print(self):
        print(self.name, self.xCoordinate, self.yCoordinate)

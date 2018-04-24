import sys
from math import sqrt

from matplotlib import pyplot as plt


class Path:
    distance = sys.maxsize
    cities = []

    def __init__(self, cities):
        self.cities = cities
        if cities:
            self.distance = self.calculateTotalDistance()

    def calculateTotalDistance(self):
        totalDistance = 0
        for i, j in zip(self.cities, self.cities[1:]):
            totalDistance += sqrt(pow(i.xCoordinate - j.xCoordinate, 2) + pow(i.yCoordinate - j.yCoordinate, 2))
        return totalDistance

    def print(self):
        names = list(map((lambda x: x.name), self.cities))
        print(names)

    def plotPath(self):
        x = list(map((lambda x: x.xCoordinate), self.cities))
        y = list(map((lambda y: y.yCoordinate), self.cities))
        solutionPlot = plt.figure(1)
        plt.plot(x, y, '.r-')
        plt.scatter(self.cities[0].xCoordinate, self.cities[0].yCoordinate)
        solutionPlot.show()

import random
from math import floor, ceil
from random import shuffle

from src.ga.Path import Path


class Population:
    bestPath = None
    _pathes = []
    cityCount = 0

    def __init__(self, startingCity, inputCities, populationSize):
        self.cityCount = len(inputCities) + 2
        self.generateInitialPopulation(startingCity, inputCities, populationSize)
        self.bestPath = Path([])

    def generateInitialPopulation(self, startingCity, inputCities, populationSize):
        for i in range(0, populationSize):
            cityOrder = []
            cityOrder.extend(inputCities)
            shuffle(cityOrder)
            cityOrder.insert(0, startingCity)
            cityOrder.append(startingCity)

            path = Path(cityOrder)
            self._pathes.append(path)

    def evolve(self, mutationRate=0):
        # Create next population
        self._pathes = self._performCrossover()
        if mutationRate != 0:
            self._mutate(mutationRate)
        self._updateBestPath()

        # print(len(self._pathes))
        # for path in self._pathes:
        #     for city in path.cities:
        #         city.print()
        # print(len(path.cities))

    def _performCrossover(self):
        newPathes = []

        # opulation in 10 % chunks
        # chunkSize = 10
        chunkSize = 12
        bestCount = int(chunkSize / 2)

        chunks = list(self._splitIntoChunks(self._pathes, chunkSize))

        if len(chunks[-1]) < chunkSize:
            lastChunk = chunks[-1]
            newPathes.extend(lastChunk)
            chunks = chunks[:-1]

        for chunk in chunks:
            chunk.sort(key=lambda x: x.distance, reverse=False)
            bestOfChunk = chunk[0:bestCount]
            firstHalf = bestOfChunk[0:floor(bestCount / 2)]
            secondHalf = bestOfChunk[ceil(bestCount / 2):]

            firstHalfCopy = list(firstHalf)
            secondHalfCopy = list(secondHalf)
            firstHalfCopy.sort(key=lambda x: x.distance, reverse=True)
            secondHalfCopy.sort(key=lambda x: x.distance, reverse=False)
            firstHalf.extend(firstHalfCopy)
            secondHalf.extend(secondHalfCopy)

            for firstPath, secondPath in zip(firstHalf, secondHalf):
                newPathes.append(self._createChild(firstPath, secondPath))
                newPathes.append(self._createChild(secondPath, firstPath))

            if bestCount % 2 != 0:
                # for firstPath in firstHalf:
                #     for secondPath in secondHalf:
                #         newPathes.append(self._createChild(firstPath, secondPath))
                #         newPathes.append(self._createChild(secondPath, firstPath))
                middleValue = bestOfChunk[floor(bestCount / 2)]
                newPathes.append(middleValue)
                newPathes.append(middleValue)

        return newPathes

    def _createChild(self, firstPath, secondPath):
        newCitiesOrder = []
        firstCitiesList = firstPath.cities[:floor(self.cityCount)]
        secondCitiesList = secondPath.cities[ceil(self.cityCount):]
        newCitiesOrder.extend(firstCitiesList)
        newCitiesOrder.extend(secondCitiesList)
        return Path(newCitiesOrder)

    def _splitIntoChunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _mutate(self, mutationRate):
        for path in self._pathes:
            if random.random() <= mutationRate:
                self._swapRandomCities(path.cities)

    def _swapRandomCities(self, cities):
        idx = range(1, len(cities) - 1)
        i1, i2 = random.sample(idx, 2)
        cities[i1], cities[i2] = cities[i2], cities[i1]

    def _updateBestPath(self):
        value = min(node.distance for node in self._pathes)
        newBestPath = next((x for x in self._pathes if x.distance == value), None)
        if self.bestPath.distance > value:
            self.bestPath = newBestPath

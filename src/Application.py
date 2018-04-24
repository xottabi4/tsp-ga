import csv
import os

from definitions import RESOURCES_DIR
from src.ga.City import City
from src.ga.Path import Path
from src.ga.Population import Population

csv_name = os.path.join(RESOURCES_DIR, "ATT48.csv")
csv_answer_name = os.path.join(RESOURCES_DIR, "ATT48_answer.csv")


def main():
    cityList = read_csv()

    # Load correct answer
    answercitynumbers = read_answer_csv()
    answercitynumbers[:] = [x - 1 for x in answercitynumbers]
    answerCityList = list(cityList)
    answerCityList[:] = [answerCityList[i] for i in answercitynumbers]
    answerPath = Path(answerCityList)

    startingCity = cityList.pop(0)

    # cityList = []
    # cityList.append(City("a", 2, 3))
    # cityList.append(City("b", 3, 4))
    # cityList.append(City("c", 5, 6))
    # cityList.append(City("d", 7, 20))
    # cityList.append(City("e", 0, 13))
    # startingCity=City("start", 8, 8)

    mutationRate = 0.35
    iterationCount = 2000
    populationSize = 1000
    population = Population(startingCity, cityList, populationSize)
    for i in range(iterationCount):
        population.evolve(mutationRate)
        print(i, population.bestPath.distance)

    population.bestPath.print()
    population.bestPath.plotPath()

    print("\nCorrect Answer")
    print(answerPath.distance)
    answerPath.print()
    answerPath.plotPath()

    print("\nDifference: ", population.bestPath.distance - answerPath.distance)


def read_csv():
    cityList = []
    with open(csv_name, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            cityList.append(City(row[0], float(row[1]), float(row[2])))
    return cityList


def read_answer_csv():
    city_number = []
    with open(csv_answer_name, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            city_number.append(int(row[0]))
    return city_number


if __name__ == '__main__':
    main()

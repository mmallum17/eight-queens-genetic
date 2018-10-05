import random


class Chromosome:
    def __init__(self, state):
        self.state = state
        self.fitness = calculateFitness(state)


def calculateFitness(state):
    validPairs = 0
    stateLength = len(state)

    for i in range(0, stateLength - 1):
        row = int(state[i])
        for j in range(i + 1, stateLength):
            tempRow = int(state[j])
            rowValid = False
            diagValid = False

            # Check for different rows
            if row != tempRow:
                rowValid = True

            # Check for diagonals
            diagRowDist = j - i
            if tempRow != row + diagRowDist and tempRow != row - diagRowDist:
                diagValid = True

            # If rows and diags valid, pair of queens are valid
            if rowValid and diagValid:
                validPairs = validPairs + 1

    return validPairs


def getParent(population, totalFitness):
    # Generate a random number between 0 and totalFitness
    probability = random.randint(0, totalFitness)

    # Find parent chromosome
    partialFitness = 0
    parent = None
    for chromosome in population:
        partialFitness = partialFitness + chromosome.fitness
        if partialFitness >= probability:
            parent = chromosome
            break

    return parent


def populationFitnessSum(population):
    totalFitness = 0

    for chromosome in population:
        totalFitness = totalFitness + chromosome.fitness

    return totalFitness


def singlePointCrossover(parentOne, parentTwo):
    crossoverPoint = random.randint(0, 6)
    childOne = parentOne[0:crossoverPoint + 1] + parentTwo[crossoverPoint + 1:]
    childTwo = parentTwo[0:crossoverPoint + 1] + parentOne[crossoverPoint + 1:]
    return [childOne, childTwo]


def twoPointCrossover(parentOne, parentTwo):
    crossoverPointOne = random.randint(0, 6)
    crossoverPointTwo = random.randint(0, 6)
    while (crossoverPointTwo == crossoverPointOne):
        crossoverPointTwo = random.randint(0, 6)

    if crossoverPointOne > crossoverPointTwo:
        temp = crossoverPointOne
        crossoverPointOne = crossoverPointTwo
        crossoverPointTwo = temp

    childOne = parentOne[0:crossoverPointOne + 1] + parentTwo[crossoverPointOne + 1: crossoverPointTwo + 1] + parentOne[
                                                                                                              crossoverPointTwo + 1:]
    childTwo = parentTwo[0:crossoverPointOne + 1] + parentOne[crossoverPointOne + 1: crossoverPointTwo + 1] + parentTwo[
                                                                                                              crossoverPointTwo + 1:]

    return [childOne, childTwo]


def cutAndSpliceCrossover(parentOne, parentTwo):
    crossoverPointOne = random.randint(0, 6)
    crossoverPointTwo = random.randint(0, 6)

    childOne = parentOne[0:crossoverPointOne + 1] + parentTwo[crossoverPointTwo + 1:]
    childTwo = parentTwo[0:crossoverPointOne + 1] + parentOne[crossoverPointTwo + 1:]

    if len(childOne) > 8:
        childOne = childOne[0:8]
    elif len(childOne) < 8:
        for i in range(8 - len(childOne)):
            randomNumber = random.randint(1, 8)
            childOne = childOne + str(randomNumber)

    if len(childTwo) > 8:
        childTwo = childTwo[0:8]
    elif len(childOne) < 8:
        for i in range(8 - len(childTwo)):
            randomNumber = random.randint(1, 8)
            childTwo = childTwo + str(randomNumber)

    return [childOne, childTwo]


def uniformCrossover(parentOne, parentTwo):
    childOne = ""
    childTwo = ""
    for i in range(8):
        randomValue = random.randint(0, 1)
        if (randomValue == 0):
            childOne = childOne + parentTwo[i]
            childTwo = childTwo + parentOne[i]
        else:
            childOne = childOne + parentOne[i]
            childTwo = childTwo + parentTwo[i]

    return [childOne, childTwo]


def reproduce(parentOne, parentTwo, crossover):
    children = None

    if (crossover == SINGLE_POINT):
        children = singlePointCrossover(parentOne, parentTwo)
    elif (crossover == TWO_POINT):
        children = twoPointCrossover(parentOne, parentTwo)
    elif (crossover == CUT_AND_SPLICE):
        children = cutAndSpliceCrossover(parentOne, parentTwo)
    elif (crossover == UNIFORM):
        children = uniformCrossover(parentOne, parentTwo)

    return children


def mutate(child):
    geneMutationAmount = random.randint(1, 8)
    geneToMutate = random.randint(0, 8 - geneMutationAmount)
    mutatedChromosome = ""
    for i in range(geneToMutate, geneToMutate + geneMutationAmount):
        mutateValue = random.randint(1, 8)
        mutatedChromosome = child[0:i] + str(mutateValue) + child[i + 1:]
        child = mutatedChromosome
    return mutatedChromosome


SINGLE_POINT = 0
TWO_POINT = 1
CUT_AND_SPLICE = 2
UNIFORM = 3


validSolution = "82417536"
invalidSolution = "43254323"
population = [Chromosome("24748552"), Chromosome("32752411"), Chromosome("24415124"),
              Chromosome("32543213")]
populationSize = 4
selectionSize = 2
mutationRate = 0.4
iterationAmount = -1
crossover = 2

while population[0].fitness < 28:
    print(population[0].fitness)
    print(population[0].state)

    newPopulation = []
    # Save fittest parents, if selection size is small
    if selectionSize < populationSize:
        population.sort(key=lambda chromosome: chromosome.fitness, reverse=True)
        for i in range(populationSize - selectionSize):
            newPopulation.append(population[i])

    # Get offspring and add to new population
    totalFitness = populationFitnessSum(population)
    for i in range(int(selectionSize / 2)):
        parentOne = getParent(population, totalFitness)
        parentTwo = getParent(population, totalFitness)
        children = reproduce(parentOne.state, parentTwo.state, crossover)

        # Decide mutation for both offspring
        for j in range(2):
            probability = random.random()
            if mutationRate > probability:
                children[j] = mutate(children[j])

        # Add children to new population
        for j in range(2):
            newPopulation.append(Chromosome(children[j]))

    newPopulation.sort(key=lambda chromosome: chromosome.fitness, reverse=True)
    # Verify population is correct size
    if len(newPopulation) > populationSize:
        while len(newPopulation) > populationSize:
            del newPopulation[-1]

    population = newPopulation

print(population[0].fitness)
print(population[0].state)

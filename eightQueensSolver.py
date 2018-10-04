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

validSolution = "82417536"
invalidSolution = "43254323"
fitness = calculateFitness(validSolution)
print(fitness)

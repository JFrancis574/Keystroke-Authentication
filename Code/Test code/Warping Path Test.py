import numpy as np

def generateMatrix(size):
    tempArray = []
    for x in range(size*size):
        tempArray.append(x+1)
    return np.matrix(tempArray).reshape(size, size)

def getRows(matrix):
    return (matrix[0: , :]).tolist()

def getColumns(matrix, matrixSize):
    tempArray = []
    i = 0
    while ( i <= matrixSize-1):
        tempArray.append(matrix[:, i].tolist())
        i +=1
    return tempArray
    #(matrix[:, 0])

def cleanColumns(inpArray):
    for position, value in enumerate(inpArray):
        print(value)
        for x in value:
            print("Value: ", value)
            temp = []
            for i in x:
                temp.append(i)
                print(i)
                print("temp: ",temp)
    print(temp)

D = generateMatrix(4)

print("OG: ", D)
print("Size: ", D.size)
print("ToList: ",D.tolist())

print("Rows: ", getRows(D))
print("Columns: ",getColumns(D, 4))
cleanColumns(getColumns(D, 4))


#j = columns(D)

#while (i>1 & j>1):
 #   if i == 1:
#        j = j-1
 #   elif j == 1:
 #       j = j -1
#    else:
 #       pass



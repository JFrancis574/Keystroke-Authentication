import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 3, 7])
y = np.array([1, 2, 2, 2, 2, 2, 2, 4])

# https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
# The distance between a and b is the last element of the matrix. In this case it is 2

def dynamicTimeWarping(s, t):
    n, m = len(s), len(t)
    matrix = np.zeros((n+1, m+1))
    for i in range(n+1):
        for j in range(m+1):
            matrix[i,j] = np.inf
    
    matrix[0,0] = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(s[i-1] - t[j-1])
            last_min = np.min([matrix[i-1, j], matrix[i, j-1], matrix[i-1, j-1]])
            matrix[i, j] = cost + last_min
    
    return matrix

print(dynamicTimeWarping(x, y))

distance, path = fastdtw(x, y, dist=euclidean)

# Pass in the KDS signal
# Pass in the KDS signal for the same text
# This is the same word typed by two different people
KDS1 = {0.1 : 1, 0.2 : 2, 0.3 : 3, 0.4 : 3, 0.5 : 2, 0.6 : 2, 0.7 : 1, 0.8 : 0, 0.9 : 1}
KDS2 = {0.1 : 1, 0.2 : 2, 0.3 : 2, 0.4 : 2, 0.5 : 2, 0.6 : 2, 0.7 : 2, 0.8 : 4}

x = np.array(list(KDS1.values()))
y = np.array(list(KDS2.values()))

distance, path = fastdtw(x, y, dist=euclidean)
print(path)
print(distance)

f,g = [], []
for [a,b] in path:
    #print(x[a], y[b])
    f.append(x[a])
    g.append(y[b])


print(f)
print(g)
plt.plot([x/10 for x in range(1,10)], f, color="purple")
plt.plot([x/10 for x in range(1,10)], g, color="red")

#plt.plot(KDS1.keys(), KDS1.values())
#plt.plot(KDS2.keys(), KDS2.values())
plt.show()
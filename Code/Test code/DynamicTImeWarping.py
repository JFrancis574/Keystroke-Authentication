import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 3, 7])
y = np.array([1, 2, 2, 2, 2, 2, 2, 4])

# https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
# The distance between a and b is the last element of the matrix. In this case it is 2

def compute_euclidean_distance_matrix(x, y):
    """Calculate distance matrix
    This method calcualtes the pairwise Euclidean distance between two sequences.
    The sequences can have different lengths.
    """
    dist = np.zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            dist[i,j] = (x[j]-y[i])**2
    return dist


def compute_accumulated_cost_matrix(x, y):
    """Compute accumulated cost matrix for warp path using Euclidean distance
    """
    distances = compute_euclidean_distance_matrix(x, y)

    # Initialization
    cost = np.zeros((len(y), len(x)))
    cost[0,0] = distances[0,0]
    
    for i in range(1, len(y)):
        cost[i, 0] = distances[i, 0] + cost[i-1, 0]  
        
    for j in range(1, len(x)):
        cost[0, j] = distances[0, j] + cost[0, j-1]  

    # Accumulated warp path cost
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            cost[i, j] = min(
                cost[i-1, j],    # insertion
                cost[i, j-1],    # deletion
                cost[i-1, j-1]   # match
            ) + distances[i, j] 
            
    return cost


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
print(distance)

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

x_path, y_path = zip(*path)
x_path = np.asarray(x_path)
y_path = np.asarray(y_path)
x_warped = x[x_path]
y_warped = y[y_path]

corr2 = np.corrcoef(x_warped, y_warped)
print(corr2[0,1])
print(f'Correlation after DTW: {corr2[0, 1]:.4f}')

print(compute_euclidean_distance_matrix(x, y))

fig, ax = plt.subplots(2, 1)
ax[0].plot(x, color="orange") #KDS1
ax[0].plot(y, color="blue") #KDS2
ax[0].grid(True)
ax[1].plot(x_warped, color="orange")
ax[1].plot(y_warped, color="blue")
ax[1].grid(True)
ax[0].set_title('Original Signals')
ax[1].set_title('Aligned with DTW')
plt.show()

warpedDictKDS1 = {}
warpedDictKDS2 = {}
for i in range(len(x_warped)):
    warpedDictKDS1[i/10] = x_warped[i]
    warpedDictKDS2[i/10] = y_warped[i]

fig, ax = plt.subplots(2, 1)
ax[0].plot(KDS1.keys(), KDS1.values(), color="orange") #KDS1
ax[0].plot(KDS2.keys(), KDS2.values(), color="blue") #KDS2
ax[0].grid(True)
ax[1].plot(warpedDictKDS1.keys(), warpedDictKDS1.values(), color="orange")
ax[1].plot(warpedDictKDS2.keys(), warpedDictKDS2.values(), color="blue")
ax[1].grid(True)
ax[0].set_title('Original Signals')
ax[1].set_title('Aligned with DTW')
plt.show()

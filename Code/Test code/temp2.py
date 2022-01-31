import json
from keyboardTest import *


# with open(os.getcwd()+"/Data/WordData/"+'above.json', 'r') as read_file:
#     temp = json.load(read_file)
# temp = [
#             [0, {0.0001: 0.5, 0.0002: 0.5, 0.0003: 0.5, 0.0004: 1.0, 0.0005: 1, 0.0006: 1.0, 0.0007: 1.0, 0.0008: 0.5}],
#             [1, {0.0001: 0.5, 0.0002: 0.5, 0.0003: 0.5, 0.0004: 1.0, 0.0005: 1, 0.0006: 1.0, 0.0007: 1.0, 0.0008: 0.5}]
#         ]

temp2 = {0.0001: 0.5, 0.0002: 0.5, 0.0003: 0.5, 0.0004: 1.0, 0.0005: 1, 0.0006: 1.0, 0.0007: 1.0, 0.0008: 0.5}
        # Word Data For
        # ALWAYS KDS
        # IDEA
        # No point storing 
        # 0.001 : 1
        # 0.002 : 1
        # 0.003 : 1
        # 0.004 : 1
        # Might as well store 0.001 -> 0.004 : 1
        # [0.001, 0.004] : 1
def compress(dataIn):
    data = np.array(list(dataIn.values()))
    keys = np.array(list(dataIn.keys()))
    startValue = data[0]
    start = keys[0]
    endDict = {}
    for i, j in enumerate(data):
        if j == startValue:
            grouping = (start, keys[i])
        else:
            endDict[grouping] = startValue
            startValue = data[i]
            start = keys[i]
            grouping = (start, keys[i])
        if i == len(data)-1:
            grouping = (start, keys[i])
            endDict[grouping] = startValue
    return endDict

print(compress(temp2))

def remap_keys(mapping):
        return [{'key':k, 'value': v} for k, v in mapping.items()]
data = remap_keys(compress(temp2))
print(data)

# with open(os.getcwd()+"/Data/WordData/"+'above2.json', 'w') as write_file:
#     json.dump(remap_keys(compress(temp)), write_file)
outDict = {}
for x in data:
    print(x)
    startTime = list(x.values())[0][0]
    endTime = list(x.values())[0][1]
    value = list(x.values())[1]
    print(startTime, endTime, value)
    for x in range(int(startTime*10000), int(endTime*11000)+1):
        outDict[x/10000] = value

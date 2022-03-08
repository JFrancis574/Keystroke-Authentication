import profile as p
import os
import time as t
import keyboard as k
from Interval import Calculation

def testerDataFormer(string, holdTime, floatTime, file='N'):
    output = []
    if file == 'N':
        data = string
    else:
        if os.path.exists(os.getcwd()+string):
            data = open(string, 'r')
        else:
            return
        
    if isinstance(holdTime, float) and isinstance(floatTime, float):
        time = t.time()
        for x in data:
            output.append(k.KeyboardEvent('down', 99, name=x, time=time))
            time+= holdTime
            output.append(k.KeyboardEvent('up', 99, name=x, time=time))
            time += floatTime
        return output
    elif isinstance(holdTime, list) and isinstance(floatTime, float):
        if len(holdTime) > len(data):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime[i]
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime
            return output
    elif isinstance(holdTime, float) and isinstance(floatTime, list):
        if len(floatTime) > len(data):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime[i]
            return output
    else:
        if (len(holdTime) > len(data)) or (len(floatTime) > len(data)):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime[i]
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime[i]
            return output
                      

start = t.time()
pf = p.Profile('temp')
dt = testerDataFormer("Hello", [0.1, 0.2, 0.1, 0.3, 0.1], [3.0, 2.0, 1.5, 1.9, 2.9])
# Both floatime and holdTime need to be in second. e.g one minute between presses would be 60. 1 second would be 1. A tenth of a second, 0.1 e.g. 
# Examples
# Simple string with 2 floats
# print("FLOATS: ")
# for x in dt:
#     print(x.name, x.time)
    
# print("Arrays: ")
# for x in testerDataFormer("Hello", [0.1, 0.2, 0.1, 0.3, 0.1], [1.0, 2.0, 0.5, 1.0, 0.9]):
#     print(x.name, x.time)
    
    
inter = Calculation(dt, start, pf, 0)
print(inter.noWords)
decision, index = inter.validation(mode='r')
print(decision, index)
    
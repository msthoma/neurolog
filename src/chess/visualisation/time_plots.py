

import matplotlib.pyplot as plt
import numpy as np
from params import logs_root

def importData(fileName:str):
    array = []
    xs = []
    x = list()
    y = list()
    with open(fileName) as fp:
        while True:
            line = fp.readline()
            line = line.rstrip("\n")
            if not line:
                break
            if not (line.startswith('Iteration') or line.startswith('Epoch') or line.startswith('Total') or line.startswith('Running') or line.startswith('cuda')
or line.startswith('*') or line.startswith('!') or line.startswith('SICStus') or line.startswith('Licensed')):
                data = line.split('\t')
                x.append(int(data[0]))
                y.append(float(data[1])/100)
                if int(data[0]) == 9000:
                    array.append(np.array(y.copy()))
                    xs = np.array(x)
                    x = list()
                    y = list()
    
    return xs,array 


def createCurves(filename):    
    
    x,arrays = importData(filename)
        
    ymin = arrays[0]
    ymax = arrays[0]
    
    for index in [1,2,3,4]:
        ymin = np.minimum(ymin, arrays[index]) 
        ymax = np.maximum(ymax, arrays[index])   
    
    median = []
    for index in range(0,len(ymin)):
        value = np.median([arrays[0][index], arrays[1][index], arrays[2][index], arrays[3][index], arrays[4][index]])
        median.append(value)
    
    return x,ymin,ymax,np.array(median)

BIGGER_SIZE = 16

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

_, ax = plt.subplots()
ax.set_xlim(0, 9000)

path1 = logs_root + "BSV/log.txt"
x,ymin1,ymax1,ymed1 = createCurves(path1)

path2 = logs_root + "ISK/log.txt"
x,ymin2,ymax2,ymed2 = createCurves(path2)

path3 = logs_root + "NGA/log.txt"
x,ymin3,ymax3,ymed3 = createCurves(path3)

line1, = ax.plot(x, ymed1, '-')
ax.fill_between(x, ymin1, ymax1, alpha=0.2)
    
line2, = ax.plot(x, ymed2, 'g-')
ax.fill_between(x, ymin2, ymax2, facecolor='g', alpha=0.2)

line3, = ax.plot(x, ymed3, 'r-')
ax.fill_between(x, ymin3, ymax3, facecolor='r', alpha=0.2)

plt.legend([line1, line2, line3], ["NLOG ?=BSV n=3", "NLOG ?=ISK n=3", "NLOG ?=NGA n=3"], loc='upper left')
plt.savefig('time.png', format='png', bbox_inches='tight')



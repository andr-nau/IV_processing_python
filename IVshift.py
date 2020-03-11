# IV SHIFT
# This is code for processing of experimental data from I-V (current vs voltage) measurements of superconducting nanowires.
# The tasks are:
# 1) to rescale and center I-V curve relatively to the (0.0) coordinates (important for obtaining retrapping current values and proper R-I presentation (resistance vs current);
# 2) to transform I-V to R-I presentation (resistance vs current).
# 3) to save processed data

import matplotlib.pyplot as plt

def selectData(minVal, maxVal, dataForCheck, dataForSelect):
    tempList=[]
    for i in range(len(dataForCheck)):
        if dataForCheck[i]>minVal and dataForCheck[i]<maxVal:
            tempList.append(dataForSelect[i])
    return tempList

zeroPosition=0
rawdata=[]
voltage=[]
current=[]
resist=[]
shift_current=[]
shift_voltage=[]

rescaleVoltage=1/100
rescaleCurrent=1/100/100


# READ I-V DATA AND DIVIDE TO VOLTAGE AND CURRENT LISTS

# Input file contains 4 columns tab separated: time | voltage | time | current
filename="iv1"
with open(filename+".txt","r") as f:
    rawdata = [float(i) for i in f.read().split()]

voltage=list(map(lambda x: x*rescaleVoltage, rawdata[1::4]))
current=list(map(lambda x: x*rescaleCurrent, rawdata[3::4]))

# Plotting of raw data on Fig0
plt.figure(0)
plt.plot(voltage, current)

# SHIFT ALONG Y (CURRENT) AXIS.
# Selecting the central part of I-V to find max/min Y values for centering. 
# Excluding side parts is needed, because they could be higher than central part.
# Select Current(Y) data using Voltage(X) limits
leftX = -1e-4
rightX = 1e-4
tempList=selectData(leftX, rightX, voltage, current)

# Shift along Y axis to symmetrical position.
shiftY=zeroPosition-(max(tempList)+min(tempList))/2
for i in range(len(current)):
    shift_current.append(current[i]+shiftY)

# Calculate switching current (max current for zero voltage state)
isw=(abs(max(current))+abs(min(current)))/2

# Control of Y shift
print("raw data minY=",min(current),"\nraw data maxY=",max(current),"\nshiftY=",shiftY,"\nSwitching current=", isw)
plt.plot(voltage, shift_current)

# SHIFT ALONG X (VOLTAGE) AXIS.
# Select part of Y-shifted data, that has near zero Y values.
# Because X shifting is based only on the position of central vertical I-V line.
#Select Voltage(X) data using Current(Y) limits

bottomY=-1e-6
topY=1e-6
tempList=selectData(bottomY, topY, shift_current, voltage)

#Shift of X data
shiftX=zeroPosition-(max(tempList)+min(tempList))/2
for i in range(len(voltage)):
    shift_voltage.append(voltage[i]+shiftX)

#Control of X shift
print("minX=", min(tempList), "maxX=", max(tempList), "shiftX=", shiftX)

#Final shifted graph
plt.plot(shift_voltage, shift_current)

#Resistance calc and plot graph in R-I presentation
for j in range(len(voltage)):
    resist.append((shift_voltage[j])/(shift_current[j]))

#Resistance vs current graph
plt.figure(1)
#plt.axis([-0.00005, 0.00005, -10, 150])
plt.plot(shift_current, resist)

#Save to new file
output=zip(shift_voltage, shift_current, shift_current, resist)

with open(filename+"-shifted.txt", 'w') as f:
    f.write("Voltage Current Current Resistance\n")
    for item in output:
        f.write("%s %s %s %s\n" % item)
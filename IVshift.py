"""
IV SHIFT
Code for experimental data processing.
Data: I-V (current vs voltage) characteristics of superconducting nanowires.
Workflow:
1. rescaling and centering of I-V curve relatively to the (0.0) coordinates.
2. transforming I-V to R-I (resistance vs current) presentation.
3. saving processed data.

@author: A.Naumov
"""

import matplotlib.pyplot as plt


def selectData(minVal, maxVal, dataForCheck, dataForSelect):
    """
    Function selects part of input data list (arg2), with index corresponding
    to the index of data1 list (arg1) that meet condition
    minVal < data1 < maxVal.
    Then it returns new list.
    """
    tempListSel = []
    tempListChk = []
    for i in range(len(dataForCheck)):
        if dataForCheck[i] > minVal and dataForCheck[i] < maxVal:
            tempListSel.append(dataForSelect[i])
            tempListChk.append(dataForCheck[i])
    return tempListSel


def shiftData(selectedData, dataForShift):
    """
    Function finds middle point of selected part of data (arg1),
    then calculates shift value for shifting of full data (arg2)
    to center middle point at (0.0) position.
    Then it returns new list
    """
    tempList = []
    shift = zeroPosition - (max(selectedData) + min(selectedData))/2
    for i in range(len(dataForShift)):
        tempList.append(dataForShift[i]+shift)
    return tempList


def readData(filename, rescaleX, rescaleY):
    """
    Function reads experimental data file and selects voltage and current.
    Input file contains 4 columns: time | voltage | time | current
    """
    with open(filename+".txt", "r") as f:
        rawdata = [float(i) for i in f.read().split()]
    voltage = list(map(lambda x: x*rescaleX, rawdata[1::4]))
    current = list(map(lambda x: x*rescaleY, rawdata[3::4]))
    return voltage, current


def saveData(filename, voltage, current, resist):
    output = zip(voltage, current, current, resist)
    with open(filename+"-shifted.txt", 'w') as f:
        f.write("Voltage Current Current Resistance\n")
        for item in output:
            f.write("%s %s %s %s\n" % item)


def selectRetrap(minVal, maxVal, voltage, current):
    """
    Function selects part of input data lists (arg2,3), with index
    corresponding to the index of first data list (arg2) that meet condition
    minVal < data < maxVal.
    Then it returns two new lists with selected data.
    """
    v = []
    c = []
    for i in range(len(voltage)):
        if voltage[i] > minX and voltage[i] < maxX:
            v.append(voltage[i])
            c.append(current[i])
    return v, c


zeroPosition = 0
rawdata = []
voltage = []
current = []
resist = []
tempList = []
shift_current = []
shift_voltage = []

rescaleVoltage = 1 / 100        # V1/100 - remove x100 amplification
rescaleCurrent = 1 / 100 / 100  # remove x100 amplification, current=V2/100 Ohm


# READ I-V DATA AND DIVIDE TO VOLTAGE AND CURRENT LISTS
filename = "iv1"
voltage, current = readData(filename, rescaleVoltage, rescaleCurrent)


# PLOT OF RAW DATA
plt.figure(0)
plt.plot(voltage, current)


# SHIFT ALONG Y (CURRENT) AXIS.
"""
Selecting central part of I-V to find max/min Y values for centering.
Side parts of I-V could be higher than central part, so they are excluded.
"""
minX = -1e-4
maxX = 1e-4

tempList = selectData(minX, maxX, voltage, current)  # Select Current(Y) data using Voltage(X) limits. Limits are taken from raw graph.

shift_current = shiftData(tempList, current)  # Shift along Y axis to symmetrical position.

isw = (abs(max(tempList)) + abs(min(tempList))) / 2  # Calculate switching current (max current for zero voltage state)


# CONTROL AFTER Y-SHIFTING
print("raw data minY=", min(current), "\nraw data maxY=", max(current), 
      "\nSwitching current=", isw)
plt.plot(voltage, shift_current)


# SHIFT ALONG X (VOLTAGE) AXIS.
"""
Select part of Y-shifted data, that has near zero Y values.
X-shifting is based only on the position of central vertical I-V line.
"""

minY = -3e-6
maxY = 3e-6

tempList = selectData(minY, maxY, shift_current, voltage)  # Select Voltage(X) data using Current(Y) limits. Limits should be close to 0.

shift_voltage = shiftData(tempList, voltage)  # Shift of X data


# CONTROL AFTER X-SHIFTING
print("raw data minX=", min(tempList), "\nraw data maxX=", max(tempList))
plt.plot(shift_voltage, shift_current)  # Final shifted graph


# RESISTANCE CALC
for j in range(len(voltage)):
    resist.append((shift_voltage[j])/(shift_current[j]))


# CONTROL PLOT RESISTANCE
plt.figure(1)  # Resistance vs current
plt.axis([-0.00005, 0.00005, -10, 150])  # change graph range
plt.plot(shift_current, resist)


# RETRAPPING CURRENT
"""
selecting middle part around zero for finding Xmin Xmax
"""
tempList = []
tempList = selectData(minY, maxY, shift_current, shift_voltage)

print("\nRETRAPPING")

# "+" BRANCH
print("\nIr+\n")
minX = max(tempList)+5e-5
maxX = 4e-4
print("minX=", minX, "\tmaxX=", maxX)
v = []
c = []
v, c = selectRetrap(minX, maxX, shift_voltage, shift_current)
retrapCurrentP = min(c)

# CONTROL OUTPUT
plt.figure(3)
plt.plot(v, c, 'bo')
print("+Ir=:", retrapCurrentP)


# "-" BRANCH
print("\nIr-\n")
minX = -4e-4
maxX = min(tempList)-5e-5
print("minX=", minX, "\tmaxX=", maxX)
v = []
c = []
v, c = selectRetrap(minX, maxX, shift_voltage, shift_current)
retrapCurrentN = max(c)


# CONTROL OUTPUT
plt.figure(4)
plt.plot(v, c, 'bo')
print("-Ir=:", retrapCurrentN)

# MEAN RETRAPPING CURRENT VALUE
retrap = (abs(retrapCurrentP) + abs(retrapCurrentN)) / 2
print("\n mean Ir=", retrap)

# SAVING DATA "voltage|current|current|resistance"
saveData(filename, shift_voltage, shift_current, resist)

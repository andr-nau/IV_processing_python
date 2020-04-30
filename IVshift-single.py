"""
IV SHIFT
Code for experimental data processing - shifting/centering of the data 
and obtaining values for critical points.
Input data: file with experimental numerical data in tabular form (I-V current vs voltage characteristics of superconducting nanowires).
Workflow:
    Input from txt file.
    Rescaling and centering of I-V curve relatively to the (0.0) coordinates.
    Obtaining values of some critical points.
    Transformation I-V to R-I (resistance vs current).
    Saving processed data in tabular form.
Output data: file with processed data in tabular form

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
    rawdata = []
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

def figplot(n, axisX, axisY, label, labelX="X axis", labelY="y axis",
            style='-'):
    plt.figure(n)
    plt.plot(axisX, axisY, style, label=label)
    plt.legend()
    plt.xlabel(labelX)
    plt.ylabel(labelY)


zeroPosition = 0
rawdata = []
voltage = []
current = []
resist = []
tempList = []
shift_current = []
shift_voltage = []

rescaleVoltage = 1 / 100        # V1/100 - remove x100 amplification
rescaleCurrent = 1 / 100 / 100  # V2/100/100 remove x100 amplification, and convert to current


# READ I-V DATA AND DIVIDE TO VOLTAGE AND CURRENT LISTS
filename = "iv1"
voltage, current = readData(filename, rescaleVoltage, rescaleCurrent)


# PLOT OF RAW DATA
figplot(0, voltage, current, "rawdata", "Voltage (V)", "Current (A)")


# SHIFT ALONG Y (CURRENT) AXIS.
"""
    Select central part of I-V to find max/min Y values
    Side parts of I-V can be higher than central part, 
    so they needs to be excluded.
    Calculate shift step for centering relative X=0.
    Move all data by Y-axis by shift step.
    Find max/min => Iswitching
"""
minX = -1e-4
maxX = 1e-4

tempList = selectData(minX, maxX, voltage, current)  # Select Current(Y) data using Voltage(X) limits.

shift_current = shiftData(tempList, current)  # Shift along Y axis to symmetrical position.

isw = (abs(max(tempList)) + abs(min(tempList))) / 2  # Calculate switching current (max current for zero voltage state)


# CONTROL AFTER Y-SHIFTING
print("\nRawdata:\nminY =", "{:2.2e}".format(min(current)), 
      "\nmaxY =", "{:2.2e}".format(max(current)), 
      "\nSwitching current =", "{:2.2e}".format(isw))
print("\nAfter Yshift:\nminY =", "{:2.2e}".format(min(shift_current)), 
      "\nmaxY =", "{:2.2e}".format(max(shift_current)), 
      "\nSwitching current =", "{:2.2e}".format(isw))
figplot(0, voltage, shift_current, "shifted by Y", "Voltage (V)",
        "Current (A)")


# SHIFT ALONG X (VOLTAGE) AXIS.
"""
    X-shift is based on position of central vertical I-V line.
    Select small part of data around zero, with +Y and -Y close to zero.
    Find min/max X values
    Calculate shift step for centering relative Y=0.
    Move all data by X-axis by shift step.
"""

minY = -3e-6
maxY = 3e-6

tempList = selectData(minY, maxY, shift_current, voltage)  # Select Voltage(X) data using Current(Y) limits. Limits should be close to 0.

shift_voltage = shiftData(tempList, voltage)  # Shift of X data


# CONTROL AFTER X-SHIFTING
print("\nBefore shift:\nminX=", "{:2.2e}".format(min(tempList)),
      "\nmaxX=", "{:2.2e}".format(max(tempList)))
figplot(0, shift_voltage, shift_current, "shifted by X,Y", "Voltage, (V)",
        "Current (A)")  # Final shifted graph


# RESISTANCE CALC
for j in range(len(voltage)):
    resist.append((shift_voltage[j])/(shift_current[j]))


# CONTROL PLOT RESISTANCE
figplot(1, shift_current, resist, "R-I presentation", "Current (A)",
        "Resistance (Ohms)")
plt.axis([-0.00005, 0.00005, -10, 150])  # change graph range

# RETRAPPING CURRENT
"""
    Select middle part around zero to find Xmin Xmax for shifted data
    Select data that falls into a narrow area on the left and right next to
    the center line.
    Find min(Y) for "+" branch and max(Y) for "-" branch
"""
tempList = []
tempList = selectData(minY, maxY, shift_current, shift_voltage)

print("\nRETRAPPING")

# "+" BRANCH
print("\nIr+\n")
minX = max(tempList)+5e-5
maxX = 4e-4
print("minX=", "{:2.2e}".format(minX), "\tmaxX=", "{:2.2e}".format(maxX))
v = []
c = []
v, c = selectRetrap(minX, maxX, shift_voltage, shift_current)
retrapCurrentP = min(c)

# CONTROL OUTPUT
figplot(2, v, c, "+ branch", "Voltage, (V)", "Current (A)", 'bo')
print("+Ir=:", "{:2.2e}".format(retrapCurrentP))


# "-" BRANCH
print("\nIr-\n")
minX = -4e-4
maxX = min(tempList)-5e-5
print("minX=", "{:2.2e}".format(minX), "\tmaxX=", "{:2.2e}".format(maxX))
v = []
c = []
v, c = selectRetrap(minX, maxX, shift_voltage, shift_current)
retrapCurrentN = max(c)


# CONTROL OUTPUT
figplot(3, v, c, "- branch", "Voltage, (V)", "Current (A)", 'bo')
print("-Ir=:", "{:2.2e}".format(retrapCurrentN))

# MEAN RETRAPPING CURRENT VALUE
retrap = (abs(retrapCurrentP) + abs(retrapCurrentN)) / 2
print("\nmean Ir=", "{:2.2e}".format(retrap))

# SAVING DATA "voltage|current|current|resistance"
saveData(filename, shift_voltage, shift_current, resist)

import matplotlib.pyplot as plt
f=open("iv1.txt","r")

zeroPosition=0
rawdata=[]
voltage=[]
current=[]
tempList=[]
resist=[]
shift_current=[]
shift_voltage=[]

rescaleVoltage=1/100
rescaleCurrent=1/100/100

#Read IV data and divide to voltage and current lists
rawdata = [float(i) for i in f.read().split()]
voltage=list(map(lambda x: x*rescaleVoltage, rawdata[1::4]))
current=list(map(lambda x: x*rescaleCurrent, rawdata[3::4]))

plt.figure(0)

#Rawdata graph
plt.plot(voltage, current)

#Shift of Y data
shiftY=zeroPosition-(max(current)+min(current))/2
isw=(abs(max(current))+abs(min(current)))/2
print("minY=",min(current),"maxY=",max(current),"shiftY=",shiftY,"Switching current=", isw)
for i in range(len(current)):
    shift_current.append(current[i]+shiftY)

#Test graph
plt.plot(voltage, shift_current)

#Select data around zeroY for X shift
bottomBorder=-1e-6
topBorder=1e-6
for i in range(len(shift_current)):
    if shift_current[i]>bottomBorder and shift_current[i]<topBorder:
        tempList.append(voltage[i])

#Shift of X data
shiftX=zeroPosition-(max(tempList)+min(tempList))/2
print("minX=", min(tempList), "maxX=", max(tempList), "shiftX=", shiftX)
for i in range(len(voltage)):
    shift_voltage.append(voltage[i]+shiftX)

#Final shifted graph
plt.plot(shift_voltage, shift_current)

#Resistance calc and plot graph in R-I presentation
for j in range(len(voltage)):
    resist.append((shift_voltage[j])/(shift_current[j]))
plt.figure(1)
plt.axis([-0.00005, 0.00005, -10, 150])
plt.plot(shift_current, resist)

f.close
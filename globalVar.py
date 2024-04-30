wparaList = []
J2List = []
JList = []

chargeList = []
chargeSpinList = []

cleanBool = False
#!NOTICE: N in line -> N+1 and N-1 also satisfy the condition
#!NOTICE: so it should be "N:" in line

#! global variables:
# chargeList, chargeSpinList, xmin, xmax, xguess, tol, cleanBool, wparaList, J2List, JList

readCharge = False
tmplist2 = []
with open("input", "r") as input:
    for line in input:
        if "orbit" in line:
            templine = line.strip().split()
            for i in range(1,len(templine)):
                tcharge1, tcharge2 = templine[i].split(",")
                #*there should be one extra file (N-1)
                tmplist = list(range(int(tcharge1)-1, int(tcharge2)+1))
                chargeList.extend(tmplist)
            #*remove the duplicate
            chargeList = list(set(chargeList))
            chargeList.sort()

        if "charge spin start" in line:
            readCharge = True
            continue

        if "charge spin end" in line:
            readCharge = False

        if readCharge:
            tmplist1 = []
            templine = line.strip().split()
            #* templine: [charge in chargeList, charge, spin]
            for i in range(len(templine)):
                tmplist1.append(int(templine[i]))
            tmplist2.append(tmplist1)

            #* sort the charge spin list, by charge
            tmplist2 = sorted(tmplist2, key = lambda x: x[0])

        if "xmin" in line:
            templine = line.strip().split()
            xmin = float(templine[-1])
        if "xmax" in line:
            templine = line.strip().split()
            xmax = float(templine[-1])
        if "xguess" in line:
            templine = line.strip().split()
            xguess = float(templine[-1])
        if "tolerance" in line:
            templine = line.strip().split()
            tol = float(templine[-1])
        if "clean" in line:
            cleanBool = True        

#* check if the charge spin is complete
if len(tmplist2) != len(chargeList):
    raise Exception("Error: charge spin is not complete.")
#* convert the charge spin list to string
for i in range(len(tmplist2)):
    tmpstr = f"{tmplist2[i][1]} {tmplist2[i][2]}"
    chargeSpinList.append(tmpstr)
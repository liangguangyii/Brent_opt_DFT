#! global variables:
# chargeList, chargeSpinList, xmin, xmax, xguess, tol, cleanBool, restartBool, oldchkBool, singleBool, wparaList, J2List, JList, UDFT
wparaList = []
J2List = []
JList = []

chargeList = []
chargeSpinList = []

UDFT = []

oldchkBool = False
restartBool = False
cleanBool = False
singleBool = False
preBool = False


#*************************************************************


readCharge = False
tmplist2 = []
with open("input", "r") as input:
    for line in input:
        if "restart" in line:
            restartBool = True
        
        if "oldchk" in line:
            oldchkBool = True

        if "clean" in line:
            cleanBool = True 

        if "single point" in line:
            singleBool = True   

        if "preprocessing" in line:
            preBool = True

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

        #* turn on the readCharge flag
        if "charge spin start" in line:
            readCharge = True
            continue

        if "charge spin end" in line:
            readCharge = False

        #* finish reading the charge spin

        if readCharge:
            tmplist1 = []
            templine = line.strip().split()
            #* templine: [charge in chargeList, charge, spin]
            for i in range(3):
                tmplist1.append(int(templine[i]))
            #* append the last element (may be 'U' or just duplicate of the charge spin)
            tmplist1.append(templine[-1])
            tmplist2.append(tmplist1)

            #* sort the charge spin list, by charge(i in N+i)
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


if preBool:
    chargeList = []
    chargeList = [row[0] for row in tmplist2]

    #* sorted based on i in N+i, and if i is the same, then sort based on the spin
    tmplist2 = sorted(tmplist2, key = lambda x: (x[0], x[2]))

    #* convert the charge spin list to string
    for i in range(len(tmplist2)):
        tmpstr = f"{tmplist2[i][1]} {tmplist2[i][2]}"
        if tmplist2[i][-1] == "U":
            UDFT.append(True)
        else:
            UDFT.append(False)
        chargeSpinList.append(tmpstr)
else:
    #* check if the charge spin is complete(only for non-preBool case)
    if len(tmplist2) != len(chargeList):
        raise Exception("Error: charge spin is not matched with the number of orbitals.")
    #* convert the charge spin list to string
    for i in range(len(tmplist2)):
        tmpstr = f"{tmplist2[i][1]} {tmplist2[i][2]}"
        if tmplist2[i][-1] == "U":
            UDFT.append(True)
        else:
            UDFT.append(False)
        chargeSpinList.append(tmpstr)

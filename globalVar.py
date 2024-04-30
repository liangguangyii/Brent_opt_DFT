#! global variables:
# chargeList, chargeSpinList, xmin, xmax, xguess, tol, cleanBool, restartBool, oldchkBool, wparaList, J2List, JList, UDFT
wparaList = []
J2List = []
JList = []

chargeList = []
chargeSpinList = []

UDFT = []

oldchkBool = False
restartBool = False
cleanBool = False


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
    

#* check if the charge spin is complete
if len(tmplist2) != len(chargeList):
    raise Exception("Error: charge spin is not complete.")
#* convert the charge spin list to string
for i in range(len(tmplist2)):
    tmpstr = f"{tmplist2[i][1]} {tmplist2[i][2]}"
    if tmplist2[i][-1] == "U":
        UDFT.append(True)
    else:
        UDFT.append(False)
    chargeSpinList.append(tmpstr)
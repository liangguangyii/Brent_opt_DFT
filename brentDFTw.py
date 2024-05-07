from globalVar import xmin, xmax, xguess, tol, cleanBool, restartBool, oldchkBool, UDFT, chargeList, chargeSpinList, singleBool, preBool
from brent import *
from fileIO import *
from function import *


if singleBool:
    J, J2 = calIP(xguess)
    with open("output.txt", "w") as finout:
        finout.write(f"J:\t{J:.12f}\nJ2:\t{J2:.12f}\n")
#* if calculte single point, then brent won't be executed
#* only calculate J J2 at xguess

elif preBool:
    g16input_0(chargeList, chargeSpinList)

else:
    if restartBool:
        xmin, icount = brentMethod_re(funJ2)
    else:
        #Clean the files
        if cleanBool:
            fileClean()

        #* clean the output file if restart is not specified
        os.system("rm output.txt")
        os.system("rm Brent.out")
        xmin, icount = brentMethod(xmin, xmax, xguess, funJ2, tol)

    #Save all the file name into fileList.txt
    with open ("fileList.txt","w") as fileList:
        for i in range(len(wparaList)):
            fileList.write(f"{int(wparaList[i]*10000):05}\n")    
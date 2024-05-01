from globalVar import xmin, xmax, xguess, tol, cleanBool, restartBool
from brent import *
from fileIO import *
from function import *

if restartBool:
    xmin, icount = brentMethod_re(funJ2)
else:
    #Clean the files
    if cleanBool:
        fileClean()

    #* clean the output file if restart is not specified
    os.system("rm output.txt")
    xmin, icount = brentMethod(xmin, xguess, xmax, funJ2, tol)

#Save all the file name into fileList.txt
with open ("fileList.txt","w") as fileList:
    for i in range(len(wparaList)):
        fileList.write(f"{int(wparaList[i]*10000):05}\n")

from globalVar import *
from brent import *
from fileIO import *
from function import *


#Clean the files
if cleanBool:
    fileClean()
    os.system("rm fileList.txt")

xmin, icount = brentMethod(0.05, 0.325, 0.6, funJ2, 1.0e-3)

#Save all the file name into fileList.txt
with open ("fileList.txt","w") as fileList:
    for i in range(len(wparaList)):
        fileList.write(f"{int(wparaList[i]*10000):05}\n")

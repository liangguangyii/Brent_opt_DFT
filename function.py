import os
import math
from fileIO import *
from globalVar import wparaList, J2List, JList, Nspin, Naspin, Nmspin

'''
@brief: read the energy from the Gaussian output file, as a function y(x)

@param wpara: parameter of functional LC-wPBE, as x
@return: J2, as y

@global: Nspin, Naspin, Nmspin
'''

def calIP(wpara):
    global Nspin, Naspin, Nmspin

    g16input(Nspin, Naspin, Nmspin, wpara)
    #* run g16
    #! remove the module load command later
    exitcode1 = os.system("g16 < N.gjf > N.log")
    exitcode2 = os.system("g16 < N+1.gjf > N+1.log")
    exitcode3 = os.system("g16 < N-1.gjf > N-1.log")

    #* check the exit code (non-zero means error)
    if exitcode1 or exitcode2 or exitcode3:
        print("Error in Gaussian16")
        raise Exception("Error: Gaussian doesn't finish correctly. (exitcode does not equal to 0)")

    #* store the output files
    tempstr = f"{int(round(wpara,4)*10000):05}" 
    os.system(f"mkdir {tempstr}")
    os.system(f"cp *.log {tempstr}")

    #* extract the energy
    EN, eN = g16read("N.log")
    ENa, eNa = g16read("N+1.log")
    ENm, eNm = g16read("N-1.log")

    JN = abs(eN + ENm - EN)
    JNa = abs(eNa + EN - ENa)
    J = JN + JNa
    J2 = JN**2 + JNa**2

    return J, J2

'''
@brief: point to the function calIP, only return J2
#! Here wpara -> round(wpara, 4)

@param wpara: parameter of functional LC-wPBE
'''
def funJ2(wpara):
    global wparaList, J2List, JList, Nspin, Naspin, Nmspin
    if round(wpara, 4) in wparaList:
        print(f"Already calculated.{round(wpara, 4)} {wparaList}")
        return J2List[wparaList.index(round(wpara, 4))]
    J, J2 = calIP(wpara)
    wparaList.append(round(wpara, 4))
    JList.append(J)
    J2List.append(J2)
    return J2

'''
@breif: function for debugging
@param x: input
@return y
'''

def fun3(x):
    y = (1.0/3.0)*x**3 - 0.5*x**2 - x - 1.0
    return y

def func(x):
    y = math.cos(x)
    return y
import os

'''
@brief: clean the files in the fileList.txt
'''
def fileClean(filename="fileList.txt"):
    with open(filename, "r") as fileList:
        for line in fileList:
            os.system(f"rm -r {line.strip()}")

'''
@breif: find the spin index in the gjf file
by locating the second blank line index, then add 1

@param filename: default filename is "template.gjf"

@retrun iopIndex: the index of the iop line (start from 1)
@return spinIndex: the index of the spin line (start from 1)
'''
def findSpinIndex(filename = "template.gjf"):

    with open(filename, "r") as gjf:
        icount = 0
        blankCount = 0
        
        for line in gjf:
            icount += 1
            if line == "\n":
                blankCount += 1
            if blankCount == 2:
                spinIndex = icount + 1
                break
        
        iopIndex = spinIndex - 4

    return iopIndex, spinIndex

# '''
# @brief: generate gjf with N+1, N, N-1 spins in different IOp(3/107, 3/108) values (int(wpara*1000):05 + 0:05 format)

# @param Nspin: "charge spin" of N
# @param Naspin: "charge spin" of N+1
# @param Nmspin: "charge spin" of N-1
# @param wpara: the parameter for the IOp(3/107, 3/108) value
# @param filename: the template file name, default is "template.gjf"


# @return: void, three gjf files: N.gjf, N+1.gjf, N-1.gjf
# '''
#! here I use f"{int(wpara*10000):05}" to convert the float to string, by adding 5 zeros
#! it's not good, I suggest to use round(x,4) functon instead

# def g16input(Nspin, Naspin, Nmspin, wpara, filename = "template.gjf"):

#     iopIndex, spinIndex = findSpinIndex()

#     with open("N.gjf", "w") as Ngjf, open("N+1.gjf", "w") as Nagjf, open("N-1.gjf", "w") as Nmgjf:
#         with open(filename, "r") as gjf:
#             icount = 0
#             for line in gjf:
#                 icount += 1
#                 if icount == iopIndex:
#                     tempIop = line.strip()  #*remove the newline character
#                     wpara = round(wpara, 4)    #*round the float to 4 decimal places
#                     str_wpara = f"{int(wpara*10000):05}"   #*convert the float to string, by adding 5 zeros
#                     str_iop = str_wpara + f"{0:05}"
                    
#                     Ngjf.write(f"{tempIop} IOp(3/107={str_iop},3/108={str_iop})\n")
#                     Nagjf.write(f"{tempIop} IOp(3/107={str_iop},3/108={str_iop})\n")
#                     Nmgjf.write(f"{tempIop} IOp(3/107={str_iop},3/108={str_iop})\n")

#                 elif icount == spinIndex:
#                     Ngjf.write(f"{Nspin}\n")
#                     Nagjf.write(f"{Naspin}\n")
#                     Nmgjf.write(f"{Nmspin}\n")
#                 else:
#                     Ngjf.write(line)
#                     Nagjf.write(line)
#                     Nmgjf.write(line)

'''
@brief: generate gjf with series of spins in different IOp(3/107, 3/108) values (int(wpara*1000):05 + 0:05 format)

@param chargeList: the number of eletron corresponding to the template file
@param chargeSpinList: the charge spin list [str1, str2, ...]
@param wpara: the parameter for the IOp(3/107, 3/108) value
@param filename: the template file name, default is "template.gjf"

@return: fileList: the list of the gjf files
@return: void, series of gjf files
'''

def g16input(chargeList, chargeSpinList, wpara, filename = "template.gjf"):
    fileList = []

    iopIndex, spinIndex = findSpinIndex()

    for i in range(len(chargeSpinList)):
        icount = 0
        #* generate the filename
        if chargeList[i] == 0:
            tmpstr = "N.gjf"
        elif chargeList[i] > 0:
            tmpstr = f"N+{chargeList[i]}.gjf"
        else:
            tmpstr = f"N-{abs(chargeList[i])}.gjf"


        with open(filename, "r") as gjf:
            with open(tmpstr, "w") as Ngjf:
                for line in gjf:
                    icount += 1
                    if icount == iopIndex:
                        tempIop = line.strip()  #*remove the newline character
                        wpara = round(wpara, 4)    #*round the float to 4 decimal places
                        str_wpara = f"{int(wpara*10000):05}"   #*convert the float to string, by adding 5 zeros
                        str_iop = str_wpara + f"{0:05}"
                        
                        Ngjf.write(f"{tempIop} IOp(3/107={str_iop},3/108={str_iop})\n")

                    elif icount == spinIndex:
                        Ngjf.write(f"{chargeSpinList[i]}\n")
                    else:
                        Ngjf.write(line)
        
        fileList.append(tmpstr)
    
    return fileList


'''
@brief: read the SCF energy and eigenvalues of HOMO orbital

@param: filename the log file

@return: SCFenergy, eHOMO
'''

#* NOTICE: sometimes there will be not one SCF iterations in a log file,
#* such as stable=opt, and we take the newest values
def g16read(filename):
    success = False

    with open(filename, "r") as log:
        for line in log:
            if "SCF Done" in line:
                templine = line.split()
                SCFenergy = float(templine[4])
            if "Alpha virt. eigenvalues" in line and "Alpha  occ. eigenvalues" in prev_line:
                templine = prev_line.split()
                eHOMO = float(templine[-1])
            #* check if succeed
            if "Normal termination" in line:
                success = True
            prev_line = line    #! prev_line should be updated in the end of line

        if not success:
            raise Exception("Error: Gaussian doesn't finish correctly. (Does not finished normally.)")
    
    return SCFenergy, eHOMO
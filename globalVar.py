wparaList = []
J2List = []
JList = []

cleanBool = False
#!NOTICE: N in line -> N+1 and N-1 also satisfy the condition
#!NOTICE: so it should be "N:" in line

with open("input", "r") as input:
    for line in input:
        if "N+1:" in line:
            templine = line.strip().split()
            Naspin = f"{templine[-2]} {templine[-1]}"
        if "N-1:" in line:
            templine = line.strip().split()
            Nmspin = f"{templine[-2]} {templine[-1]}"
        if "N:" in line:
            templine = line.strip().split()
            Nspin = f"{templine[-2]} {templine[-1]}"
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

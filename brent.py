import os
'''
@breif: parabolic interpolation method
@param x1, y1, x2, y2, x3, y3: three points
@return p, q: x4 = x3 + p/q               
'''

# x3<x2, x1
#x = (x1^2*(y2-y3)+x2^2*(y3-y1)+x3^2*(y1-y2))/(2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)))
#which is invariant under the permutation of the three points
def parabolic_interpolation(x1, y1, x2, y2, x3, y3):
    p = (x2 - x3)**2 * (y3 - y1) + (x1 - x3)**2 * (y2 - y3)
    q = 2.0 * ((x2 - x3) * (y3 - y1) + (x1 - x3) * (y2 - y3))
    return p, q
    
'''
@breif: brent method in one iteration, in one iteration, only one new point is evaluated(fu)

@param a, b: boundary of the interval
@param v, fv: the old value of w
@param w, fw: second least value
@param x, fx: the least value
@param fun_p: the function to be minimized
@param dx: the last step length
@param dxold: the last last step length

@return fv, fw, fx: updated values
@return a, b, v, w, x, dx, dxold: updated values
@return u: last evaluated point
'''

#* here I updated the values of fv, fw, fx to save the computation time, only fu is evaluated in one iteration
def brent(a, b, v, fv, w, fw, x, fx, fun_p, dx, dxold):
    CGOLD = 0.381966013
    xm = 0.5 * (a + b)

    #perform parabolic interpolation using v, w, x (x the minimum point)
    p, q = parabolic_interpolation(v, fv, w, fw, x, fx)

    #Boolean variables for the safety of parabolic interpolation
    #* qSafe: q is not zero
    qSafe = True if (q != 0) else False

    tempdx = p/q if qSafe else 0.0
    #* paraSafe:
    #* 1. q is not zero
    #* 2. the new point is within the interval
    #* 3. the new step length is less than half of the last last step length
    paraSafe = True if (qSafe and (a < x+tempdx) and (x+tempdx < b) and (abs(tempdx) < 0.5*abs(dxold))) else False

    #update the dx and store the last last step length for next iteration

    if paraSafe:
        dxold = dx
        dx = tempdx
    else:
        if x < xm:
            dxold = b - x
        else:
            dxold = a - x
        dx = CGOLD * dxold

    #! evaluate the new point
    u = x + dx
    fu = fun_p(u)

    if (fu < fx):
        #* update the boundary of interval
        a = a if (u < x) else x
        b = x if (u < x) else b
        #* update the values of v, w, x
        v = w
        fv = fw
        w = x
        fw = fx
        x = u
        fx = fu
    else:
        #* update the boundary of interval
        a = u if (u < x) else a
        b = b if (u < x) else u

        #* update the values of v, w, x
        if (fu < fw) or (w == x):
            v = w
            fv = fw
            w = u
            fw = fu
        elif (fu < fv) or (v == x) or (v == w):
            v = u
            fv = fu
    
    return a, b, v, fv, w, fw, x, fx, dx, dxold

'''
@breif: brent method
@param a0, b0: initial boundary of the interval
@param xguess: initial guess of the minimum point
@param fun_p: the function to be minimized
@param tol: tolerance

@return xmin: the minimum point
@return icount: the number of iterations
'''
def brentMethod(a0, b0, xguess, fun_p, tol):
    Maxloop = 1000

    icount = 0
    #! evaluate the function at the initial guess
    y0 = fun_p(xguess)
    a, b, v, fv, w, fw, x, fx, dx, dxold = brent(a0, b0, xguess, y0, xguess, y0, xguess, y0, fun_p, 0.0, 0.0)

    with open("Brent.out", "w") as output:
        output.write(f"{a}\t{b}\t{v}\t{fv}\t{w}\t{fw}\t{x}\t{fx}\t{dx}\t{dxold}\t{tol}\n")
        #* add the flush() to make sure the output is written to the file immediately
        output.flush()
        print(f"Iteration:\t{icount}\tx:\t{x:.5f}\ty:\t{fx:.12f}")

        for i in range(Maxloop):
            a, b, v, fv, w, fw, x, fx, dx, dxold = brent(a, b, v, fv, w, fw, x, fx, fun_p, dx, dxold)
            
            icount += 1
            output.write(f"{a}\t{b}\t{v}\t{fv}\t{w}\t{fw}\t{x}\t{fx}\t{dx}\t{dxold}\t{tol}\n")
            #* add the flush() to make sure the output is written to the file immediately
            output.flush()
            print(f"Iteration:\t{icount}\tx:\t{x:.5f}\ty:\t{fx:.12f}")

            if (abs(b - a) < tol):
                break
            
    return x, icount

'''
@breif: brent method with restart

@param filename: the file name to restart

@return xmin: the minimum point
@return icount: the number of iterations
'''

def brentMethod_re(filename="Brent.out"):
    Maxloop = 1000

    with open("Brent.out", "r") as input:
        for line in input:
            tmpline = line.strip().split()
            tmpline = [float(i) for i in tmpline]
            a, b, v, fv, w, fw, x, fx, dx, dxold, tol = tmpline
        
    print(f"restart from {filename}, with parameters:\n")
    print(f"a:{a}\tb:{b}\tv:{v}\tfv:{fv}\tw:{w}\tfw:{fw}\tx:{x}\tfx:{fx}\ttol:{tol}\n")

    with open("Brent.out", "w") as output:
        output.write(f"a:{a}\tb:{b}\tv:{v}\tfv:{fv}\tw:{w}\tfw:{fw}\tx:{x}\tfx:{fx}\t{tol}\n")
        print(f"Iteration:\t{icount}\tx:\t{x:.5f}\ty:\t{fx:.12f}")

        for i in range(Maxloop):
            a, b, v, fv, w, fw, x, fx, dx, dxold = brent(a, b, v, fv, w, fw, x, fx, fun_p, dx, dxold)
            
            icount += 1
            output.write(f"a:{a}\tb:{b}\tv:{v}\tfv:{fv}\tw:{w}\tfw:{fw}\tx:{x}\tfx:{fx}\t{tol}\n")
            #* add the flush() to make sure the output is written to the file immediately
            output.flush()
            print(f"Iteration:\t{icount}\tx:\t{x:.5f}\ty:\t{fx:.12f}")

            if (abs(b - a) < tol):
                break
            
    return x, icount

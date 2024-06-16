## Optimize the LC range seperated functional

More details about the funtional tuning are given in [Tian Lu's Blog](http://sobereva.com/550).

There is only one parameter ($\omega$) to optimize in the LC range seperated functional. And I choose to use Brent method to find the minimum point of loss funtion:
$$
\begin{aligned}
J_{N}(\omega) & = | \epsilon^{\omega}_{HOMO} (N) + E^{\omega}(N-1) - E^{\omega}(N) | \\
J^{2}(\omega) & = J^{2}_{N}(\omega) + J^{2}_{N+1}(\omega) \\ 
\end{aligned}
$$

The code will generate a series of documents with the name of corresponding $\omega$, all output documents are enclosed in these documents. And the result of each iteration of brent method are both printed and writen into `Brent.out`.

Human-friendly output are shown in `output.txt`.

And `globalVar.py` reads all input parameters (they are all global parameters) from `input`:

```
oldchk
orbit:          0,1
charge spin start
1   -1   2  U
-1  1   2   U
0   0   1
charge spin end
xmin:           0.05
xmax:           0.6
xguess:         0.325
tolerance:      0.001
clean
restart
single point
```

**I Suggest to choose the original w as xmin, when `olachk` is specified, to save computation time.**

Here ``single point``, `oldchk`, `clean`, and `U` in charge spin code area are optional function.

## functions

### helper function

#### `preprocessing`

It's used to search for the spin multiplicity of the system with different charges. 

```
orbit:          -1,1
charge spin start
0	0	3   U
-1	1	4
-1  1   2
-1  1   6
1	-1	4
1	-1	2
charge spin end
xmin:           0.2
xmax:           0.6
xguess:         0.325
tolerance:      0.001
clean
preprocessing
```

When `preprocessing` is given in the `input`, the program will not check the length of `chargeList` and `chargeSpinList`, cause multiple spin multiplicities are given for each charge, besides, the `chargeList` will extend to the length of `chargeSpinList`.

the `chargeSpinList` are sorted by `i` and `spin`, the sorted indies are also the suffix of the gjf files.

#### `single point`

`single point`: calculate the function (J2 and J) for a given x (`xguess`), when `single point` is turned on, brent algorithm, besides with `clean` or other functions related, won't work even if they are specified.

### main function

`oldchk`: add oldchk for each `N+i.gjf` repectively, by default their names are "N+i.chk". Or we could use the same oldchk as `template.gjf` by remove `oldchk`. For both cases, there should be `guess=read` in command line of gjf file.

`restart` will restart the optimization from the last point of the last optimization, it will read the parameters of the last iteration from `Brent.out`.

`clean` will remove all the backup documents, from `fileList.txt`, it only works when `restart` is not specified.

`orbit`: we could tuned MULTIPLE orbitals, by specifying `orbit:    a,b     f,g     ..      x,y`, that will generate gjf files `N+i.gjf`, where i from a to b, f to g, ..., x to y, and they are sorted automatic, besides, duplicate files are removed in `globalVar.py`. **BE NOTICE that N orbits with continous indies mean that N+1 gjf fiels are needed**

For example, `orbit: 0,1` $\rightarrow$ `N-1.gjf` `N.gjf` `N+1.gjf`, and `orbits: 0,1 4,5`
$\rightarrow$ `N-1.gjf` `N.gjf` `N+1.gjf` `N+3.gjf` `N+4.gjf` `N+5.gjf`.

`charge spin start` and `charge spin end` are the start and end of charge spin area.
```
charge spin start
electronNumber  charge  spinMultiplicity    U(optional)
charge spin end
```

if `U` is specified, the U method will be used in Gaussian16 for the corresponding `N+i.gjf`.

Where `N:`, `N+1:`, `N-1:` are the charge+spin multiplicity of systems with corresped electron number. ":" COULD NOT BE OMITTED!

`xmin`,`xmax`,`xguess` are the parameters of brent method. `tolerance` is the convergence condition (|a-b| < tolerance).

And `clean` is an optional funciton, it is used to clean all the backup documents.

## `function.py`
**ALL THE INDEPENDENT VARIABLES ARE ROUNDED TO FOURTH DECIMAL PLACES, AS THIS IS THE HIGHEST PRECISION OF GAUSSIAN16.**

In this file the loss function is calucated. Besides, you could also define your own loss function here, with the format of `def loss(x): return y`.

`calIP` will check the exitcode of Gaussian16, and in `g16read` of `fileIO.py` it will be checked again (wether it's terminated normally).

**New version support the gjf files with IOp, but do place the `functional/basis` part in the front of IOp string,** becasue the code split the command lien by "/" and I assume the first element is functional so that I could add "U" at the biginning of it.


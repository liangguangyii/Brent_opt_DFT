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

And `globalVar.py` reads all input parameters (they are all global parameters) from `input`:

```
N:      0       1
N+1:    -1      2
N-1:    1       2
xmin:           0.05
xmax:           0.6
xguess:         0.325
tolerance:      0.0001
clean
```

Where `N:`, `N+1:`, `N-1:` are the charge+spin multiplicity of systems with corresped electron number. ":" COULD NOT BE OMITTED!

`xmin`,`xmax`,`xguess` are the parameters of brent method. `tolerance` is the convergence condition (|a-b| < tolerance).

And `clean` is an optional funciton, it is used to clean all the backup documents.

## `function.py`
**ALL THE INDEPENDENT VARIABLES ARE ROUNDED TO FOURTH DECIMAL PLACES, AS THIS IS THE HIGHEST PRECISION OF GAUSSIAN16.**

In this file the loss function is calucated. Besides, you could also define your own loss function here, with the format of `def loss(x): return y`.

`calIP` will check the exitcode of Gaussian16, and in `g16read` of `fileIO.py` it will be checked again (wether it's terminated normally).
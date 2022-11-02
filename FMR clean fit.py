# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 12:30:31 2022

@author: Arkaprava Mondal
"""




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import shapely.geometry as SG
from sympy import symbols, solve
import time
from scipy import stats
from scipy.optimize import curve_fit
#slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
start=time.time()
f=pd.read_csv("FMR_Data_R3_5.csv")
X=f["Field"]
Y=f["Combined"]
S=f["Fitted"]
lenX=len(X)
lenY=len(Y)
f1=f[f.columns[1:3]]
M=max(Y)
L=min(Y)
for i in range(1,lenY):
    if Y[i]==M:
        Xmax=X[i]
for i in range(1,lenY):
    if Y[i]==L:
        Xmin=X[i]
dx=Xmax-Xmin
Curve=plt.plot(X, Y) #to plot FMR data
#print(Xmax, Xmin, dx)
print("Linewidth=", dx)
Xslope=stats.linregress(X,Y) 
baseline=Xslope.intercept + Xslope.slope*X
#plt.plot(X, Xslope.intercept + Xslope.slope*X, 'r', label='fitted line')
slope=Xslope.slope
line = SG.LineString(list(zip(X,Y)))
baseline1 = SG.LineString(list(zip(X,baseline)))
coords = np.array(line.intersection(baseline1))

coord=np.delete(coords,1,1)
#plt.scatter(coords[:,0], coords[:,1], s=50, c='orange')

Xres=[]
for i in range(0,len(coord)):
    if (coord[i]<Xmax and coord[i]>Xmin):
        Xres=float(coord[i])

print("Xres=", Xres)

 

# Test function with coefficients as parameters
#def test(x, a, b):
 #   return a * np.sin(b * x)
 
    
def objective(X,K1,K2):
     St1=dx/2
     St2=X-Xres
     T1=(St1*St2)/(((St1**2)+(St2**2))**2)
     T2=((St1**2)-(St2**2))/(((St1**2)+(St2**2))**2)+(X*slope)
     return (K1*T1+K2*T2)
    
# curve_fit() function takes the test-function
# x-data and y-data as argument and returns
# the coefficients a and b in param and
# the estimated covariance of param in param_cov
#param, param_cov = curve_fit(test, x, y)

popt, Fit_final = curve_fit(objective, X, Y)
# summarize the parameter values
print(popt)
K1=popt[0]
K2=popt[1]
# define a sequence of inputs between the smallest and largest known inputs

St1=dx/2
St2=X-Xres
T1=(St1*St2)/(((St1**2)+(St2**2))**2)
T2=((St1**2)-(St2**2))/(((St1**2)+(St2**2))**2)+(X*slope)

final_ans = popt[0]*T1+popt[1]*T2
# create a line plot for the mapping function
#plt.plot(X, y_line, '--', color='red')
print("K1=", K1, "K2=", K2)


plt.plot(X, Y, color ="red", label ="data") #plot data
#plt.scatter(Xres, 0, s=10, c='black')
plt.plot(X, final_ans, '-', color ='black', label ="optimized data") #
plt.legend()
#plt.savefig("FMR_Data_R3_8.png",dpi=3000)
#plt.show()

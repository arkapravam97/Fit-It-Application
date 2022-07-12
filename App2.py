# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:20:46 2022

@author: Arkaprava Mondal
"""


import tkinter as tk
from tkinter.filedialog import askopenfile 
import pandas as pd
import numpy as np
import shapely.geometry as SG
from scipy import stats
from scipy.optimize import curve_fit
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)


#Window
root = tk.Tk()
root.withdraw()
win=tk.Toplevel()
win.title('Fit It!')
win.geometry("1250x800")
entry=tk.Entry(win)
win.configure(background='#856ff8')

img =tk.PhotoImage(file="D:\Documents_D\Img\Logo10.png")
img1=tk.Label(win,image=img)
img1.grid(row = 0, column = 5)
img1.config(bg='#856ff8')
win.iconphoto(False, img)


Pad1=tk.Label(win,text='    ')
Pad1.grid(column=0, row=0)
Pad1.config(bg='#856ff8')
Pad2=tk.Label(win,text='____________________________________________________',fg='#856ff8')
Pad2.grid(column=1, row=0)
Pad2.config(bg='#856ff8')
Pad3=tk.Label(win,text='______________________________',fg='#856ff8')
Pad3.grid(column=2, row=0)
Pad3.config(bg='#856ff8')
Pad4=tk.Label(win,text='             Fit it !!                                        ',fg='white',font=("Harlow Solid Italic",30,"bold"))
Pad4.grid(column=3, row=0)
Pad4.config(bg='#856ff8')
FD=tk.Label(win,text='FMR Data in csv file format',fg='white',font=("Kabel",15,"bold"))
FD.grid(column=1, row=1,pady=0)
FD.config(bg='#856ff8')
FDbtn=tk.Button(win,text ='Choose File',command = lambda:open_file() ) 
FDbtn.grid(column=2, row=1,pady = 2)
btn1 = tk.Button(win, text = 'Quit !',bg="red",fg="white",font="bold", command = lambda:root.destroy() & win.destroy())
btn1.grid(row = 6, column = 5, pady =2)



def open_file():
    file_path = askopenfile(mode='r', filetypes=[('FMR csv file', '*csv')])
    if file_path is not None:
        f=pd.read_csv(file_path)
        X=f["Field"]
        Y=f["Combined"]
        lenY=len(Y)
        M=max(Y)
        L=min(Y)
        for i in range(1,lenY):
            if Y[i]==M:
                Xmax=X[i]
        for i in range(1,lenY):
            if Y[i]==L:
                Xmin=X[i]
        dx=Xmax-Xmin
        print("Linewidth=", dx)
        Xslope=stats.linregress(X,Y) # to fit straight line or baseline
        baseline=Xslope.intercept + Xslope.slope*X
        slope=Xslope.slope
        line = SG.LineString(list(zip(X,Y)))
        baseline1 = SG.LineString(list(zip(X,baseline)))
        coords = np.array(line.intersection(baseline1))
        coord=np.delete(coords,1,1)
        Xres=[]
        for i in range(0,len(coord)):
            if (coord[i]<Xmax and coord[i]>Xmin):
                Xres=float(coord[i])
        print("Xres=", Xres)
        def objective(X,K1,K2):
             St1=dx/2
             St2=X-Xres
             T1=(St1*St2)/(((St1**2)+(St2**2))**2)
             T2=((St1**2)-(St2**2))/(((St1**2)+(St2**2))**2)+(X*slope)
             return (K1*T1+K2*T2)
        popt, Fit_final = curve_fit(objective, X, Y)
        print(popt)
        K1=popt[0]
        K2=popt[1]
        St1=dx/2
        St2=X-Xres
        T1=(St1*St2)/(((St1**2)+(St2**2))**2)
        T2=((St1**2)-(St2**2))/(((St1**2)+(St2**2))**2)+(X*slope)
        final_ans = popt[0]*T1+popt[1]*T2
        print("K1=", K1, "K2=", K2)
                
        fig = Figure(figsize = (7, 6),dpi = 100)
        frame=tk.Frame(win)
        frame.grid(row=6, column=3, pady = 2)
        frame.config(bg='#856ff8')
        plt1 = fig.add_subplot(111)
        plt1.plot(X, Y, 'o', color ="red", label ="data") #plot data
        plt1.scatter(Xres, 0, s=50, c='black')
        plt1.plot(X, final_ans, '-', color ='blue', label ="optimized data") #
        plt1.legend()
        canvas = FigureCanvasTkAgg(fig,master = win)
        canvas.draw()
        toolbar=NavigationToolbar2Tk(canvas,frame)
        toolbar.config(bg='#856ff8')
        canvas.get_tk_widget().grid(row=5, column=3, pady = 0)
     
        
        R=tk.Text(win, width=30, height=37)
        R.grid(column=1, row=5, pady = 2)
        def printit():
            R.insert(tk.END,"K1="+str(K1)+"\n")
            R.insert(tk.END,"K2="+str(K2)+"\n")
            R.insert(tk.END,"Xres=="+str(Xres)+"\n")
            R.insert(tk.END,"Linewidth="+str(dx)+"\n")
        Results = tk.Button(win,text ='Show Results',font=("Kabel",12,"bold"),height=5,width=12,command = lambda:printit() ) 
        Results.grid(column=2, row=5, pady = 2) 
        
        
        pass 

win.mainloop()
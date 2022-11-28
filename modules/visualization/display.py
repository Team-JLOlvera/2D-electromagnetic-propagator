"""
Bscan image shows
"""
#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


#======================================================================================================
# function
#======================================================================================================

def data_raw(data2D,save=False):

    data = np.copy(data2D)

    fig = plt.figure('B-scan')
    axes = fig.add_axes([0.15,0.15,0.8,0.8])
    axes.tick_params(axis='both', labelsize=16, length=5, width=1.5, colors='black', grid_color='gray', grid_alpha=0.5)
    #axes.set_xlim([0, 5 ])


    #axis
    x = np.array(range(data.shape[1]))
    y = np.arange(0,data.shape[0]*(1.66782e-11)*1e9,(1.66782e-11)*1e9)
    X, Y = np.meshgrid(x, y)

    #image
    cs = axes.contourf(data,levels=150,cmap=cm.gray) # white lows and black highs cm.twilight
    plt.colorbar(cs)


    plt.xlabel('Número de trasas A-scan',fontsize=19)
    plt.ylabel('Muestras ',fontsize=19)
    ax = plt.gca() 
    ax.invert_yaxis() 
    if save:
        plt.savefig("b-scan-raw.jpg",dpi=400)
    plt.show()

#=====================================================================================================================

def imagen_Bscan(data2D,dt,save=False):

    data = np.copy(data2D)
    discretization_time = dt 

    fig = plt.figure('B-scan')
    axes = fig.add_axes([0.15,0.15,0.8,0.8])
    axes.tick_params(axis='both', labelsize=16, length=5, width=1.5, colors='black', grid_color='gray', grid_alpha=0.5)
    #axes.set_xlim([0, 5 ])


    #axis
    x = np.array(range(data.shape[1]))
    y = np.arange(0,data.shape[0]*(discretization_time )*1e9,(discretization_time )*1e9)
    X, Y = np.meshgrid(x, y)

    #image
    cs = axes.contourf(X, Y, data,levels=150,cmap=cm.gray) # white lows and black highs cm.twilight
    plt.colorbar(cs)


    plt.xlabel('Número de trasas A-scan',fontsize=19)
    plt.ylabel('Tiempo (ns) ',fontsize=19)
    ax = plt.gca() 
    ax.invert_yaxis() 
    if save:
        plt.savefig("b-scan.jpg",dpi=400)
    plt.show()    
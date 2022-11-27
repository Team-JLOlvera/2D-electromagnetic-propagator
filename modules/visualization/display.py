"""
Bscan image shows
"""
#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

import matplotlib.pyplot as plt


#======================================================================================================
# function
#======================================================================================================

def data_raw(data2D):

    plt.contourf(data2D,levels=65)
    #plt.axis('off')
    plt.title('Bscan data of a cylinder')
    plt.colorbar()
    plt.xlabel('Number of traces')
    plt.ylabel('Time')
    ax = plt.gca() 
    ax.invert_yaxis() 
    plt.show()
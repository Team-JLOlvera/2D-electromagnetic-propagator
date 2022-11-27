
"""
has two functions:
1) FDTD modeling
2) PML absorbent barrier
"""

#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

import numpy as np
from math import  sqrt
from tqdm import tqdm
from numba import njit, jit
import warnings
warnings.filterwarnings("ignore")


#======================================================================================================
# Absorbent barrier
#======================================================================================================
@jit
def PML(model_feature):


    # Variables of interes:
    x_model = model_feature['model_size_in_x']
    y_model = model_feature['model_size_in_y']


    # Initialization of the PML parameters
    gi2 = np.ones(y_model)
    gi3 = np.ones(y_model)
    fi1 = np.zeros(y_model)
    fi2 = np.ones(y_model)
    fi3 = np.ones(y_model)

    gj2 = np.ones(x_model)
    gj3 = np.ones(x_model)
    fj1 = np.zeros(x_model)
    fj2 = np.ones(x_model)
    fj3 = np.ones(x_model)

    # PM creation
    npml = 8 # how many yee cells does it take

    for n in range(npml):
        xnum = npml - n
        xd = npml
        xxn = xnum / xd
        xn = 0.33 * xxn ** 3
        gi2[n] = 1 / (1 + xn)
        gi2[y_model - 1 - n] = 1 / (1 + xn)
        gi3[n] = (1 - xn) / (1 + xn)
        gi3[y_model - 1 - n] = (1 - xn) / (1 + xn)
        gj2[n] = 1 / (1 + xn)
        gj2[x_model - 1 - n] = 1 / (1 + xn)
        gj3[n] = (1 - xn) / (1 + xn)
        gj3[x_model - 1 - n] = (1 - xn) / (1 + xn)
        
        xxn = (xnum - 0.5) / xd
        xn = 0.33 * xxn ** 3
        fi1[n] = xn
        fi1[y_model - 2 - n] = xn
        fi2[n] = 1 / (1 + xn)
        fi2[y_model - 2 - n] = 1 / (1 + xn)
        fi3[n] = (1 - xn) / (1 + xn)
        fi3[y_model - 2 - n] = (1 - xn) / (1 + xn)
        fj1[n] = xn
        fj1[x_model - 2 - n] = xn
        fj2[n] = 1 / (1 + xn)
        fj2[x_model - 2 - n] = 1 / (1 + xn)
        fj3[n] = (1 - xn) / (1 + xn)
        fj3[x_model - 2 - n] = (1 - xn) / (1 + xn)

    return (gi2,gi3,gj2,gj3,fi1,fi2,fi3,fj1,fj2,fj3)

#======================================================================================================
# FDTD
#======================================================================================================

@jit
def propagate2D(model_feature, simulation_parameters,obj_waveform,PML_parameters,mediums):

    #======================================================================================================
    # Variable initialization
    #======================================================================================================

    gaz, gbz = mediums   
    gi2, gi3, gj2, gj3, fi1,fi2,fi3,fj1,fj2,fj3 = PML_parameters

    number_steps_antenna = simulation_parameters['antenna_steps']
    time_window = simulation_parameters['time_window']
    electric_field_z = np.zeros((time_window+1,number_steps_antenna))

    # dictionary:
    x_model = model_feature['model_size_in_x']
    y_model = model_feature['model_size_in_y']
    position_TX_y = model_feature['position_TX_y']
    position_TX_x = model_feature['position_TX_x']
    position_RX_y = model_feature['position_RX_y']
    position_RX_x = model_feature['position_RX_x']

    # constant
    C = 299792458 # speed of light (m/s)
    DELTA_T = model_feature['discretization_x']/int(2*C) # time discretization

    #======================================================================================================
    # propagator 2D
    #======================================================================================================

    for steps in range(number_steps_antenna):  
    
        # variable initialization
        ez = np.zeros((y_model, x_model)) 
        ix = np.zeros((y_model, x_model))
        dz = np.zeros((y_model, x_model))
        hx = np.zeros((y_model, x_model))
        hy = np.zeros((y_model, x_model))
        ihx = np.zeros((y_model, x_model))
        ihy = np.zeros((y_model, x_model))   
             
    
        loop = tqdm(total=time_window+1,position=0,leave=False)

        # Main FDTD Loop
        for time_step in range(1, time_window + 1):

            

            # process visualization
            loop.set_description(f'A-scan trace {steps} of {number_steps_antenna} '.format(time_step))
            loop.update(1)

            # calculation of Dz
            for j in range(1, x_model):
                for i in range(1, y_model):
                    dz[i, j] = gi3[i] * gj3[j] * dz[i, j] + gi2[i] * gj2[j] * 0.5*(hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])
                    
            # source:                
            pulse = obj_waveform.transmitted_pulse(time_step,DELTA_T ) 
            dz[position_TX_y, position_TX_x+steps] = pulse
                
            
            # Ez field calculation
            for j in range(1, x_model):
                for i in range(1, y_model):
                    ez[i,j] = gaz[i,j] * (dz[i,j]-ix[i,j]) 
                    ix[i,j] = ix[i,j] + gbz[i,j]*ez[i,j]
                    
            # calculation of the Hx field
            for j in range(x_model - 1):
                for i in range(y_model - 1):
                    curl_e = ez[i, j] - ez[i, j + 1]
                    ihx[i, j] = ihx[i, j] + curl_e
                    hx[i, j] = fj3[j] * hx[i, j] + fj2[j] *(0.5 * curl_e + fi1[i] * ihx[i, j])
                        
            # calculation of the field hy
            for j in range(0, x_model - 1):
                for i in range(0, y_model - 1):
                    curl_e = ez[i, j] - ez[i + 1, j]
                    ihy[i, j] = ihy[i, j] + curl_e
                    hy[i, j] = fi3[i] * hy[i, j] - fi2[i] *(0.5 * curl_e + fj1[j] * ihy[i, j])
                    
                    
            # Save field to receiver location
            electric_field_z[time_step-1,steps] = ez[position_RX_y,position_RX_x +steps]

        loop.close()

        # save data 
        np.save('field_Ez.npy',electric_field_z)

    # save data 
    time_image = np.arange(DELTA_T,time_window*DELTA_T,DELTA_T )
    np.save('time.npy',time_image)
    return electric_field_z
            







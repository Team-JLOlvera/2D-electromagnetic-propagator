"""
a code to read electric field and time from .npy files
"""

#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

import numpy as np


# Import modules
import importlib
import modules
importlib.reload(modules)

# modules 

import modules.visualization.display as visualization

#===========================================================================
# 1) upload files
#===========================================================================
name_file_field = 'field_Ez.npy'
name_file_time = 'time.npy'

data_raw = np.load(name_file_field)
time = np.load(name_file_time)

#===========================================================================
# 1) visualizacion 
#===========================================================================
new_data = data_raw[0:221,:]
dt = time[4]-time[3]
visualization.imagen_Bscan(new_data,dt,save=True)




"""
create the GPR model and run the simulation
"""

#======================================================================================================
# Libraries
#======================================================================================================

# Import modules
import importlib
import modules
importlib.reload(modules)

# modules 

import modules.interface.user_message as message

import modules.images_Bscan.formation_Bscan as electromagnetic_simulation


#======================================================================================
# 1) model dimensions
#======================================================================================

model_features = {
    'discretization_x': 0.01, # meters
    'model_size_in_x': 100, # points
    'model_size_in_y': 60, #points
    'position_TX_y': 50, #points
    'position_TX_x': 10,  #points
    'position_RX_y': 50, #points
    'position_RX_x': 14, #points
}

#======================================================================================
# 2) simulation parameters
#======================================================================================
simulation_parameters = {
    'antenna_steps': 80,
    'time_window': 420
}

#======================================================================================
# 3) waveform
#======================================================================================
waveform_characteristics = {
    'frequency': 1.6e9, #Hz
    'type': 'ricker'

}
#======================================================================================
# 4) creation of objects
#======================================================================================

dict_box = {
    'type' : 'box',
    'location_at_x': 0, #points
    'location_at_y': 50, #points
    'conductivity': 0,  #s/m
    'relative permittivity': 6 
}

dict_cylinder = {
    'type': 'cylinder',
    'location_at_x': 50, #points
    'location_at_y': 25, #points
    'conductivity': 0.0003, #s/m
    'relative permittivity': 15,
    'radius': 10 #points

}

list_objects = [dict_box,dict_cylinder]

#======================================================================================
# 5) run program
#======================================================================================

electromagnetic_simulation.generation_Bscan(model_features,simulation_parameters,waveform_characteristics,list_objects)


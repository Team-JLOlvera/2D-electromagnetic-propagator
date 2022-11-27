"""
This code joins all the parts to generate a Bscan image

"""

#======================================================================================================
# Libraries
#======================================================================================================
#libraries 
import time

from numba import jit
import warnings
warnings.filterwarnings("ignore")


# Import modules
import importlib
import modules
importlib.reload(modules)

# modules 

import modules.interface.user_message as message
import modules.propagator.propagator2D as propagator
import modules.objets.join_objects as join
import modules.visualization.display as visualization

#classes

from modules.pulses.waveform import Waveform


#====================================================================================
# formation of B-scan images
#======================================================================================
@jit
def generation_Bscan (model_features,simulation_parameters,waveform_characteristics,objects ):

    dict_model_features = model_features
    dict_simulation_parameters = simulation_parameters
    dict_waveform_characteristics = waveform_characteristics 
    list_objects = objects

    #======================================================================================
    # 1) initial message
    #======================================================================================
    message.initial_message()

    #======================================================================================
    # 2) message with model characteristics
    #======================================================================================
    message.model_features_message (dict_model_features)

    #======================================================================================
    # 3) creation PML
    #======================================================================================
    parameters_PML =  propagator.PML(dict_model_features)

    #======================================================================================
    # 4) initialize the object for the pulse
    #======================================================================================
    source = Waveform (dict_waveform_characteristics)

    #======================================================================================
    # 5) object creation in the subsurface
    #======================================================================================
    complete_model = join.add_objects(dict_model_features,list_objects )

    #======================================================================================
    # 6) run the propagator
    #======================================================================================
    start = time.time()      
    electric_field_at_z = propagator.propagate2D(dict_model_features,dict_simulation_parameters,source,parameters_PML,complete_model)
    end  = time.time()
    simulation_time= end-start

    #======================================================================================
    # 7) run the propagator
    #======================================================================================
    message.final_message(simulation_time)

    #======================================================================================
    # 8) show image
    #======================================================================================
    visualization.data_raw(electric_field_at_z)
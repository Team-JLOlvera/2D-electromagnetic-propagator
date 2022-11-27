"""
the model is generated with the proposed object

"""

#======================================================================================================
# Libraries
#======================================================================================================

# Import modules
import importlib
import modules
importlib.reload(modules)


# classes 
from modules.objets.creation_objects import Creation_objects

#======================================================================================================
# function
#======================================================================================================

def add_objects (model_features,objects):

    # variable initialization
    dict_model_features = model_features
    list_objects = objects

    complete_model = Creation_objects(dict_model_features)

    
    number_of_objects = len(list_objects)

    for i in range(number_of_objects):
        dict_object = list_objects[i]
        label = dict_object['type']

        if label == 'box':
            medium = complete_model.box(dict_object)
        elif label == 'cylinder':
            medium = complete_model.cylinder(dict_object)
        else: 
            print('the list of objects has the wrong type')

    return medium


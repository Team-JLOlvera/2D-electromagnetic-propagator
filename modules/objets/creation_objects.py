"""
Add two types of objects:
1) rectangles
2) cylinders
"""
#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

import numpy as np
from math import  sqrt


#===========================================================================
# Class 
#===========================================================================

class Creation_objects:

    def __init__(self,model_features):

        self.size_in_x = model_features['model_size_in_x']
        self.size_in_y = model_features['model_size_in_y']
        self.DDX = model_features['discretization_x'] # spatial discretization
        self.gaz = np.ones((self.size_in_y, self.size_in_x))
        self.gbz = np.zeros((self.size_in_y, self.size_in_x))

        self.structure_name ={}        
        self.C = 299792458 # speed of light [m/s]
        self.DT = self.DDX/int(2*self.C) # time discretization
        self.EPSZ = 8.8541e-12        


    # def add_structure(self, structure, model_features):

    #     x_dimensional = model_features['location_in_x']
    #     y_dimensional = model_features ['location_in_y']
    #     conductivity = model_features['conductivity']
    #     relative_permittivity = model_features['relative_permittivity']

    #     try: 
    #         radius = model_features['radius']
    
    #     except KeyError:
    #         radius = None
        

    #     information_tuple = (x_dimensional, y_dimensional,conductivity, relative_permittivity,radius)
    #     self.structure_name[structure] = information_tuple
        
    def box(self,structure):

        # Creation of the dielectric profile
        epsr = structure ['relative permittivity']
        sigma = structure ['conductivity']
        medium_start_row = structure ['location_at_x']
        medium_start_column = structure ['location_at_y']

        self.gaz[0:medium_start_row,medium_start_column:] = 1 / (epsr + (sigma * self.DT / self.EPSZ))
        self.gbz[0:medium_start_row,medium_start_column:] = sigma * self.DT / self.EPSZ

        return (self.gaz, self.gbz)
    
    def cylinder(self,structure):
        ia = 7 
        ja  = 7
        ib = self.size_in_y  -8
        jb = self.size_in_x  - 8

        # creation of the dielectric profile
        x_object = structure ['location_at_x']
        y_object = structure ['location_at_y']
        epsr = structure ['relative permittivity']
        sigma = structure ['conductivity']
        radius = structure ['radius']


        for j in range(ja, jb):
            for i in range(ia, ib):
                xdist = (y_object - i)
                ydist = (x_object - j)
                dist = sqrt(xdist ** 2 + ydist ** 2)
                if dist <= radius:
                    self.gaz[i, j] = 1 / (epsr + (sigma * self.DT / self.EPSZ))
                    self.gbz[i, j] = (sigma * self.DT / self.EPSZ)
                    
        return (self.gaz, self.gbz)
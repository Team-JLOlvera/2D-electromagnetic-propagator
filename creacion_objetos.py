"""
====================================================
Agrega dos tipos de objetos:
1) rectangulos
2) cilindros
=====================================================
"""


import numpy as np
from math import  sqrt

class Creacion_objetos:

    def __init__(self,caracteristicas_modelo):

        self.tamano_en_x = caracteristicas_modelo['tamano_modelo_en_x']
        self.tamano_en_y = caracteristicas_modelo['tamano_modelo_en_y']
        self.gaz = np.ones((self.tamano_en_y, self.tamano_en_x ))
        self.gbz = np.zeros((self.tamano_en_y, self.tamano_en_x))

        self.nombre_estructura ={}
        self.DDX = 0.01 # discretizacion espacial
        self.C = 299792458 # velocidad de la luz [m/s]
        self.DT = self.DDX/int(2*self.C) # discretizacion temporal
        self.EPSZ = 8.8541e-12

    def anadir_estructura(self, estructura, caracteristicas_estructura):

        dimension_x = caracteristicas_estructura['ubicacion_en_x']
        dimension_y = caracteristicas_estructura ['ubicacion_en_y']
        conductividad = caracteristicas_estructura['conductividad']
        permitividad_relativa = caracteristicas_estructura['permitividad_relativa']

        try: 
            radio = caracteristicas_estructura['radio']
    
        except KeyError:
            radio = None
        

        tupla = (dimension_x, dimension_y,conductividad, permitividad_relativa,radio)
        self.nombre_estructura [estructura] = tupla
        
    def caja (self,estructura):

        # Creacion del perfil dielectrico
        epsr = self.nombre_estructura[estructura][3]
        sigma = self.nombre_estructura[estructura][2]
        medio_start_fila = self.nombre_estructura[estructura][1]
        medio_start_columna = self.nombre_estructura[estructura][0]

        self.gaz[0:medio_start_fila,medio_start_columna:] = 1 / (epsr + (sigma * self.DT / self.EPSZ))
        self.gbz[0:medio_start_fila,medio_start_columna:] = sigma * self.DT / self.EPSZ

        return (self.gaz, self.gbz)
    
    def cilindro(self,estructura):
        ia = 7 
        ja  = 7
        ib = self.tamano_en_y -8
        jb = self.tamano_en_x - 8

        # creacion del perfil dielectrico
        x_objeto = self.nombre_estructura[estructura][0]
        y_objeto = self.nombre_estructura[estructura][1]
        epsr = self.nombre_estructura[estructura][3]
        sigma = self.nombre_estructura[estructura][2]
        radius = self.nombre_estructura[estructura][4]


        for j in range(ja, jb):
            for i in range(ia, ib):
                xdist = (y_objeto - i)
                ydist = (x_objeto - j)
                dist = sqrt(xdist ** 2 + ydist ** 2)
                if dist <= radius:
                    self.gaz[i, j] = 1 / (epsr + (sigma * self.DT / self.EPSZ))
                    self.gbz[i, j] = (sigma * self.DT / self.EPSZ)
                    
        return (self.gaz, self.gbz)
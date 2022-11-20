
"""
=================================================================
tiene dos funciones:
1) El modelado FDTD
2) la barrera absorbente PML
=================================================================
"""

import numpy as np
from mensajes_usuario import Mensajes_usuario


class Propagador_2D_GPR:

    def __init__(self,caracteristicas_modelo):
        
        self.size_x = caracteristicas_modelo['tamano_modelo_en_x']
        self.size_y = caracteristicas_modelo['tamano_modelo_en_y']
        self.delta_x = caracteristicas_modelo['discretizacion_en_x']

        self.posicion_TX_x = caracteristicas_modelo['posicion_antena_transmision_x']
        self.posicion_TX_y = caracteristicas_modelo['posicion_antena_transmision_y']
        self.posicion_RX_x = caracteristicas_modelo['posicion_antena_recepcion_x']
        self.posicion_RX_y = caracteristicas_modelo['posicion_antena_recepcion_y']
        self.caracteristicas_modelo = caracteristicas_modelo

        
        self.C = 299792458 # velocidad de la luz [m/s]
        self.DELTA_T = self.delta_x/int(2*self.C) # discretizacion temporal

    def propagar(self, parametros_simulacion,forma_de_onda,parametros_PML,medios):

        gaz, gbz = medios    
        gi2, gi3, gj2, gj3, fi1,fi2,fi3,fj1,fj2,fj3 = parametros_PML

        numero_pasos_antena = parametros_simulacion['pasos_de_la_antena']
        ventana_tiempo = parametros_simulacion['ventana_tiempo']
        campo_electrico_Z = np.zeros((ventana_tiempo+1,numero_pasos_antena))

        x_modelo = self.size_x
        y_modelo = self.size_y


        for pasos in range(numero_pasos_antena):  
        
            #inicializacion de variables 
            ez = np.zeros((y_modelo, x_modelo)) 
            ix = np.zeros((y_modelo, x_modelo))
            dz = np.zeros((y_modelo, x_modelo))
            hx = np.zeros((y_modelo, x_modelo))
            hy = np.zeros((y_modelo, x_modelo))
            ihx = np.zeros((y_modelo, x_modelo))
            ihy = np.zeros((y_modelo, x_modelo))            
      
        
            # Main FDTD Loop
            for time_step in range(1, ventana_tiempo + 1):
                # calculo de  Dz
                for j in range(1, x_modelo):
                    for i in range(1, y_modelo):
                        dz[i, j] = gi3[i] * gj3[j] * dz[i, j] + gi2[i] * gj2[j] * 0.5*(hy[i, j] - hy[i - 1, j] - hx[i, j] + hx[i, j - 1])
                        
                # fuente                   
                #pulse = forma_de_onda.sixth_der_gaussiana(time_step) 3 para datos reales
                pulse = forma_de_onda.ricker(time_step,self.DELTA_T ) # para ecuaciones
                dz[self.posicion_TX_y, self.posicion_TX_x+pasos] = pulse
                    
                
                #calculo del campo Ez
                for j in range(1, x_modelo):
                    for i in range(1, y_modelo):
                        ez[i,j] = gaz[i,j] * (dz[i,j]-ix[i,j]) 
                        ix[i,j] = ix[i,j] + gbz[i,j]*ez[i,j]
                        
                # calculo del campo Hx
                for j in range(x_modelo - 1):
                    for i in range(y_modelo - 1):
                        curl_e = ez[i, j] - ez[i, j + 1]
                        ihx[i, j] = ihx[i, j] + curl_e
                        hx[i, j] = fj3[j] * hx[i, j] + fj2[j] *(0.5 * curl_e + fi1[i] * ihx[i, j])
                            
                # calculo del campo hy
                for j in range(0, x_modelo - 1):
                    for i in range(0, y_modelo - 1):
                        curl_e = ez[i, j] - ez[i + 1, j]
                        ihy[i, j] = ihy[i, j] + curl_e
                        hy[i, j] = fi3[i] * hy[i, j] - fi2[i] *(0.5 * curl_e + fj1[j] * ihy[i, j])
                        
                        
                #Guardar el  campo en la ubicacion del receptor
                campo_electrico_Z[time_step-1,pasos] = ez[self.posicion_RX_y,self.posicion_RX_x+pasos]

            #mensaje para usuario:   
            Mensajes_usuario(self.caracteristicas_modelo).mensaje_proceso(numero_pasos_antena,pasos)

        return campo_electrico_Z
            
    def PML(self):

        x_modelo =self.size_x
        y_modelo = self.size_y

        # Inicializacion de los parametros de la PML
        gi2 = np.ones(y_modelo)
        gi3 = np.ones(y_modelo)
        fi1 = np.zeros(y_modelo)
        fi2 = np.ones(y_modelo)
        fi3 = np.ones(y_modelo)

        gj2 = np.ones(x_modelo)
        gj3 = np.ones(x_modelo)
        fj1 = np.zeros(x_modelo)
        fj2 = np.ones(x_modelo)
        fj3 = np.ones(x_modelo)

        # creacion de la PML
        npml = 8 #cuantas celdas de yee toma

        for n in range(npml):
            xnum = npml - n
            xd = npml
            xxn = xnum / xd
            xn = 0.33 * xxn ** 3
            gi2[n] = 1 / (1 + xn)
            gi2[y_modelo - 1 - n] = 1 / (1 + xn)
            gi3[n] = (1 - xn) / (1 + xn)
            gi3[y_modelo - 1 - n] = (1 - xn) / (1 + xn)
            gj2[n] = 1 / (1 + xn)
            gj2[x_modelo - 1 - n] = 1 / (1 + xn)
            gj3[n] = (1 - xn) / (1 + xn)
            gj3[x_modelo - 1 - n] = (1 - xn) / (1 + xn)
            
            xxn = (xnum - 0.5) / xd
            xn = 0.33 * xxn ** 3
            fi1[n] = xn
            fi1[y_modelo - 2 - n] = xn
            fi2[n] = 1 / (1 + xn)
            fi2[y_modelo - 2 - n] = 1 / (1 + xn)
            fi3[n] = (1 - xn) / (1 + xn)
            fi3[y_modelo - 2 - n] = (1 - xn) / (1 + xn)
            fj1[n] = xn
            fj1[x_modelo - 2 - n] = xn
            fj2[n] = 1 / (1 + xn)
            fj2[x_modelo - 2 - n] = 1 / (1 + xn)
            fj3[n] = (1 - xn) / (1 + xn)
            fj3[x_modelo - 2 - n] = (1 - xn) / (1 + xn)

        return (gi2,gi3,gj2,gj3,fi1,fi2,fi3,fj1,fj2,fj3)
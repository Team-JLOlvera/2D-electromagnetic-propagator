"""
===============================================================
tiene diferentes formas de ondas implementadas 
para el uso en el propagador

*sinusoidal
*chirp
*gaussiana
*primera derivada del pulso gaussiana
*ricker

===============================================================
"""


from math import exp, pi,sqrt 
import scipy.io as sio
import numpy as np

class Forma_de_onda:

    def __init__(self, caracteristicas_forma_de_onda):
        self.frecuencia = caracteristicas_forma_de_onda['frecuencia']
             
    def sinusoidal(self,time_step,delta_t):
        
        w = 2*np.pi*self.frecuencia 
        signal_sinusoidal = np.sin(w*delta_t*time_step)

        return signal_sinusoidal    

    def chirp(self,time_step,delta_t):
        #==============================================================
        #modificable por el usuario:
        ventana_tiempo = 200
        fase_inicial= 0 #radianes 
        frecuencia_final = 5.2e9
        #===============================================================
        
        frecuencia_inicial = self.frecuencia        
        tiempo_barrido = ventana_tiempo * delta_t
        constante_c = (frecuencia_final-frecuencia_inicial )/ tiempo_barrido       
        tiempo = time_step*delta_t

        signal_chirp = np.sin(fase_inicial+(2*np.pi*(((constante_c*tiempo**2)/2)+frecuencia_inicial*tiempo)))

        return signal_chirp
       

       
    def gaussiana(self, time_step,delta_t):

        sita = 2*(pi**2)*(self.frecuencia)**2
        equis = 1/self.frecuencia
        tiempo = time_step*delta_t
        
        pulse = exp(-1*sita*(tiempo-equis)**2)
        
        return pulse

    
    def first_der_gaussiana(self,time_step,delta_t):

        sita = 2*(pi**2)*(self.frecuencia)**2
        equis = 1/self.frecuencia
        tiempo = time_step*delta_t

        pulse = -2 *sqrt(exp(1)/(2*sita))*sita*(tiempo-equis)*exp(-1*sita*(tiempo-equis)**2)

        return pulse

    def ricker(self,time_step,delta_t):

        sita = (pi**2)*(self.frecuencia)**2
        equis = sqrt(2) /self.frecuencia
        tiempo = time_step*delta_t

        pulse = -1*((2*sita*((tiempo-equis)**2))-1)*exp(-1*sita*(tiempo-equis)**2)

        return pulse

    def fourth_der_gaussiana(self,time_step):
        #======================================================================
        # columna 0 = tiempo
        # columna 1 = 0.5 ns
        # columna 2 = 1 ns
        # columna 3 = 1.5 ns 
        # columna 4 = 2 ns 
        #======================================================================

        datos_cuarta_derivada = sio.loadmat('pulso_cuarta_derivada_pos.mat')
        pulso_cuarta_derivada = datos_cuarta_derivada['alfa']
        
        #borrar filas 
        indices_eliminar = np.arange(0,401) # filas que quiero borrar 
        pulso_cuarta_derivada = np.delete(pulso_cuarta_derivada, indices_eliminar, axis=0) # 0 = borrar filas y 1 = borra columnas

        #agregar filas 
        indices_agregar = len(pulso_cuarta_derivada)
        valores = [pulso_cuarta_derivada[indices_agregar-1,i] for i in range(0,5)]
        valores_agregar = np.full((401, 5),valores)
        pulso_cuarta_derivada = np.insert(pulso_cuarta_derivada, indices_agregar,valores_agregar, axis=0 )
        
        datos_pulso = pulso_cuarta_derivada[:,1]
        downsample_pulso = datos_pulso[::6]

        return downsample_pulso[time_step] # la columna escogia es 1 

    def fifth_der_gaussiana(self,time_step):
        #======================================================================
        # columna 0 = tiempo
        # columna 1 = 0.5 ns
        # columna 2 = 1 ns
        # columna 3 = 1.5 ns 
        # columna 4 = 2 ns 
        #======================================================================

        datos_quinta_derivada = sio.loadmat('pulso_quinta_derivada_pos.mat')
        pulso_quinta_derivada = datos_quinta_derivada['alfa']
        
        #borrar filas 
        indices_eliminar = np.arange(0,401) # filas que quiero borrar 
        pulso_quinta_derivada = np.delete(pulso_quinta_derivada, indices_eliminar, axis=0) # 0 = borrar filas y 1 = borra columnas

        #agregar filas 
        indices_agregar = len(pulso_quinta_derivada)
        valores = [pulso_quinta_derivada[indices_agregar-1,i] for i in range(0,5)]
        valores_agregar = np.full((401, 5),valores)
        pulso_quinta_derivada = np.insert(pulso_quinta_derivada, indices_agregar,valores_agregar, axis=0 )
        
        datos_pulso = pulso_quinta_derivada[:,1]           
        downsample_pulso = datos_pulso[::6]

        return downsample_pulso[time_step] # la columna escogia es 1 
        
    def sixth_der_gaussiana(self,time_step):
        #======================================================================
        # columna 0 = tiempo
        # columna 1 = 0.5 ns
        # columna 2 = 1 ns
        # columna 3 = 1.5 ns 
        # columna 4 = 2 ns 
        #======================================================================

        datos_sexta_derivada = sio.loadmat('pulso_sexta_derivada_pos.mat')
        pulso_sexta_derivada = datos_sexta_derivada['alfa']
        
        #borrar filas 
        indices_eliminar = np.arange(0,401) # filas que quiero borrar 
        pulso_sexta_derivada = np.delete(pulso_sexta_derivada, indices_eliminar, axis=0) # 0 = borrar filas y 1 = borra columnas

        #agregar filas 
        indices_agregar = len(pulso_sexta_derivada)
        valores = [pulso_sexta_derivada[indices_agregar-1,i] for i in range(0,5)]
        valores_agregar = np.full((401, 5),valores)
        pulso_sexta_derivada = np.insert(pulso_sexta_derivada, indices_agregar,valores_agregar, axis=0 )

        datos_pulso = pulso_sexta_derivada[:,1]
        downsample_pulso = datos_pulso[::6]    

        return downsample_pulso[time_step] # la columna escogia es 1 
        
        
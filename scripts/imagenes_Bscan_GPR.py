"""
Archivo principal para el propagador electromagnetico

* se llaman a todos los modulos previamente creados:

1) propagador_2D_GPR, es el programa que tiene el modelado FDTD
2) forma_de_onda, es el programa en el cual se cargan los pulso electromagneticos
3) creacion_objeto, es el programa que crea los objetos en el modelo GPR
4) mensaje_usuario, es el programa que genera la informacion por consola de la simulacion

"""




#=================================================================================================
#librerias 
# ===============================================================================================
#librerias nativas de python:
import matplotlib.pyplot as plt
import time

#librerias nativas del propagador:
from propagador_2D_GPR import Propagador_2D_GPR
from forma_de_onda import Forma_de_onda
from creacion_objetos import Creacion_objetos
from mensajes_usuario import Mensajes_usuario


# ===============================================================================================
# funcion para graficar los resultados 
# ===============================================================================================

def graficar(parametros_simulacion,campo_electrico_Z):

    trazas = range(parametros_simulacion['pasos_de_la_antena'])

    plt.contourf(campo_electrico_Z,levels=65)
    #plt.axis('off')
    plt.title('Datos Bscan de un cilindro')
    plt.colorbar()
    plt.xlabel('Número de trazas')
    plt.ylabel('Tiempo')
    ax = plt.gca() 
    ax.invert_yaxis() 
    plt.show()

# ===============================================================================================
# funcion con el programa principal 
# ===============================================================================================


def main(caracteristicas_modelo,parametros_simulacion,caracteristicas_forma_de_onda, lista_de_objetos):
    
    mensaje_en_consola = Mensajes_usuario(caracteristicas_modelo)
    condiciones_iniciales = Propagador_2D_GPR(caracteristicas_modelo)
    creacion_PML = condiciones_iniciales.PML()
    fuente = Forma_de_onda(caracteristicas_forma_de_onda)

    modelo_completo = Creacion_objetos(caracteristicas_modelo)

    nombres_objetos =[]
    caracteristicas_objetos = []

    for i in range(len(lista_de_objetos)):
        if i % 2 == 0:
            nombres_objetos.append(lista_de_objetos[i])
        else:
            caracteristicas_objetos.append(lista_de_objetos[i])

    for j in range(len(nombres_objetos)):

        modelo_completo.anadir_estructura(nombres_objetos[j], caracteristicas_objetos[j])

        
    mensaje_en_consola.mensaje_inicial(nombres_objetos)
    medio = modelo_completo.caja(nombres_objetos[0])
    medio = modelo_completo.cilindro(nombres_objetos[1])
    
    comienzo = time.time()      
    campo_electrico_en_z = condiciones_iniciales.propagar(parametros_simulacion,fuente,creacion_PML,medio)
    final = time.time()
    tiempo_simulacion = final-comienzo
    mensaje_en_consola.mensaje_final(tiempo_simulacion)
    
    
    plt.plot(campo_electrico_en_z[:,15])
    plt.show()

    graficar(parametros_simulacion,campo_electrico_en_z)

    return (medio)


if __name__ == '__main__':

    """
    En esta seccion que agregan las caracteristica para el modelo GPR
    """

    # 1) Dimensiones del modelo
    caracteristicas_modelo ={
    'tamano_modelo_en_x' : 100 ,
    'tamano_modelo_en_y' : 60 ,
    'discretizacion_en_x': 0.01,
    'posicion_antena_transmision_x'  : 10,
    'posicion_antena_transmision_y' : 50,
    'posicion_antena_recepcion_x' : 14,
    'posicion_antena_recepcion_y' : 50      
     }


     
    model_features = {
        'discretization_x': 0.01, # meters
        'model_size_in_x': 100, # points
        'model_size_in_y': 60, #points
        'position_TX_y': 50, #points
        'position_TX_x': 10,  #points
        'position_RX_y': 50, #points
        'position_RX_x': 14, #points
    }


    waveform_characteristics = {
        'frequency': 1.6e9, #Hz
        'type': 'ricker'

    }

    # ===============================================================================================
    # 2) parametros de la simulacion 

    parametros_simulacion = {'pasos_de_la_antena' : 80, 'ventana_tiempo': 420}

    simulation_parameters = {
        'antenna_steps': 80,
        'time_window': 420


    }


    # ===============================================================================================
    # 3) forma de onda utilizar 
    caracteristicas_forma_de_onda = {'frecuencia':1.6e9}
    
    # ===============================================================================================
    # 4) Creacion de objetos:
    nombre_objeto_1 = 'caja_subsuelo'
    caracteristicas_objeto_1 = { 'ubicacion_en_x': 0,
    'ubicacion_en_y': 50,
    'conductividad': 0,
    'permitividad_relativa': 6
    }

    dict_box = {
        'type' : 'box',
        'location_at_x': 0, #points
        'location_at_y': 50, #points
        'conductivity': 0,  #s/m
        'relative permittivity': 6 
    }
    nombre_objeto_2 = 'cilindro'
    caracteristicas_objeto_2 = { 'ubicacion_en_x': 50,
    'ubicacion_en_y': 25,
    'conductividad': 0.0003,
    'permitividad_relativa': 15,
    'radio': 10
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
    # ===============================================================================================
    # 5) agrupar toda la informacion: primero los nombres de los objetos y luego sus caracteristicas 
    
    lista_de_objetos = [nombre_objeto_1,caracteristicas_objeto_1,nombre_objeto_2,caracteristicas_objeto_2]
    
    """
    =======================================================================
    se ejecuta la funcion principal
    =======================================================================
    """
   
    guarda = main(caracteristicas_modelo, parametros_simulacion, caracteristicas_forma_de_onda, lista_de_objetos)




    #===========================================================================

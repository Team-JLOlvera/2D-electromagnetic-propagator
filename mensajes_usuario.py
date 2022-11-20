
class Mensajes_usuario:

    def __init__(self, caracteristicas_modelo):

        self.size_x = caracteristicas_modelo['tamano_modelo_en_x']
        self.size_y = caracteristicas_modelo['tamano_modelo_en_y']
        self.posicion_TX_x = caracteristicas_modelo['posicion_antena_transmision_x']
        self.posicion_TX_y = caracteristicas_modelo['posicion_antena_transmision_y']
        self.posicion_RX_x = caracteristicas_modelo['posicion_antena_recepcion_x']
        self.posicion_RX_y = caracteristicas_modelo['posicion_antena_recepcion_y']

    def mensaje_inicial(self,nombres_objetos):

        print('-----------------------------------------------------------------------------------------------')     
        print('-----------------------------------------------------------------------------------------------')   
        print('           *****         ******         *****                *******     ***********           ')
        print('         ***   ***      *********      *********            **     ***   ***     ****          ')
        print('        ***             ***    ***     ***    ***                  ***   ***      ****         ')
        print('        **              ***    ***     ***    **                  ***    ***        ****       ')
        print('        ***********     ***   ***      ***   **                 ***      ***         ****      ')
        print('        ***      ***    *******        ******      ******     ***        ***         ****      ')
        print('        ***      ***    ***            ***  ***             ***          ***        ****       ')
        print('        ****    ***     ***            ***   ***           ***           ***      ****         ')
        print('         *********      ***            ***    ***         ***      **    ***    ****           ')
        print('           *****        ***            ***      **        ***********    **********            ')
        print('-----------------------------------------------------------------------------------------------')     
        print('-----------------------------------------------------------------------------------------------')   
        print('_______________________________________________________________________________________________')
        print('MODEL FEATURES:        ')
        print(f'size {int(self.size_x)*0.01} [m] x {int(self.size_y)*0.01} [m]')
        print('spatial discretization 0.01 [m]') 
        print('temporal discretization 16.6 [ps]')
        print('_______________________________________________________________________________________________')
        print('INITIAL ANTENNA LOCATION: ')
        print(f'transmission antenna in x: {int(self.posicion_TX_x)*0.01} [m] and in y: {int(self.posicion_TX_y)*0.01} [m] ')
        print(f'reception antenna in x: {int(self.posicion_RX_x)*0.01} [m] and in y: {int(self.posicion_RX_y)*0.01} [m] ')
        print('_______________________________________________________________________________________________')
        
        for name in nombres_objetos:
            print(f'The model has an object created with the name of: {name}')
        print('_______________________________________________________________________________________________')
    
    def mensaje_proceso(self,cantidad_maxima,lo_que_lleva):
        procentaje = round((int(lo_que_lleva+1)/int(cantidad_maxima))*100,1)
        print(f'{lo_que_lleva+1} A-scan of {cantidad_maxima} has been made, process = {procentaje}% ')

    def mensaje_final(self,tiempo):
        print('_______________________________________________________________________________________________')
        print('SIMULATION FINISHED')
        print(f'total simulation time is {round(tiempo/60,2)} [min]')
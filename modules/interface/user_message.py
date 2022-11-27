"""
Messages to the user
"""

def initial_message ():
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

def model_features_message (dict_features):
    
    # variable initialization
    points_model = (dict_features['model_size_in_x'], dict_features['model_size_in_y'])
    dx = dict_features['discretization_x']
    dt = dx/int(2*299792458)
    points_Tx = (dict_features['position_TX_x'],dict_features['position_TX_y'])
    points_Rx = (dict_features['position_RX_x'],dict_features['position_RX_y'])

    print('Model features: ')
    print(f'model points {points_model} ')
    print(f'spatial discretization {dx} (m)') 
    print(f'temporal discretization {dt} (ps)')
    print('_______________________________________________________________________________________________')
    print('Initial position of the antenna:')
    print(f'Coordinates in points for the Tx antenna: {points_Tx}')
    print(f'Coordinates in points for the Rx antenna : {points_Rx} [m] ')
    print('_______________________________________________________________________________________________')


def final_message(time_elapsed):
    print('_______________________________________________________________________________________________')
    print('The simulation is over')
    print(f'total simulation time is {round(time_elapsed/60,2)} (min)')


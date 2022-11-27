"""

has different waveforms implemented for use in propagator:

*sinusoidal
*chirp
*Gaussian
*first derivative of the Gaussian pulse
*ricker

"""

#======================================================================================================
# Libraries
#======================================================================================================
#libraries 

from math import exp, pi,sqrt 
import numpy as np


#======================================================================================================
#Class
#======================================================================================================
class Waveform:

    def __init__(self, waveform_characteristics):
        self.frequency = waveform_characteristics['frequency']
        self.pulse_type = waveform_characteristics['type']

    def transmitted_pulse(self,time_step,delta_t):

        if 'ricker' == self.pulse_type:
            return self.ricker(time_step,delta_t)
        elif 'gaussian' == self.pulse_type:
            return self.gaussian(time_step,delta_t)
        elif 'chirp' == self.pulse_type:
            return self.chirp(time_step,delta_t)
        elif 'sinusoidal' == self.pulse_type:
            return self.sinusoidal(time_step,delta_t)
        elif 'first_der_gaussian' == self.pulse_type:
            return self.first_der_gaussian(time_step,delta_t)
        else:
            print('The correct pulse was not selected')

    #======================================================================================================
    # Chirp
    #======================================================================================================


    def chirp(self,time_step,delta_t):
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # user modifiable:
        time_window = 200
        initial_phase= 0 #radians 
        
        end_frequency = 5.2e9
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        start_frequency = self.frequency
        sweep_time = time_window* delta_t
        constant_c = (end_frequency-start_frequency )/ sweep_time      
        time = time_step*delta_t

        signal_chirp = np.sin(initial_phase+(2*np.pi*(((constant_c*time**2)/2)+start_frequency*time)))

        return signal_chirp
        

    #======================================================================================================
    # Gaussian
    #======================================================================================================

    def gaussian(self, time_step,delta_t):

        sita = 2*(pi**2)*(self.frequency )**2
        equis = 1/self.frequency 
        time = time_step*delta_t
        
        pulse = exp(-1*sita*(time-equis)**2)
        
        return pulse

    #======================================================================================================
    # Sinusoidal
    #======================================================================================================
           
    def sinusoidal(self,time_step,delta_t):
        
        w = 2*np.pi*self.frequency  
        signal_sinusoidal = np.sin(w*delta_t*time_step)

        return signal_sinusoidal    

    #======================================================================================================
    # first derivative Sinusoidal
    #======================================================================================================
    
    def first_der_gaussian(self,time_step,delta_t):

        sita = 2*(pi**2)*(self.frequency )**2
        equis = 1/self.frequency 
        time = time_step*delta_t

        pulse = -2 *sqrt(exp(1)/(2*sita))*sita*(time-equis)*exp(-1*sita*(time-equis)**2)

        return pulse
    
    #======================================================================================================
    # Ricker
    #======================================================================================================

    def ricker(self,time_step,delta_t):

        sita = (pi**2)*(self.frequency)**2
        equis = sqrt(2) /self.frequency
        time = time_step*delta_t

        pulse = -1*((2*sita*((time-equis)**2))-1)*exp(-1*sita*(time-equis)**2)

        return pulse


        
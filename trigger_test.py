# %%
# imports
from psychopy import visual, core, prefs

prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 3

import serial
from psychopy import sound

# %%
from math import floor
import numpy as np

# comment out if not using serial port
port = serial.Serial('/dev/tty.usbserial-D30C1INU', 115200)

rng = np.random.uniform()

# najpierw musimy zaladowac dzwieki z plikow zeby nie bylo ich w forze
win = visual.Window([400,400]) 
std = sound.Sound("stnd_h500.wav")
dev = sound.Sound("dev_h800.wav")
omission = sound.Sound("omiss.wav")

win.flip()
    
# tu trzeba wygenerwoac liste dzwiekow z zadanymi warunkami
    
# ilość iteracji dźwięków     
d = 30     
    
ite = list(range(d))    
    
# %%

# iterowanie po dzwiekach z wyzej wygenerowanej listy    
for i in ite:
    next_flip = win.getFutureFlipTime(clock='ptb')
    if np.random.uniform() < .2:
        dev.play(when=next_flip)
        win.callOnFlip(port.write, str.encode('2'))
    
    else:
        std.play(when=next_flip)
        win.callOnFlip(port.write, str.encode('1'))
    
    
    win.flip()
    win.callOnFlip(port.write, str.encode('0')) # wyzerowanie portu - przenosimy do oddzielnej funkcji 
    
    for _ in range(59):
        win.flip()



### FUNCTIONS NEEDED: 
    
#play_sound()
def play_sound(sound): 
    """
    Play a sound.

    Parameters:
    sound (object): The sound object to play.

    Returns:
    None
    """
    sound.play() 
    
# send_trigger()
def send_trigger(port, value: int):
    """
    Send a trigger to the port.
    
    Parameters:
    port (object): The port object to send the trigger to.
    value (int): The value to send to the port.
    
    Returns:
    None
    """
    win.callOnFlip(port.write, str.encode(value))
    
#--------------------------------------------------------------

# reset_port()
def reset_port(port, value: int):
    """
    Reset the port and write the specified value to it.

    Parameters:
    port (object): The port object to reset.
    value (str): The value to write to the port.

    Returns:
    None
    """
    win.flip()
    win.callOnFlip(port.write, str.encode(value)) 
    

    
    
#--------------------------------------------------------------   
#--------------------------------------------------------------        
        
### TO DO: 
# play_sound(plik_dzwieku)

# generate_list(dlugosc_bloku) - DONE

# funkcja do liczenia ile procent dewiantow faktycznie byl wygenerowany w liscie dla czlowieka - DONE

# tworzenie listy funkcja(no_sounds: int) -- no_sounds wziete z funkcji - DONE

# na podstawie inputu okreslamy liczbe bodzcow ktora ma byc w tym bloku - DONE

# losujemy liczbe pomiedzy 0 a 1 - DONE

# jezeli ona jest mniejsza niz 0.15 to najpierw sprawdzanie, jesli true to dopisujemy do listy dewiant1
# jezeli pomiedzy 0.15 a 0.3 to najpierw sprawdzanie, jesli true to dopisujemy do listy dewiant2
# jezeli powyzej 0.3 to dopisujemy do listy standard

# napisac funkcje sprawdzajaca - DONE

#%%

def calculate_stim_count(block_length: int, ioi: float): 
    """
    This function calculates the number of stimuli that can fit in a block
    based on the block length and the inter-onset interval (IOI).

    Parameters:
        block_length (int): The length of the block in seconds.
        ioi (float): The inter-onset interval in seconds.

    Returns:
        int: The number of stimuli that can fit in the block.
    """
    from math import floor
    s_count = floor(block_length / ioi) 
    return s_count
    
#%%
stim_count = calculate_stim_count(15, 2)

#%%

def generate_stim_list(stim_count: int):
    """
    This function generates a list of stimuli based on the number of stimuli
    
    Parameters:
        stim_count (int): The number of stimuli to generate.
        
    Returns:
        list: The list of stimuli.
    """    
    stim_list = ["std", "std", "std", "std", "std", "std"]
    
    while len(stim_list) < stim_count:
        if np.random.uniform() < .15:
            if check_stimuli(stim_list, "dev"):
                stim_list.append("dev")
        elif np.random.uniform() < .3:
            if check_stimuli(stim_list, "omission"):
                stim_list.append("omission")
        else :
            stim_list.append("std")
        
    return stim_list

          


def check_stimuli(stim_list, stim: str):
    """
    Check if the given stimulus is valid based on the previous stimuli in the list.

    Args:
        stim_list (list): List of previous stimuli.
        stim (str): The stimulus to be checked.

    Returns:
        bool: True if the stimulus is valid, False otherwise.
    """
    if stim == "dev":
        if "std" == stim_list[-1]:
            if "dev" not in stim_list[-4:]:
                return True 

        else:
            return False
        
    elif stim == "omission":
        if "std" == stim_list[-1]:
            if "omission" not in stim_list[-4:]:
                return True

        else:
            return False
    
    else:
        return False
            
            
que = generate_stim_list(100)
que            

# %%

def percentage_of_deviants(stim_list: list, *deviants: str) -> float:
    """
    Calculate the percentage of deviant stimuli in the list.

    Parameters:
        stim_list (list): The list of stimuli.
        *deviants (str): Variable number of deviant stimuli.

    Returns:
        float: The percentage of deviant stimuli.
    """
    dev_omission_count = sum(stim_list.count(item) for item in deviants)
    # print(deviants)
    # print(type(deviants))
    dev_omission_percentage = (dev_omission_count / len(stim_list)) * 100
   
    print(f"Percentage of deviants in a list: {dev_omission_percentage:.2f} %")

percentage_of_deviants(que, "dev", "omission")
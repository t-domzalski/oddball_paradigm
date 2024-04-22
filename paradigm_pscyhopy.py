# imports
from psychopy import visual, core, prefs, visual, sound, event, gui, logging

prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 3

import os
import serial
from math import floor
import numpy as np

send_triggers = True
if send_triggers:
    port = serial.Serial('/dev/tty.usbserial-D30C1INU', 115200)
# Config
# comment out if not using serial port
#port = serial.Serial('/dev/tty.usbserial-D30C1INU', 115200)

#rng = np.random.uniform()

# najpierw musimy zaladowac dzwieki z plikow zeby nie bylo ich w forze
#win = visual.Window([400,400]) 
#std = sound.Sound("std_h500.wav")
#dev = sound.Sound("dew_h800.wav")
#omission = sound.Sound("omiss.wav")
    
sound_pool = {"std": sound.Sound("std_h500.wav", hamming = False),
              "dev": sound.Sound("dev_h800.wav", hamming = False),
              "omission": sound.Sound("omiss.wav", hamming = False)}

trigger_pool = {
    "std": 1,
    "dev": 2,
    "omission": 4
}
    
# Uploading needed functions

# when standard is playing I need corresponding name of stimuli on the screen  
# win flips implemented in procedure
# play_sound()

def play_sound_from_dict(stim_list: list, sound_pool: dict):
    """
    Play sounds from a list of stimuli using a dictionary of sounds.

    Parameters:
        stim_list (list): A list of stimuli to be played.
        sound_pool (dict): A dictionary of sounds,
            where the keys are the stimulus types
            and the values are the sound objects.

    Returns:
        None
    """
    for stim in stim_list:
        if stim in sound_pool:
            play_sound(sound_pool[stim])
            if send_triggers:
                send_trigger(port, trigger_pool[stim])
            flip_screen(1)
               
            flip_screen(59)
            
        else:
            print(f"Unknown stimulus: {stim}")


def play_sound(sound: object):
    """
    This function plays a sound from a sound pool on the next flip.
    It takes a sound object as input and uses the `win.getFutureFlipTime()` function
    to determine the next flip time. The sound is then
    played using the `sound.play()` method.

    Parameters:
    sound (object): The sound object to play.

    Returns:
    None
    """
    next_flip = win.getFutureFlipTime(clock='ptb')
    sound.play(when=next_flip)
  
 
def flip_screen(times: int = 1):
    """
    Flips the screen a specified number of times.

    Parameters:
    times (int): The number of times to flip the screen. Default is 1.
    """
    for _ in range(times):
        win.flip()

# send_trigger()
def send_trigger(port, value):
    """
    Send a trigger to the port.
    
    Parameters:
    port (object): The port object to send the trigger to.
    value (int): The value to send to the port.
    
    Returns:
    None
    """
    value_s = str(value)
    win.callOnFlip(port.write, str.encode(value_s))
    

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
    
#stim_count = calculate_stim_count(15, 2)


def generate_stim_list(stim_count: int):
    """
    This function generates a list of stimuli based on the number of stimuli
    
    Parameters:
        stim_count (int): The number of stimuli to generate.
        
    Returns:
        list: The list of stimuli.
    """    
    stim_list = 6 * ["std"]
    
    while len(stim_list) < stim_count:
        if np.random.uniform() < .20:
            if check_stimuli(stim_list, "dev"):
                stim_list.append("dev")
        elif np.random.uniform() < .40:
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
            
            
#que = generate_stim_list(100)
#que            

def percentage_of_deviants(stim_list: list, *deviants: str):
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
    dev_omission_percentage: float = (dev_omission_count / len(stim_list)) * 100
   
    print(f"Percentage of deviants in a list: {dev_omission_percentage:.2f} % \n"
          f"Number of deviants: {dev_omission_count}")

#percentage_of_deviants(que, "dev", "omission")



# Psychopy task

# my_path = os.path.abspath(os.path.dirname(__file__))
# os.chdir(my_path)
# os.chdir('..')
# log_dir = 'logs/'

def quit_exp():
    win.close()
    #logging.flush()
    core.quit()

# create quit key:
event.globalKeys.add(key='escape', func = quit_exp, name='shutdown')
keyNext = "space"

# get subject info:
ID_box = gui.Dlg(title = 'Subject identity')
ID_box.addField('ID: ')
#sub_id = ID_box.show()
#ID_box.show()

#create a window
color = "white"
win = visual.Window([800, 600], color='black')

# setup logging file
block_time = core.Clock()

Instructions = visual.TextStim(win, text = 'In the following, you will hear a sequence '
                                            'At certain points in the sequence',
                                            color=color, wrapWidth=1.8)

#logging.setDefaultClock(block_time)
#filename = log_dir + '.log'
#lastLog = logging.LogFile(filename, level=logging.INFO, filemode='a')

#def text_window():
#    Instructions = visual.TextStim(win, text = 'In the following, you will hear a sequence '
#                                        'of short sound patterns.\n'
#                                        'At certain points in the sequence',
#                                        color=color, wrapWidth=1.8)
#    Instructions.draw()
#    event.waitKeys(keyList=[keyNext])
    
# screen to show the stimuli names
def insert_cross():
    stname_screen = visual.TextStim(win, text='+', color="white", height=0.2)
    stname_screen.draw()

######### Run experiment ##########

#insert_cross()
#Instructions.draw()
#core.wait(5)
ID_box.show()
stim_list = generate_stim_list(500)
play_sound_from_dict(stim_list, sound_pool)



# ilość iteracji dźwięków     
#d = 30     
   
#ite = list(range(d))    
#
#for i in ite:
#   next_flip = win.getFutureFlipTime(clock='ptb')
#   if np.random.uniform() < .2:
#       dev.play(when=next_flip)
#       win.callOnFlip(port.write, str.encode('2'))
#   
#   else:
#       std.play(when=next_flip)
#       win.callOnFlip(port.write, str.encode('1'))
#   
#   
#   win.flip()
#   win.callOnFlip(port.write, str.encode('0')) # wyzerowanie portu - przenosimy do oddzielnej funkcji 
#   
#   for _ in range(59):
#       win.flip()
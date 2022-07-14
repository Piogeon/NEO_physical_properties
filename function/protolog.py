# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:03:45 2022

@author: pio-r
"""
import datetime

def protolog(level, message):
    """
    

    Parameters
    ----------
    level : TYPE: string, deb = debugging, inf = information, 
        war = warning, err = error
        
    message : TYPE: string.

    Returns
    -------
    TYPE
        [<time_utc>] - [level] - <message>.

    """

    time_stamp = datetime.datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S]")
    if level not in ["deb", "inf", "war", "err"]:
        print("Error")
    else:
        level = "[" + level + "]"
    
    logentry = time_stamp + " - " + level + " - " + message
    
    return print(logentry)
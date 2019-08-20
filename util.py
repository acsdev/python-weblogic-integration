'''
Class with util methods
'''
import sys
import subprocess

from os import system, name

# define our clear function 
def clear_screen(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def execute_command( cmd ):
    print(cmd)
    process = subprocess.Popen( cmd , shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return process

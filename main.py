#!/usr/bin/env python

'''
Dependencies of this projetc
pip install spur
'''
import json
import spur
import re
import os 
import subprocess
import pdb
import time
import sys

from datetime import datetime

from collections import defaultdict

from util import clear_screen, execute_command

from data_environment import DataEnvironment

from actions.stop_servers import ActionStopServers

_options_env   = defaultdict(lambda : 'EMPTY', {'0':'SIGAP_DSV','1':'SIGAP_TST','2':'SIGAP_HML','3':'SIGAP_PRD'})
_options_opt   = defaultdict(lambda : 'EMPTY', {'0':'CLEAR_ALL_NODES'})

def load_json_environment_options():
    '''
    Load data from json file
    '''
    with open('config.json', 'r') as f:
        _config_data = json.load(f)

    return _config_data

def identify_chosen_environment( config_data, name_env ):
    '''
    Load data from chosen environment to '_chosen_env' variable
    '''
    try:
        _chosen_env = DataEnvironment([ value for value in config_data['environments'] if value['name'] == name_env ][0])
        print(f'\nEnvironment chosen: {_chosen_env.name}\n')
    except:
        print('Fail on identify the enviromment')
        exit()
    
    return _chosen_env

def check_servers_running( env ):
    '''
    Identify all servers running
    '''
    shell = spur.SshShell( hostname=env.ssh_host, username=env.ssh_usr, password=env.ssh_pwd)
    result = shell.run(["ps","auxww"])

    serversRunning = []
    for line in str(result.output).split(r'\n'):
        match = re.findall(r'(oracle\s+\d+\s).+(-Dweblogic.Name=\w+)', line)
        if match:
            serverPid = re.sub(r'[^0-9]', '', str(match[0][0]) )
            serverName = re.sub(r'-Dweblogic.Name=', '', str(match[0][1]) )
            serversRunning.append( (serverName, serverPid) )
    
    serversRunning.sort()
    return serversRunning

def clean_server(env):
    print('Process start')

    #Stop servers
    pythonScript = f'{os.path.dirname(os.path.realpath(__file__))}/actions/stop_servers.py'
    subprocess.run(['./wlst.sh',f'{env.oracle_home}/wlserver/server/bin', pythonScript, f'"{env.__dict__}"'])

    # MOVE
    date_now = datetime.now()
    pattern_folder_old = "{:%Y%m}".format( date_now )
    pattern_folder_new = "{:%Y%m%d%H%M}".format( date_now )

    shell = spur.SshShell( hostname=env.ssh_host, username=env.ssh_usr, password=env.ssh_pwd)
    ssh_session = shell._connect_ssh()
    
    for node in env.weblogic_nodes:
        node_address = f'{env.weblogic_domain_dir}/servers/{node}'
        node_address_backup = f'{node_address}_{pattern_folder_new}'
        node_address_remove = f'{node_address}_{pattern_folder_old}*'
    
        cmd_on_server = f'rm -rf {node_address_remove} && mv {node_address} {node_address_backup}'
        print()    
        print(f'CMD ON SERVER: {cmd_on_server}')
        ssh_session.exec_command( cmd_on_server )    

    ssh_session.close()
    print()
    print()

    #Start servers
    pythonScript = f'{os.path.dirname(os.path.realpath(__file__))}/actions/start_servers.py'
    subprocess.run(['./wlst.sh',f'{env.oracle_home}/wlserver/server/bin', pythonScript, f'"{env.__dict__}"'])

    print('Process end')

def interctive_chose_environment( config_data ):
    
    print('List of available environments')
    
    for (opt_k, opt_v) in _options_env.items():
        print(f'{opt_k} - {opt_v}')
    
    # Get options from user
    while True:
        _option_env = str(_options_env[ input('Pick one of them: ') ])
        if _option_env != 'EMPTY':
            break

    # Identify enviromment
    return identify_chosen_environment( config_data, _option_env )

def interctive_chose_operation():
    
    print('List of available operations')
    for (opt_k, opt_v) in _options_opt.items():
        print(f'{opt_k} - {opt_v}')
    
    # Get options from user
    while True:
        option_opt = str(_options_opt[ input('Pick one of them: ') ])
        if option_opt != 'EMPTY':
            break
    
    # Identify enviromment
    print(f'Operation chosen: {option_opt}')
    return option_opt

def start( config_data ):
    while True:
        clear_screen()

        chosen_env = interctive_chose_environment( config_data )

        chosen_opt = interctive_chose_operation()

        result = check_servers_running( chosen_env )

        if not result:
            print('There are none servers running')

        if result:
            print('List of servers runnig:\n')
            for name, id in result:
                print(f'{"".ljust(5)}Server name: {name.ljust(20)},PID: {id}')

        time.sleep( 2 )
        print()
        
        if chosen_opt == _options_opt['0']:
            clean_server( chosen_env )

        print('Do you wanna continue? (y == yes, any other key == no) ')
        if input() != 'y':
            break

if __name__ == '__main__':
    
    config_data = load_json_environment_options()

    if ( len(sys.argv) == 1 ):
        
        start( config_data )

    else:
        
        chosen_env = identify_chosen_environment( config_data, sys.argv[1] )
        
        try:
            action  = sys.argv[2]
        except:
            print('Fail on identify action')
            exit()

        if not action in _options_opt.values():
            print('Fail on identify action')
            exit()

        print(f'Operation chosen: {action}')
        if (action == _options_opt['0']):
            clean_server( chosen_env )
        
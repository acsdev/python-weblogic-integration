'''
Class to keep information about enviroment
'''
class DataEnvironment:
    
    def __init__(self, jsonEnv):
        self.oracle_home = jsonEnv['oracle_home']
        self.name = jsonEnv['name']
        self.ssh_host = jsonEnv['ssh_host']
        self.ssh_usr = jsonEnv['ssh_usr']
        self.ssh_pwd = jsonEnv['ssh_pwd']
        self.admin_server_name = jsonEnv['admin_server_name']
        self.weblogic_host = jsonEnv['weblogic_host']
        self.weblogic_port = jsonEnv['weblogic_port']
        self.weblogic_usr = jsonEnv['weblogic_usr']
        self.weblogic_pwd = jsonEnv['weblogic_pwd']
        self.weblogic_domain_dir = jsonEnv['weblogic_domain_dir']
        self.weblogic_nodes = jsonEnv['weblogic_nodes']

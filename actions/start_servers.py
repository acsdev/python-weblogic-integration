'''
Integratated with WLST
'''
import sys
from data_environment import DataEnvironment

class ActionStartServers:

    def __init__(self, data_env):
        self.env =  DataEnvironment( eval( data_env ) )

    def execute(self):
        connect( self.env.weblogic_usr, self.env.weblogic_pwd, self.env.weblogic_host +':'+self.env.weblogic_port )       
        
        for node in self.env.weblogic_nodes:
            try:
                start(node,'Server')
            except:
                print( 'Error on start node:' + node)
                print( sys.exc_info()[0] )
        
        exit()


# __name__ == 'main'
# because __name__ will be equals to main, when called by java weblogic.WLSTn
if (__name__ == 'main'):
    obj = ActionStartServers( sys.argv[2] )
    obj.execute()
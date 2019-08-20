'''
Integratated with WLST
'''
import sys
from data_environment import DataEnvironment

class ActionStopServers:

    def __init__(self, data_env):
        self.env =  DataEnvironment( eval( data_env ) )

    def execute(self):
        connect( self.env.weblogic_usr, self.env.weblogic_pwd, self.env.weblogic_host +':'+self.env.weblogic_port )       
        
        for node in self.env.weblogic_nodes:
            try:
                shutdown(node,'Server', ignoreSessions='true', force='true')
            except:
                print( 'Error on shutdown node:' + node)
                print( sys.exc_info()[0] )

        exit()

# __name__ == 'main'
# because __name__ will be equals to main, when called by java weblogic.WLSTn
if (__name__ == 'main'):
    obj = ActionStopServers( sys.argv[2] )
    obj.execute()
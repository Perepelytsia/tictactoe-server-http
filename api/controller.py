import sys, os
sys.path.append(os.path.join(os.getcwd(), 'actions'))

class Controller:

    def __init__( cmd: dict):
        self.command = cmd

	def createServerCmd(cmd: str, response: dict):
    	return {"cmd":cmd, "time":"2018-08-31T00:00:00.1", "data":response}

	def action(self):

	    try:

	        if not isinstance(self.command, dict):
	            raise ValueError("Invalid json for command")
	        if 'cmd' not in self.command:
	            raise ValueError('No send cmd')
	        if 'device' not in self.command:
	            raise ValueError('No send device')
	        if 'time' not in self.command:
	            raise ValueError('No time for command')
	        if 'data' not in self.command:
	            raise ValueError('No data for command')

	    except BaseException as err:
	        import error
	        response = error.action({"msg": err})
	        return createServerCmd("error", response)
	    else:
	       
	        if self.command['cmd'] == 'init':
	            import init
	            response = init.action(self.command['data']);
	        elif self.command['cmd'] == 'start':
	            import start
	            response = start.action(self.command['data']);
	        elif self.command['cmd'] == 'move':
	            import move
	            response =  move.action(self.command['data']);
	        elif data['cmd'] == 'finish':
	            import finish
	            response =  finish.action(self.command['data']);
	        
	        return createServerCmd(self.command['cmd'], response)
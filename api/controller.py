import sys, os
sys.path.append(os.path.join(os.getcwd(), 'actions'))

class Controller:

    def __init__(cmd: dict):
        self.command = cmd

    def createServerCmd(self, response: dict) -> dict:
        # save command to the database
        answer = {"data": response}
        answer['owner'] = self.command['owner']

        if self.command['cmd'] == 'init':
            answer['cmd'] = 'user'
        elif self.command['cmd'] == 'finish':
            answer['cmd'] = 'user'
        elif self.command['cmd'] == 'start':
            answer['cmd'] = 'state'
        elif self.command['cmd'] == 'move':
            answer['cmd'] = 'state'
        elif self.command['cmd'] == 'error':
            answer['cmd'] = 'error'

        return answer

    def action(self) -> dict:
        try:
            if not isinstance(self.command, dict):
                raise ValueError("Invalid json for command")
            if 'cmd' not in self.command:
                raise ValueError('No send cmd')
            if 'owner' not in self.command:
                raise ValueError('No owner for command')
            if 'data' not in self.command:
                raise ValueError('No data for command')
        except BaseException as err:
            return createServerCmd("error", {"msg": err})
        else:
            # save command to the database
            if self.command['cmd'] == 'init':
                import init
                response = init.action(self.command['data'])
            elif self.command['cmd'] == 'start':
                import start
                response = start.action(self.command['data'])
            elif self.command['cmd'] == 'move':
                import move
                response =  move.action(self.command['data'])
            elif self.command['cmd'] == 'finish':
                import finish
                response =  finish.action(self.command['data'])
        return createServerCmd(response)
import sys, os
import psycopg2
import json
#sys.path.append(os.path.join(os.getcwd(), 'actions'))
sys.path.append('/www/tictactoe/api/actions')

class Controller:

    def __init__(self, cmd: dict):
        self.command = cmd

    def action(self) -> dict:

        conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
        cursor = conn.cursor()

        try:
            if not isinstance(self.command, dict):
                raise ValueError("Invalid json for command")
            if 'cmd' not in self.command:
                raise ValueError('No send cmd')
            if 'data' not in self.command:
                raise ValueError('No data for command')
        except BaseException as err:
            response = {"cmd":"error", "owner":self.command['owner'], "data": err}
        else:

            postgres_insert_query = """ INSERT INTO commands (type, cmd, owner, data) VALUES (%s,%s,%s,%s)"""
            record_to_insert = ('req', self.command['cmd'], self.command['owner'], json.dumps(self.command['data']))
            cursor.execute(postgres_insert_query, record_to_insert)
            conn.commit()

            if self.command['cmd'] == 'init':
                import init
                response = init.action(self.command)
            elif self.command['cmd'] == 'start':
                import start
                response = start.action(self.command)
            elif self.command['cmd'] == 'move':
                import move
                response =  move.action(self.command, False)
            elif self.command['cmd'] == 'finish':
                import finish
                response =  finish.action(self.command)

        postgres_insert_query = """ INSERT INTO commands (type, cmd, owner, data) VALUES (%s,%s,%s,%s)"""
        record_to_insert = ('res', response['cmd'], response['owner'], json.dumps(response['data']))
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()

        cursor.close()
        conn.close()

        return response

#data = {"cmd":"init", "owner":"script", "data":{}}
#data = {"cmd":"start", "owner":"script", "data":{}}
data = {"cmd":"move", "owner":"script", "data":{"choose":1}}
#data = {"cmd":"finish", "owner":"script", "data":{}}
controller = Controller(data)
result = controller.action();
print(result)
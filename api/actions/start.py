import psycopg2
import random
import requests
import move
import json

def action(cmd: dict) -> dict:

    data = {"turn":1, "chip":1, "field":[0,0,0,0,0,0,0,0,0]}
    cmd['data'] = data
    cmd['cmd'] = 'state'

    if random.choice([True, False]):
        # first bot
        owner = cmd['owner']
        cmd['owner'] = 'bot'
        payload = json.dumps(cmd)
        result = requests.post("http://tictactoebot", data=payload)
        cmd = json.loads(result.text)
        cmd['owner'] = owner
        cmd = move.action(cmd, True)

    conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
    cursor = conn.cursor()
    insert = """ INSERT INTO games (active, turn, chip, owner, opponent, field) VALUES (%s, %s, %s, %s, %s, %s)"""
    bind = (1, 1, cmd['data']['chip'], cmd['owner'], 'bot', json.dumps(cmd['data']['field']))
    cursor.execute(insert, bind)
    conn.commit()
    cursor.close()
    conn.close()

    return cmd

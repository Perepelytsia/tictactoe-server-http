import psycopg2

def action(cmd: dict) -> dict:

    conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
    cursor = conn.cursor()
    insert = """ INSERT INTO games (active, turn, chip, owner, opponet, field) VALUES (%s, %s, %s, %s, %s, %s)"""
    bind = (1, 1, 1, cmd['owner'], 'bot', '[0,0,0,0,0,0,0,0,0]')
    cursor.execute(insert, bind)
    conn.commit()  

    query = "select turn, chip, field from games where owner = %s and active = 1"
    cursor.execute(query, (cmd['owner'],))
    games = cursor.fetchall()

    game = games[0]
    cmd['data'] = {"turn":game[0], "chip":game[1], "field":game[2]}
    cmd['cmd'] = 'state'

    cursor.close()
    conn.close()

    return cmd

import psycopg2

def action(cmd: dict) -> dict:

    conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
    cursor = conn.cursor()

    query = "select turn, chip, field from games where owner = %s and active = 1"
    cursor.execute(query, (cmd['owner'],))
    games = cursor.fetchall()

    if games:
        game = games[0]
        cmd['data'] = {"turn":game[0], "chip":game[1], "field":game[2]}
        cmd['cmd'] = 'state'
    else:

        query = "select win, lost from users where name = %s"
        cursor.execute(query, (cmd['owner'],))
        users = cursor.fetchall()
        data = {"win":0, "lost":0}
        
        if users:
            data['win'] = users[0][0]
            data['lost'] = users[0][1]
        else:
            insert = """ INSERT INTO users (name) VALUES (%s)"""
            bind = (cmd['owner'],)
            cursor.execute(insert, bind)
            conn.commit()

        cmd['cmd'] = 'user'
        cmd['data'] = data

    cursor.close()
    conn.close()

    return cmd


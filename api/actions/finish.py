import psycopg2

def action(cmd: dict) -> dict:

    conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
    cursor = conn.cursor()

    owner = cmd['owner']

    query = "select result from games where owner = %s and active = 1"
    cursor.execute(query, (owner,))
    games = cursor.fetchall()

    if games[0][0] == 1:
        update1 = "UPDATE users SET win = win + 1 WHERE name = %s"
    elif games[0][0] == 2:
        update1 = "UPDATE users SET draw = draw + 1 WHERE name = %s"
    else:
        update1 = "UPDATE users SET lost = lost + 1 WHERE name = %s"

    update2 = "UPDATE games SET active = 0 WHERE owner = %s and active = 1"

    cursor.execute(update1, (owner,))
    cursor.execute(update2, (owner,))

    conn.commit()

    query = "select win, lost, draw from users where name = %s"
    cursor.execute(query, (owner,))
    users = cursor.fetchall()

    data = {"win":users[0][0], "lost":users[0][1], "draw":users[0][2]}
    cmd['cmd'] = 'user'
    cmd['data'] = data
    
    cursor.close()
    conn.close()

    return cmd
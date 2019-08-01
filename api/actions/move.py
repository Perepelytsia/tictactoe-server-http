import psycopg2
import requests
import json

def action(cmd: dict, bot: bool) -> dict:

	owner = cmd['owner']

	conn = psycopg2.connect(dbname='tictactoe', user='tictactoe', password='tictactoe', host='localhost')
	cursor = conn.cursor()
	query = "select turn, chip, field, result from games where owner = %s and active = 1"
	cursor.execute(query, (owner,))
	games = cursor.fetchall()

	if games:
		game   = games[0]

		turn   = game[0]
		chip   = game[1]
		field  = game[2]
		result = game[3]

		if chip==1:
			botChip = 2
		else:
			botChip = 1

	if bot:
		# bot logic
		if games:
			# non first bot turn
			if result == None and cmd['data']['choose'] >= 0 and cmd['data']['choose'] < 9 and field[cmd['data']['choose']] == 0:
				# correct 'choose'
				field[cmd['data']['choose']] = botChip
				update = "UPDATE games SET field = %s WHERE owner = %s and active = 1"
				cursor.execute(update, (json.dumps(field), owner,))
				conn.commit()

			data = {"turn":turn, "chip":chip, "field":field}
		else:
			# first bot turn
			field = [0] * 9
			field[cmd['data']['choose']] = 1
			data = {"turn":1, "chip":2, "field":field}

		cmd = {"cmd":"state", "owner":owner, "data":data}
	else:
		# user logic
		if result == None and cmd['data']['choose'] >= 0 and cmd['data']['choose'] < 9 and field[cmd['data']['choose']] == 0:
			# correct choose
			field[cmd['data']['choose']] = chip
			update = "UPDATE games SET field = %s WHERE owner = %s and active = 1"
			cursor.execute(update, (json.dumps(field), owner,))
			conn.commit()

			if isWin(field, chip):
				# user win
				data = {"turn":turn, "chip":chip, "field":field, "result":1}
				cmd = {"cmd":"state", "owner":owner, "data":data}
				update = "UPDATE games SET result = %s WHERE owner = %s and active = 1"
				cursor.execute(update, (1, owner,))
				conn.commit()
			else:
				# user continue game

				data = {"turn":turn, "chip":botChip, "field":field}
				payload = json.dumps({"cmd":"state", "owner":"bot", "data":data})
				result = requests.post("http://tictactoebot", data=payload)
				cmd = json.loads(result.text)

				cmd['owner'] = owner
				cmd = action(cmd, True)

				if isWin(cmd['data']['field'], botChip):
					# bot win
					data = {"turn":turn, "chip":chip, "field":cmd['data']['field'], "result":0}
					cmd = {"cmd":"state", "owner":owner, "data":data}
					update = "UPDATE games SET result = %s WHERE owner = %s and active = 1"
					cursor.execute(update, (0, owner,))
					conn.commit()
		else:
			# incorrect 'choose', as result again 'state'
			data = {"turn":turn, "chip":chip, "field":field}
			cmd = {"cmd":"state", "owner":owner, "data":data}

			if len(game) == 4:
				result = game[3]
				if result == 1:
					cmd['data']['result'] = 1
				elif result == 0:
					cmd['data']['result'] = 0

	cursor.close()
	conn.close()

	return cmd

def isWin(field: list, chip: int) -> bool:

	result = False

	winCombs = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8),(0,4,8), (2,4,6))
	for winComb in winCombs:
		if field[winComb[0]] == chip and field[winComb[1]] == chip and field[winComb[2]] == chip:
			result = True
			break

	return result
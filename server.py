from tornado import websocket, web, ioloop, httpserver
import tornado
import json

connections={}

WAITING_FOR_PLAYERS=0
STARTING_GAME=1
gameState=WAITING_FOR_PLAYERS

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("Websocket open")
		print('Client IP: ' + self.request.remote_ip)
		

	def check_origin(self, origin):
		return True

	def on_message(self, message):
		print('message recieved %s' %message)
		self.write_message("You said " + message)
		messageHandler.handleIncomingMsg(message, self)
		ip = self.request.remote_ip
		message = ip
		self.addToConnectionList(self, message)


	def on_close(self):
		print("Websocket closed")

	def addToConnectionList(self, socket, message):
		connections[str(message)] = socket

class MessageHandler:
	def handleIncomingMsg(self, data, socket):
		type=""
		try:
			type = data
		except:
			print("Unexpected error.")

		if type == "join":
			success = self.addPlayer(data, socket)
			if success:
				self.sendToAll(socket, "gameState", gameState)
			else:
				self.sendToAll(socket, "error", "No available space, two players already in game.")
		if type == "updataState":
			print ()
		else:
			msg = "Error reading game request. Please make sure message type is either join, updataState, or..."
			message={"type":"error", "data":msg}
			print("Error reading game request.")

	def addPlayer(self, data, socket):
		global gameState

		result = True;
		if len(connections)<2:
			connections[socket.request.remote_ip] = socket
			print("Number of connections " + str(len(connections)))
			for key, value in connections.items():
				print(key)
			if (len(connections) == 2):
				gameState=STARTING_GAME
		elif (len(connections) >= 2):
			result = False;
		return result;

	def sendToAll(self, pid, type, data):
		for c in connections:
			connections[c].write_message("Hello Everyone")


messageHandler = MessageHandler()

app= tornado.web.Application([
	#map the handler to the URI named "wstest"
	(r'/wstest', WSHandler),
])
 
if __name__ == '__main__':
	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
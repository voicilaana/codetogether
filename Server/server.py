from flask import Flask
import pusher
import time
import json

pusher_client = pusher.Pusher(
	app_id='198468',
	key='7cf17138b96636bf08be',
	secret='956eb99e339f31a3c3f9',
	ssl=True
	)

app = Flask(__name__)

def parse_rooms(name="rooms.txt"):
	f = open(name, 'r')
	rooms = {}
	try:
		for line in f:
			line = line.split(',')
			rooms[line[0]] = line[1].replace('\n','')
	except:
		return {}
	f.close()
	return rooms

@app.route('/')
def index():
    return 'Hi'

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/test', methods=['GET', 'POST'])
def test():
    pusher_client.trigger('test_channel','my_event',{'message':'hello world'})
    return "WORKS"

@app.route('/host/<name>')
def create_room(name):
	f = open("rooms.txt", 'a+')
	f.write(name+'\n')
	f.close()
	return "Joined! Congratulations!"

def deleteContent(fName):
    with open(fName, "w"):
        pass

@app.route('/reset')
def reset():
	deleteContent('rooms.txt')
	return "cleared."

@app.route('/send_code/<params>', methods=['GET', 'POST'])
def send_code(params):
   	params = params.split('&code=')
   	channel = params[0]
   	code = params[1]
	pusher_client.trigger(channel,'my_event',{'message':code})

	deleteContent('code.txt')
	f = open("code.txt", 'a+')
	f.write(code)
	f.close()
	return "200, OK"

@app.route('/addChallenge/<params>', methods=['GET', 'POST'])
def addChallenge(params):
	params = params.split('&')
	channel = params[0]
	title = params[1]
	description = params[2]
	pusher_client.trigger(channel,'add_challenge',{'title':title, 'description':description})
	return "200, OK"

@app.route('/sendSolution/<params>', methods=['GET', 'POST'])
def sendSolution(params):
	params = params.split('&')
	channel = params[0]
	title = params[1]
	description = params[2]
	pusher_client.trigger(channel,'solution_provided',{'title':title, 'description':description})
	return "200, OK"
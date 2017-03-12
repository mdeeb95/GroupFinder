import os
import json
import script
import string
import random
import classes
import meetings
import members
import chat
from pusher import Pusher

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

from flask import Flask, jsonify, request

app = Flask(__name__)

pusher = Pusher(
  app_id='312968',
  key='0aab40d486c9e2ce1c43',
  secret='43573bfcd05521382472',
  ssl=True
)

@app.route('/', methods=['GET'])
def index():
  return jsonify(
	{
	  'hello': 'worlds'
	}
  )

@app.route('/login', methods=['POST'])
def login():
	memberID = request.form['username']
	password = request.form['password']
	return jsonify(
		members.check_member(memberID, password)
	)

@app.route('/register', methods=['POST'])
def register():
	memberID = request.form.get('username')
	name = request.form.get('name')
	password = request.form.get('password')
	print memberID, name, password
	return jsonify(
		members.add_member(memberID, name, password)
	)

@app.route('/create_class', methods=['POST'])
def create_class():
	classID = request.form['classID']
	name = request.form['name']
	leader = request.form['leader']
	return jsonify(
		classes.add_class(classID, name, leader, "GT")
	)

@app.route('/create_classes', methods=['POST'])
def create_classes():
    memberID = request.form.get('memberID')
    data = request.form.get('data')
    data_json = json.loads(data)['site_collection']
    for items in data_json:
        classID = items['id']
        name = items['title']
        leader = "Uddhav Bhagat"
        term = items.get('props').get('term')
        if term == "SPRING 2017":
            one = classes.add_class(classID, name, leader, "GT")
            two = classes.add_class_member(classID, memberID)
            if not two['success']:
                return jsonify(
                    {
                        'success': False,
                        'message': 'DB Error'
                    }
                )
    return jsonify(
        {
            'success': True,
            'message': 'Classes added successfully'
        }
    )



@app.route('/add_class_member', methods=['POST'])
def add_class_member():
	memberID = request.form['memberID']
	classID = request.form['classID']
	return jsonify(
		classes.add_class_member(classID, memberID)
	)

@app.route('/find_classes', methods=['POST'])
def find_classes():
	memberID = request.form['memberID']
	return jsonify(
		classes.find_classes(memberID)
	)

@app.route('/get_class_details', methods=['POST'])
def get_class_details():
	classID = request.form['classID']
	return jsonify(
		classes.get_class_details(classID)
	)

@app.route('/class/<string:classID>/members', methods=['GET'])
def get_class_members(classID):
    return jsonify(
        classes.get_class_members(classID)
    )


@app.route('/class/<string:classID>/meetings', methods=['POST'])
def get_class_meetings(classID):
    memberID = request.form['memberID']
    return jsonify(
        meetings.get_class_meetings(classID, memberID)
    )

@app.route('/create_meetings', methods=['POST'])
def create_meetings():
    meetingID = id_generator(32)
    classID = request.form['classID']
    title = request.form['title']
    location = request.form['location']
    description = request.form['description']
    dateJson = request.form['date']
    ownerID = request.form['owner']
    memberList = json.loads(request.form['memberList'])
    one = meetings.create_meetings(meetingID, classID, title, location, description, dateJson, ownerID)
    if not one['success']:
        return jsonify(
            {
                'success': False,
                'message': 'DB Error11'
            }
        )
    for item in memberList:
        two = meetings.add_meeting_members(meetingID, item)
        if not two['success']:
            return jsonify(
                {
                    'success': False,
                    'message': 'DB Error12'
                }
            )

    return jsonify(
        {
            'success': True,
            'message': 'Classes added successfully'
        }
    )

@app.route('/edit_meeting_location', methods=['POST'])
def edit_meetings_location():
    meetingID = request.form['meetingID']
    location = request.form['location']
    return jsonify(
        meetings.edit_meeting_location(meetingID, location)
    )

@app.route('/edit_meeting_title', methods=['POST'])
def edit_meeting_title():
    meetingID = request.form['meetingID']
    title = request.form['title']
    return jsonify(
        meetings.edit_meeting_title(meetingID, title)
    )

@app.route('/edit_meeting_description', methods=['POST'])
def edit_meeting_description():
    meetingID = request.form['meetingID']
    description = request.form['description']
    return jsonify(
        meetings.edit_meeting_description(meetingID, description)
    )

@app.route('/edit_meeting_date', methods=['POST'])
def edit_meeting_date():
    meetingID = request.form['meetingID']
    dateJson = json.loads(request.form['date'])
    return jsonify(
        meetings.edit_meeting_date(meetingID, dateJson)
    )

@app.route('/add_meeting_members', methods=['POST'])
def add_meeting_members():
    meetingID = request.form['meetingID']
    memberID = request.form['memberID']
    return jsonify(
        meetings.add_meeting_members(meetingID, memberID)
    )

@app.route('/<string:meetingID>/get_meeting_members', methods=['GET'])
def get_meeting_members(meetingID):
    return jsonify(
        meetings.get_meeting_members(meetingID)
    )


@app.route('/<string:meetingID>/get_chatID', methods = ['GET'])
def get_chatID(meetingID):
    return jsonify (
        chat.get_chatID(meetingID)
    )

@app.route('/get_chatID2', methods=['POST'])
def get_chatID2():
    memberID = request.form['memberID']
    member1ID = request.form['member1ID']
    return jsonify (
        chat.get_chatID(memberID, member1ID)
    )

@app.route('/<string:chatID>/create_message', methods = ['POST'])
def create_message(chatID):
    senderID = request.form['senderID']
    content = request.form['content']
    utc = request.form['time']
    pusher.trigger(chatID, 'new_message', { 'success': True})  
    return jsonify(
        chat.create_message(chatID, senderID, content, utc)
    )

@app.route('/<string:chatID>/get_messages', methods = ['GET'])
def get_chat(chatID):
    return jsonify(
        chat.get_messages(chatID)
    )

@app.route('/upload_document', methods=['POST'])
def upload_document():
    print request.form.get('data')
    return jsonify (
        {
            'success': True
        }
    )


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
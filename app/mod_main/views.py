from flask import Blueprint, render_template, request, redirect, url_for, Response, session
from bson import ObjectId
from app import mongo
import json
from werkzeug import secure_filename

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		data = request.form
		username = data['username']
		password = data['password']

		user = mongo.db.user.find({"username": username}).count()
		
		if user == 1:
			user_p = mongo.db.user.find({"password": password}).count()
			if user_p == 1:
				return redirect(url_for('main.index'))
			return redirect(url_for('main.login'))
		return redirect(url_for('main.login'))
				
		
	
		return 'sussess registration!'

@mod_main.route('/dashboard', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		reports = mongo.db.reports.find()
		return render_template('dashboard.html', reports=reports)
	elif request.method == 'POST':
		if username =='admin' and password == 'admin':
			return render_template('dashboard.html')
		else:  
			render_template('login.html')




@mod_main.route('/remove', methods=['POST'])
def remove_report():
	if request.method == 'POST':
		report_id = request.form["report_id"]
		print report_id
		mongo.db.reports.remove({"_id": ObjectId(report_id)})
		return Response(json.dumps({"removed": True}), mimetype='application/json')

@mod_main.route('/show/<string:report_id>', methods=['GET'])
def show(report_id):
	result=mongo.db.reports.find_one({"_id":ObjectId(report_id)})
	return 'Showing result '+str(result)


	

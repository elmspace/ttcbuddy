"""
	Author: Ash Dehghan
	Date: April 2018
	Description: 
"""


"""
	Import External Libs
"""
from flask import Flask, render_template, Response, flash, redirect, request, session, abort, url_for;
from werkzeug.utils import secure_filename
from functools import wraps;
import sys, os;
import flask;
import pickle;
import json;

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['mp4','m4a'])


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'python_modules/UserManagement/')));
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'python_modules/tag_modules/')));

"""
	Import Internal Libs
"""
from UserManagement import UserManagement;
from TagClass import Tag;

app = Flask(__name__);


"""
	This the end-point for the main page.
"""
@app.route("/")
def LandingPage():
	return render_template("landingPage.html");




"""
	This is a login-check page, which will check the session,
	we can use this as a decorator on any end-point which requires login.
"""
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if(session["logged_in"]):
			return f(*args, **kwargs)
		else:
			flash("You need to login first,")
			return LandingPage();
	return decorated_function;



@app.route('/login')
def login():
	return render_template("login.html");


 

"""
	This end-point takes care of the user login.
"""
@app.route('/authenticate', methods=['POST'])
def UserLogin():
	UserManagementObj = UserManagement(json.loads(flask.request.data));
	if(UserManagementObj.GetActionStatus()):
		session["user_profile"] = UserManagementObj.GetUserProfile();
		session["logged_in"] = True;
		msg = {};
		msg["status"] = "pass";
		msg["msg"] = UserManagementObj.GetActionMsg();
		return json.dumps(msg);
	else:
		session['logged_in'] = False;
		msg = {};
		msg["status"] = "fail";
		msg["msg"] = UserManagementObj.GetActionMsg();
		return json.dumps(msg);



@app.route('/usermanagement', methods=['POST'])
def CreateNewUser():
	UserManagementObj = UserManagement(json.loads(flask.request.data));
	if(UserManagementObj.GetActionStatus()):
		msg = {};
		msg["status"] = "pass";
		msg["msg"] = UserManagementObj.GetActionMsg();
		return json.dumps(msg);
	else:
		msg = {};
		msg["status"] = "fail";
		msg["msg"] = UserManagementObj.GetActionMsg();
		return json.dumps(msg);



"""
	This the end-point for the main page.
"""
@app.route("/profile")
@login_required
def ProfilePage():
	return render_template("profilePage.html");








@app.route("/CreateTag")
@login_required
def CreateTag():
	return render_template("createtag.html");



@app.route('/SaveTag', methods=['GET', 'POST'])
def SaveTag():
	tagData = {};
	for i in request.files:
		tagData[i] = request.files[i];
	
	for i in request.form:
		tagData[i] = request.form[i];

	TagObj = Tag();
	TagObj.SaveTag(tagData,session);

	return render_template("createtag.html");


@app.route("/GetTagData", methods=['POST'])
@login_required
def GetTagData():
	msg = {};
	msg["msg"] = True;
	return json.dumps(msg);


@app.route("/tagdata")
@login_required
def tagdata():
	return render_template("tagdata.html");



if __name__ == "__main__":
	context = ('../cert/server.crt','../cert/server.key')
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(host= '0.0.0.0',port=5000, ssl_context=context, threaded=False, debug=True);




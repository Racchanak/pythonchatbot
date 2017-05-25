import MySQLdb # Mysql ---
from flask import Flask, jsonify, make_response, send_from_directory
from flask import render_template
from flask import request
import aiml
import os

app = Flask(__name__)

kernel = aiml.Kernel()

if os.path.isfile("brain/bot_brain.brn"):
    kernel.bootstrap(brainFile="brain/bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    kernel.saveBrain("brain/bot_brain.brn")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatBot/')
@app.route('/chatBot')
def chatBot():
    return render_template('index1.html')

@app.route('/bot/<string:chat>', methods=['GET'])
def get_task(chat):
    return make_response(jsonify({'chatData': kernel.respond(chat)}))


# you must create a Cursor object. It will let
#  you execute all the queries you need
db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="appiness_dev_wow")
cursor = db.cursor()

@app.route("/wowadmin")
def wowadmin():
    cursor.execute("SELECT * FROM employer_details")
    results = cursor.fetchall()
    for row in results:
        with open('aiml/'+row[1]+'.aiml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
            f.write('<aiml version="2.0" encoding="UTF-8">')
        #     f.write('<category>')
        #     < pattern > HI < / pattern >
        #     < template >
        #     < ![CDATA[
        #         < p > Yes ! how
        #     can
        #     i
        #     help
        #     you. < / p >
        #              < a
        #     href = "javascript:;"
        #
        #     class ="btn btn-info" onclick="company_option('OPENING')" > Current Openings < / a >
        #
        #     < a
        #     href = "javascript:;"
        #
        #     class ="btn btn-info" onclick="company_option('COMPANY')" > About the Company < / a >
        #
        #     < a
        #     href = "javascript:;"
        #
        #     class ="btn btn-info" onclick="company_option('HR')" > Speak to the HR < / a >
        # ]] >
        # < / template >
        #     < / category >
            f.write('<category>')
            f.write('<pattern>HELLO </pattern>')
            f.write('<template>')
            f.write(row[4])
            f.write('</template>')
            f.write('</category>')
            f.write('</aiml>')

    return make_response(jsonify({'dbdata': row}))
    db.close()
# ---------

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor.execute("SELECT * from admin_table where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

app.config.update(
    PROPAGATE_EXCEPTIONS = True
)

if __name__ == '__main__':
    app.run(debug=True)
import MySQLdb # Mysql ---
from flask import Flask, jsonify, make_response, send_from_directory
from flask import render_template
from flask import request
import aiml, lxml
from lxml import etree
from lxml.etree import *
from lxml.builder import *

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


@app.route("/wowtest")
def wowtest():
    cursor.execute("SELECT * FROM employer_details WHERE employer_id BETWEEN 1810 AND 23876")
    results = cursor.fetchall()
    for result_row in results:
        with open('aiml/' + result_row[1] + '.aiml', 'w') as f:
            aiml = lxml.etree.Element('aiml')
            category = lxml.etree.SubElement(aiml, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = str(result_row[1])
            template = lxml.etree.SubElement(category, 'template')
            # template.text = '<![CDATA['
            span = lxml.etree.SubElement(template,'span')
            span.set('class', 'hidden-span')
            set = lxml.etree.SubElement(span,'set')
            set.set('name','topic')
            set.text = str(result_row[0])
            # template.text = ']]>'
            template.text = '<![CDATA['
            p = lxml.etree.SubElement(template, 'p')
            p.text = 'Yes ! how can i help you.'
            a = lxml.etree.SubElement(template,'a')
            a.set('href', 'javascript:;')
            a.set('onclick', 'cjoption(\'hr\')')
            a.set('class', 'btn btn-info')
            a.text = 'HR Details'
            a = lxml.etree.SubElement(template, 'a')
            a.set('href', 'javascript:;')
            a.set('onclick', 'cjoption(\'company\')')
            a.set('class', 'btn btn-info')
            a.set('text', 'About Company')
            a = lxml.etree.SubElement(template, 'a')
            a.set('href', 'javascript:;')
            a.set('onclick', 'cjoption(\'opening\')')
            a.set('class', 'btn btn-info')
            a.set('text', 'Current Openings')
            template.text = ']]>'
            # template.text = etree.CDATA(p)
            topic = lxml.etree.SubElement(aiml,'topic')
            topic.set('name',str(result_row[0]))
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'hr'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA['
            p = lxml.etree.SubElement(template,'p')
            p.text = str(result_row[4])
            template.text = ']]>'
            # template.text = etree.CDATA(p)
            f.write(tostring(aiml, pretty_print=True,xml_declaration=True, encoding='UTF-16'))

            # f.write(tostring(
            #     E.aiml(
            #         E.category(
            #             E.patern(str(result_row[1])),
            #             E.template('<![CDATA[<span class ="hidden-span">]]><set name = "topic">'+str(result_row[0])+'</set><![CDATA[</span>',
            #                 E.p('Yes ! how can i help you.'),
            #                 E.a(href='javascript:;',
            #                     onclick='cjoption(\'hr\')',
            #                     text='HR Details'),
            #                 E.a(href='javascript:;',
            #                     onclick='cjoption(\'company\')',
            #                     text='About Company'),
            #                 E.a(href='javascript:;',
            #                     onclick='cjoption(\'opening\')',
            #                     text='Current Openings')
            #             )
            #         ),
            #         E.topic(
            #             E.category(
            #                 E.patern(str(result_row[1])),
            #                 E.template('<![CDATA[<span class ="hidden-span">]]><set name = "topic">' + str(
            #                     result_row[0]) + '</set><![CDATA[</span>',
            #                            E.p('Yes ! how can i help you.'),
            #                            E.a(href='javascript:;',
            #                                onclick='cjoption(\'hr\')',
            #                                text='HR Details'),
            #                            E.a(href='javascript:;',
            #                                onclick='cjoption(\'company\')',
            #                                text='About Company'),
            #                            E.a(href='javascript:;',
            #                                onclick='cjoption(\'opening\')',
            #                                text='Current Openings')
            #                            )
            #             )
            #         )
            #     ),pretty_print=True,xml_declaration=True, encoding='UTF-16'))
    return 'Successfully Created!!!!'

@app.route("/wowadmin")
def wowadmin():
    cursor.execute("SELECT * FROM employer_details")
    results = cursor.fetchall()
    for result_row in results:
        with open('aiml/'+result_row[1]+'.aiml', 'w') as f:
            # res_str = str(result_row[0])
            f.write('<?xml version = "1.0" encoding = "UTF-8"?>')
            f.write('<aiml version = "2.0" encoding = "UTF-8">')
            f.write('<!-- insert your AIML categories here -->')
            f.write('<category>')
            f.write('<pattern>'+str(result_row[1])+'</pattern>')
            f.write('<template>')
            f.write('<![CDATA[<span class ="hidden-span">]]><set name = "topic">'+str(result_row[0])+'</set><![CDATA[</span>')
            f.write('<p> Yes ! how can i help you.</p>')
            f.write('<a href = "javascript:;" class ="btn btn-info" onclick="cjoption(\'hr\')">HR Details</a>')
            f.write('<a href = "javascript:;" class ="btn btn-info" onclick="cjoption(\'company\')">About Company</a>')
            f.write('<a href = "javascript:;" class ="btn btn-info" onclick="cjoption(\'opening\')">Current Openings</a>]]>')
            f.write('</template>')
            f.write('</category>')
            f.write('<topic name="'+ str(result_row[0])+'">')
            f.write('<category>')
            f.write('<pattern> HR </pattern>')
            f.write('<template>')
            f.write('<![CDATA[<p> Email: '+ str(result_row[4])+'</p> ]]>')
            f.write('</template>')
            f.write('</category>')
            f.write('</topic>')
            # jobs_details(row)
            f.write('</aiml>')
            return make_response(jsonify({'dbdata': result_row}))
    db.close()


def jobs_details(result_row):
    # result_row;
    cursor.execute("SELECT * FROM employer_details WHERE employer_id BETWEEN 1810 AND 23941")
    results = cursor.fetchall()
    for row in results:
        jobs_details(row)


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
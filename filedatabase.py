import MySQLdb # Mysql ---
from flask import Flask, jsonify, make_response, send_from_directory
from flask import render_template
from flask import request
import aiml, lxml
import io
import re
import urllib
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

@app.route('/appiness/')
@app.route('/appiness')
def appiness():
    return render_template('index1.html')

@app.route('/hexwhale/')
@app.route('/hexwhale')
def hexwhale():
    return render_template('index2.html')

@app.route('/bot/<string:chat>', methods=['GET'])
def get_task(chat):
    return make_response(jsonify({'chatData': kernel.respond(chat)}))


# you must create a Cursor object. It will let
#  you execute all the queries you need
db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="wow_live")
cursor = db.cursor()

def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

@app.route("/wowtest")
def wowtest():
    cursor.execute("SELECT employer_id,employer_name,employer_website,employer_email,employer_mobile_number,employer_yr_founded,employer_strength,employer_logo,employer_desc,employer_address,job_count,employer_location,employer_branches,employer_experts FROM employer_details LIMIT 0 , 25")
    company_results = cursor.fetchall()
    for result_row in company_results:
        with open('aiml/' + str(result_row[0]) + '.aiml', 'w') as f:
            aiml = lxml.etree.Element('aiml')
            category = lxml.etree.SubElement(aiml, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = (re.sub('[!@#.$~&()*]', '', result_row[1])).upper()
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template,'set')
            set.set('name','topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<p>Welcome to the world of '+result_row[1]+'</p><p>What do you like to know from the following?</p>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here You can find more about our company\')">About the Company</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here some details about our hr\')">Speak to the HR</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here Our Openings\')">Current Openings</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'VIEW\')">View Company Culture</a>'
            topic = lxml.etree.SubElement(aiml,'topic')
            topic.set('name',str(result_row[0]))
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ HR'
            template = lxml.etree.SubElement(category, 'template')
            if result_row[6] == None:
                template.text = '<![CDATA[<p>Email Id: '+str(result_row[3])+'</p>'+str(result_row[0])
            else:
                template.text = '<![CDATA[<p>Mobile no: '+str(result_row[4])+'</p><p>Email Id: '+str(result_row[3])+'</p>'+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            cursor.execute("SELECT founderName,founderDesg,founderAbout,founderImg_1,founderId FROM company_founders WHERE employer_id='"+str(result_row[0])+"'")
            if cursor.rowcount!=0:
                template.text = '<![CDATA[<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here is some details about our company\')">Company Details</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Employer Expertize in\')">Expertise</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Location and Branches\')">Location</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Team\')">Our Team</a>' + str(result_row[0])
                founder_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ TEAM'
                founder_text = '<![CDATA['
                template = lxml.etree.SubElement(category, 'template')
                for founder_row in founder_results:
                    founder_text += '<p></p><img src="https://employer.wow.jobs/' + founder_row[3] + '"/><p>'+founder_row[0]+'</p><p>' + result_row[1] + '</p>'
                template.text = founder_text + str(result_row[0])
            else :
                template.text = '<![CDATA[<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Her is some details about our company\')">Company Details</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Employer Expertize in\')">Expertise</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Location and Branches\')">Location</a>' + str(
                    result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ DETAILS'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Established: '+str(result_row[5])+'</p><p>Employee Strength: '+str(result_row[6])+'</p>'+str(result_row[0])
            cursor.execute("SELECT * FROM `wow_handler` WHERE e_id='"+str(result_row[0])+"'")
            wowhandler_result = cursor.fetchall()
            for handler_row in wowhandler_result:
                if handler_row[2] == None:
                    wow_handler = handler_row[1]
                else:
                    wow_handler = handler_row[2]
            cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='"+str(result_row[0])+"' ORDER BY job_crt_date DESC LIMIT 0 , 3")
            if cursor.rowcount != 0:
                job_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ OPENINGS'
                template = lxml.etree.SubElement(category, 'template')
                job_text = '<![CDATA['
                for job_row in job_results:
                    job_name = ((job_row[1]).strip()).replace(' ','-')
                    job_location = ((job_row[8]).strip()).replace(' ','-')
                    job_link = job_name+'-jobs-'+job_location+'/'+str(job_row[0])
                    job_text += '<p><a class="btn btn-info" target="_blank" href="https://www.wow.jobs/' + wow_handler + '/'+job_link+'">' + job_row[1] + '</a></p>'
                template.text = job_text + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ BRANCHES'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Location : ' + result_row[11] + '</p><p>Branches: '+ result_row[12]+'</p>' + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ EXPERTIZE IN'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>' + result_row[13] + '</p>' + str(result_row[0])
            f.write(tostring(aiml, pretty_print=True,xml_declaration=True  , encoding='UTF-8'))
    return 'Successfully Created!!!!'

@app.route("/chatdetails")
def chatdetails():
    cursor.execute(
        "SELECT employer_id,employer_name,employer_website,employer_email,employer_mobile_number,employer_yr_founded,employer_strength,employer_logo,employer_desc,employer_address,job_count,employer_location,employer_branches,employer_experts FROM employer_details LIMIT 0 , 25")
    company_results = cursor.fetchall()
    for result_row in company_results:
        with open('aiml/' + str(result_row[0]) + '.aiml', 'w') as f:
            aiml = lxml.etree.Element('aiml')
            category = lxml.etree.SubElement(aiml, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            # filename_word = ''.join(c for result_row[1] in input_string if valid_xml_char_ordinal(result_row[1]))
            pattern.text = (re.sub('[!@#.$~&()*]', '', result_row[1])).upper()
            # pattern.text = (re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+', '', result_row[1])).upper()
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template, 'set')
            set.set('name', 'topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<p>Yes, how may i help you?</p>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here You can find more about our company\')">About the Company</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here some details about our hr\')">Speak to the HR</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here Our Openings\')">Current Openings</a>'
            # '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'VIEW\')">View Company Culture</a>'
            topic = lxml.etree.SubElement(aiml, 'topic')
            topic.set('name', str(result_row[0]))
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ HR'
            template = lxml.etree.SubElement(category, 'template')
            if result_row[6] == None:
                template.text = '<![CDATA[<p>Email Id: ' + str(result_row[3]) + '</p>' + str(result_row[0])
            else:
                template.text = '<![CDATA[<p>Mobile no: ' + str(result_row[4]) + '</p><p>Email Id: ' + str(
                    result_row[3]) + '</p>' + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            cursor.execute(
                "SELECT founderName,founderDesg,founderAbout,founderImg_1,founderId FROM company_founders WHERE employer_id='" + str(
                    result_row[0]) + "'")
            if cursor.rowcount != 0:
                template.text = '<![CDATA[<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here is some details about our company\')">Company Details</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Employer Expertize in\')">Expertise</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Location and Branches\')">Location</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Team\')">Our Team</a>' + str(
                    result_row[0])
                founder_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ TEAM'
                founder_text = '<![CDATA['
                template = lxml.etree.SubElement(category, 'template')
                for founder_row in founder_results:
                    founder_text += '<p></p><img src="https://employer.wow.jobs/' + founder_row[3] + '"/><p>' + \
                                    founder_row[0] + '</p><p>' + result_row[1] + '</p>'
                template.text = founder_text + str(result_row[0])
            else:
                template.text = '<![CDATA[<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Her is some details about our company\')">Company Details</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Employer Expertize in\')">Expertise</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Location and Branches\')">Location</a>' + str(
                    result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ DETAILS'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Established: ' + str(result_row[5]) + '</p><p>Employee Strength: ' + str(
                result_row[6]) + '</p>' + str(result_row[0])
            cursor.execute("SELECT * FROM `wow_handler` WHERE e_id='" + str(result_row[0]) + "'")
            wowhandler_result = cursor.fetchall()
            for handler_row in wowhandler_result:
                if handler_row[2] == None:
                    wow_handler = handler_row[1]
                else:
                    wow_handler = handler_row[2]
            cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='" + str(
                result_row[0]) + "' ORDER BY job_crt_date DESC LIMIT 0 , 3")
            if cursor.rowcount != 0:
                job_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ OPENINGS'
                template = lxml.etree.SubElement(category, 'template')
                job_text = '<![CDATA['
                for job_row in job_results:
                    job_name = ((job_row[1]).strip()).replace(' ', '-')
                    job_location = ((job_row[8]).strip()).replace(' ', '-')
                    job_link = job_name + '-jobs-' + job_location + '/' + str(job_row[0])
                    job_text += '<p><a class="btn btn-info" target="_blank" href="https://www.wow.jobs/' + wow_handler + '/' + job_link + '">' + \
                                job_row[1] + '</a></p>'
                template.text = job_text + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ BRANCHES'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Location : ' + result_row[11] + '</p><p>Branches: ' + result_row[
                12] + '</p>' + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ EXPERTIZE IN'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>' + result_row[13] + '</p>' + str(result_row[0])
            f.write(tostring(aiml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    return 'Successfully Created!!!!'

@app.route("/wowadmin")
def wowadmin():
    cursor.execute("SELECT * FROM employer_details")
    results = cursor.fetchall()
    for result_row in results:
        with io.open('aiml/'+result_row[1]+'.aiml', 'w',encoding='utf-8-sig') as f:
            # res_str = str(result_row[0])
            f.write('<?xml version = "1.0" encoding = "UTF-8"?>')
            f.write('<aiml>')
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
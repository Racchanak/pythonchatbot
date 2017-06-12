
import MySQLdb # Mysql ---
from flask import Flask, jsonify, make_response, send_from_directory
from flask import render_template
from flask import request
from flask_cors import CORS
import aiml, lxml
import io
import re
import urllib
from lxml import etree
from lxml.etree import *
from lxml.builder import *
import os
import datetime

application = Flask(__name__)
CORS(application)

kernel = aiml.Kernel()

if os.path.isfile("aiml/420388.aiml"):
    if os.path.isfile("brain/bot_brain.brn"):
        kernel.bootstrap(brainFile="brain/bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        kernel.saveBrain("brain/bot_brain.brn")

@application.route('/')
def index():
    return render_template('botnew.html')

@application.route('/chatindex/')
@application.route('/chatindex')
def chatindex():
    return render_template('chatbot.html')

@application.route('/appiness/')
@application.route('/appiness')
def appiness():
    return render_template('index1.html')

@application.route('/hexwhale/')
@application.route('/hexwhale')
def hexwhale():
    return render_template('index2.html')

@application.route('/bot/<string:chat>', methods=['GET'])
def get_task(chat):
    return make_response(jsonify({'chatData': kernel.respond(chat)}))


# you must create a Cursor object. It will let
#  you execute all the queries you need
db = MySQLdb.connect(host="173.194.240.26",user="wowdev",passwd="devwow",db="wow_live")
# db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="wow_live")
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

@application.route("/wowtest")
def wowtest():
    cursor.execute("SELECT employer_id,replace(employer_name, char(153), '') AS employer_name,employer_website,employer_email,employer_mobile_number,employer_yr_founded,employer_strength,employer_logo,replace(replace(replace(replace(replace(replace(replace(replace(employer_desc, char(149), ''), char(147), ''), char(148), ''), char(153), ''), char(150), ''), char(146), ''), char(145), ''), char(39), '') AS employer_desc,employer_address,job_count,replace(employer_location, char(150), '') AS employer_location,replace(employer_branches, char(150), '') AS employer_branches,employer_experts FROM employer_details")
    company_results = cursor.fetchall()
    for result_row in company_results:
        with open('aiml/' + str(result_row[0]) + '.aiml', 'w') as f:
            benefitsName = [["bft_insurance", "Insurance"], ["bft_flexible_hours", "Flexible Work Hours"],
                            ["bft_5days_week", "5 Days a week"], ["bft_wmnf_atmp", "Women Friendly Atmosphere"],
                            ["bft_wmnf_locn", "Women Friendly Location"], ["bft_cafeteria", "Cafeteria"],
                            ["bft_game_zone", "Game Zone"], ["bft_matpat_leav", "Maternity & Paternity Leaves"],
                            ["bft_cab_srvc", "Cab Service"], ["bft_free_food", "Free Food"],
                            ["bft_dress_code", "No Dress Code"], ["bft_yearly_bnus", "Yearly Bonus"],
                            ["bft_shifts", "Shifts"], ["bft_equity", "Equity"],
                            ["bft_reloc_alwc", "Relocation Allowance"], ["bft_join_bnus", "Joining Bonus"],
                            ["bft_wrk4m_home", "Work From Home"], ["bft_mand_offs", "Mandatory Offs"],
                            ["bft_fitness_cntr", "Fitness Centre"], ["bft_train_cert", "Training & Certifications"],
                            ["bft_accomdtn", "Accomodation"], ["bft_creche", "Creche"],
                            ["bft_kid_fdly", "Kid Friendly"], ["bft_pet_fdly", "Pet Friendly"],
                            ["bft_parkg_fcty", "Parking Facility"], ["bft_onsite_opty", "Onsite Opportunity"],
                            ["bft_paid_hldy", "Paid Holidays"], ["bft_tution_rmbs", "Tution Fee Reimbursment"],
                            ["bft_401k", "401K"], ["bft_hide", "N"]];
            aiml = lxml.etree.Element('aiml')
            category = lxml.etree.SubElement(aiml, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = (re.sub('[!@#.$~&()*]', '', result_row[1])).upper()
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template,'set')
            set.set('name','topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<p></p><ul class="owl-carousel owl-theme repli">' \
                            '<li class="item scroll" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                            '<li class="item" onclick="cjoption(\'About Company\',this)">About us</li>' \
                            '<li class="item" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul>'
            topic = lxml.etree.SubElement(aiml,'topic')
            topic.set('name',str(result_row[0]))
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '*'
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template,'set')
            set.set('name','topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<p></p><p>May I help you with following?</p>' \
                            '<ul class="owl-carousel owl-theme repli">' \
                            '<li class="item" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                            '<li class="item" onclick="cjoption(\'About Company\',this)">About Us</li>' \
                            '<li class="item" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul>'
            cursor.execute("SELECT * FROM `wow_handler` WHERE e_id='" + str(result_row[0]) + "'")
            wowhandler_result = cursor.fetchall()
            for handler_row in wowhandler_result:
                wow_handler_id = handler_row[1]
                if handler_row[2] == None:
                    wow_handler = wow_handler_id
                else:
                    wow_handler = handler_row[2]
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ OPENINGS'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'OPENINGS'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'OPENINGS _'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'OPENINGS'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '* OPENINGS'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'OPENINGS'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '# OPENINGS'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'OPENINGS'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'OPENING'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'OPENINGS'
            cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='" + str(result_row[0]) + "' AND job_delete ='NO' AND job_publish ='PLA' ORDER BY job_mod_date DESC LIMIT 0 , 3")
            if cursor.rowcount != 0:
                job_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'OPENINGS'
                template = lxml.etree.SubElement(category, 'template')
                job_text = '<![CDATA[<p></p><div class="jobList"><ul class="owl-carousel owl-theme repli">'
                for job_row in job_results:
                    job_name = ((job_row[1]).strip()).replace(' ', '-')
                    job_location = ((job_row[8]).strip()).replace(' ', '-')
                    job_experience = 'Exp: '+str(job_row[10])+'-'+str(job_row[11])
                    job_link = job_name + '-jobs-' + job_location + '/' + str(job_row[0])
                    job_text += '<li class="item"> <h5>'+job_row[1]+'</h5> <h5>'+job_row[8]+'</h5> <h5>'+job_experience+'</h5> \
                                <div class="blockDis"> \
                                <a class="anchor-block" target="_blank" href="https://www.wow.jobs/' + wow_handler + '/' + job_link + '">Apply</a> \
                                </div></li>'
                template.text = job_text + '</ul></div><div class="submenu"><ul class="owl-carousel owl-theme repli">' \
                            '<li class="item scroll" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                            '<li class="item" onclick="cjoption(\'About Company\',this)">About us</li>' \
                            '<li class="item" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul></div>'+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'COMPANY'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'ABOUT COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'COMPANY'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '# COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'COMPANY'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'COMPANY _'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'COMPANY'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'ABOUT _'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'COMPANY'
            about_subtext = '<div class="submenu"><ul class="owl-carousel owl-theme repli"> \
                <li class="item " onclick="cjoption(\'Work Culture\',this)">Work culture</li> \
                <li class="item" onclick="cjoption(\'Expertise\',this)">Expertise</li>'
            cursor.execute("SELECT * FROM employer_benefits WHERE bft_hide='N' AND employer_id='" + str(result_row[0]) + "'")
            if cursor.rowcount != 0:
                about_subtext += '<li class="item" onclick="cjoption(\'Benefits\',this)">Benefits</li>'
            cursor.execute("SELECT * FROM employer_places_around WHERE plc_delete = 'N' AND employer_id = '" + str(result_row[0]) + "'")
            if cursor.rowcount != 0:
                about_subtext += '<li class="item" onclick="cjoption(\'Location\',this)">Location</li>'
            cursor.execute("SELECT * FROM company_founders WHERE employer_id='" + str(result_row[0]) + "'")
            if cursor.rowcount != 0:
                about_subtext += '<li class="item" onclick="cjoption(\'Founder\',this)">Founders</li>'
            about_subtext += '</ul></div>'
            about_text = '<![CDATA[<p></p><div class="aboutCompany"><p></p> \
                <p class="text-left"><span class="headIn">About company</span> \
                '+result_row[8]+'<span class="blockDis"><a href="https://www.wow.jobs/' + wow_handler+'" class="anchor-block">Read more</a></span></p> \
                </div><p>Do you want to know more about us?</p> \
                <ul class="owl-carousel owl-theme repli"> \
                <li class="item " onclick="cjoption(\'Work Culture\',this)">Work culture</li> \
                <li class="item" onclick="cjoption(\'Expertise\',this)">Expertise</li>'
            cursor.execute("SELECT bft_insurance,bft_flexible_hours,bft_5days_week,bft_wmnf_atmp,bft_wmnf_locn, \
                    bft_cafeteria,bft_game_zone,bft_matpat_leav,bft_cab_srvc,bft_free_food,bft_dress_code, \
                    bft_yearly_bnus,bft_shifts,bft_equity,bft_reloc_alwc,bft_join_bnus,bft_wrk4m_home, \
                    bft_mand_offs,bft_fitness_cntr,bft_train_cert,bft_accomdtn,bft_creche,bft_kid_fdly, \
                    bft_pet_fdly,bft_parkg_fcty,bft_onsite_opty,bft_paid_hldy,bft_tution_rmbs,bft_401k, \
                    bft_hide FROM employer_benefits WHERE bft_hide='N' AND employer_id='" + str(result_row[0]) + "'")
            if cursor.rowcount != 0:
                about_text += '<li class="item" onclick="cjoption(\'Benefits\',this)">Benefits</li>'
                wow_benefits = cursor.fetchall()[0]
                benefits_result = []
                for i in range(len(cursor.description)):
                    if cursor.description[i][0] == benefitsName[i][0]:
                        if wow_benefits[i] == 'Y':
                            benefits_result.append(benefitsName[i][1])
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'BENEFITS'
                template = lxml.etree.SubElement(category, 'template')
                benefit_text = '<![CDATA[<p></p><div class="benefitsHold">\
                                <h4 class="headIn">Benefits at ' + result_row[1] + '</h4>\
                                <ul>'
                for benefits in benefits_result:
                    benefit_text += '<li>' + benefits + '</li>'
                template.text = benefit_text + '</ul></div>' + about_subtext+ str(result_row[0])
            cursor.execute("SELECT * FROM employer_places_around WHERE plc_delete = 'N' AND employer_id = '" + str(result_row[0]) + "'")
            wow_location = cursor.fetchall()
            if cursor.rowcount != 0:
                about_text += '<li class="item" onclick="cjoption(\'Location\',this)">Location</li>'
                for location in wow_location:
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'LOCATION'
                    template = lxml.etree.SubElement(category, 'template')
                    template.text = '<![CDATA[<p></p><a target="_blank" href="https://www.google.co.in/maps/place/' + re.sub('[ ]', '+', location[2]) + '/@' + str(location[7]) + ',' + str(location[8]) + '">Get Direction</a> \
                            <div class="hidden"><span class="lat">' + str(location[7]) + '</span> \
                            <span class="long">' + str(location[8]) + '</span><span class="name">' + location[2] + '</span></div> \
                            <div id="map_div_' + str(result_row[0]) + '" class="map_disp"></div>' + about_subtext + str(result_row[0])
            cursor.execute("SELECT founderName,founderDesg,founderAbout,founderImg_1,founderId FROM company_founders WHERE employer_id='"+str(result_row[0])+"' ORDER BY founderId ASC")
            if cursor.rowcount!=0:
                about_text+='<li class="item" onclick="cjoption(\'Founder\',this)">Founders</li>'
                founder_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# FOUNDER'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'FOUNDER'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ FOUNDERS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'FOUNDER'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'FOUNDERS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'FOUNDER'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'FOUNDER _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'FOUNDER'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'FOUNDER'
                template = lxml.etree.SubElement(category, 'template')
                founder_text = '<![CDATA[<p></p><div class="wow-cult"><ul class="owl-carousel owl-theme repli">'
                for founder_row in founder_results:
                    founder_text += '<li class="item"><img src="https://employer.wow.jobs/' + founder_row[3] + '"/><h5>'+founder_row[0]+'</h5><h5>' + founder_row[1] + '</h5></li>'
                template.text = founder_text + '</ul></div>'+about_subtext+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'COMPANY'
            template = lxml.etree.SubElement(category, 'template')
            template.text = about_text + '</ul><div class="submenu"><ul class="owl-carousel owl-theme repli">' \
                '<li class="item scroll" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                '<li class="item" onclick="cjoption(\'About Company\',this)">About us</li>' \
                '<li class="item" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul></div>' + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ HR'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'HR'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '# HR'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template,'srai')
            srai.text = 'HR'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'HR #'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template, 'srai')
            srai.text = 'HR'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'HR _'
            template = lxml.etree.SubElement(category, 'template')
            srai = lxml.etree.SubElement(template, 'srai')
            srai.text = 'HR'
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'HR'
            template = lxml.etree.SubElement(category, 'template')
            hr_text = '<![CDATA[<p></p><div><p></p>'
            if result_row[6] != None:
                hr_text +='<p>Mobile no: '+str(result_row[4])+'</p>'
            template.text = hr_text+'<p>Email Id: '+str(result_row[3])+'</p></div><div class="submenu"><ul class="owl-carousel owl-theme repli">' \
                '<li class="item scroll" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                '<li class="item" onclick="cjoption(\'About Company\',this)">About us</li>' \
                '<li class="item" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul></div>'+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ DETAILS'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Established: '+str(result_row[5])+'</p><p>Employee Strength: '+str(result_row[6])+'</p>'+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ BRANCHES'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Location : ' + result_row[11] + '</p><p>Branches: '+ result_row[12]+'</p>'+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = 'EXPERTISE'
            template = lxml.etree.SubElement(category, 'template')
            expertise = result_row[13].split(',')
            expert_text = '<![CDATA[<p></p><div class="benefitsHold">\
            <h4 class="headIn">Expertise at '+result_row[1]+'</h4>\
            <ul>'
            for expert in expertise:
                expert_text +='<li>'+expert+'</li>'
            template.text = expert_text + '</ul></div>'+about_subtext+str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ CULTURE'
            template = lxml.etree.SubElement(category, 'template')
            culture_text = '<![CDATA[<p></p><div class="wow-cult"> \
                    <ul class="owl-carousel owl-theme repli">'
            cursor.execute("SELECT * FROM wow_culture_post WHERE postHide = 'N' AND postType = 'STRY' AND postDelete = 'NO' AND posthrId='" + str(result_row[0]) + "' ORDER BY postcrtDate DESC LIMIT 0,3")
            wow_culture_results = cursor.fetchall()
            for wow_culture_row in wow_culture_results:
                wow_culture_id = wow_culture_row[2]
                wow_culture_name = ((wow_culture_row[3]).strip()).replace(' ', '-')
                if wow_culture_row[7] == 'STRY':
                    cursor.execute("SELECT * FROM wow_post_story WHERE storypostId='" + str(wow_culture_row[1]) + "' AND storyDelete='NO' AND storyCover='YES'")
                    story_results = cursor.fetchall()
                    for story_row in story_results:
                        dater = wow_culture_row[11].strftime('%B %d, %Y')
                        culture_text += '<li class="item"> \
                            <img class="img-responsive" src="https://employer.wow.jobs/cache/'+wow_handler_id+'/'+story_row[2]+'" alt="image"> \
                            <h5>'+wow_culture_row[3]+'</h5> \
                            <h5 class="last-one">'+dater+'</h5> \
                            <div class="blockDis"> \
                            <a href="https://www.wow.jobs/' + wow_handler + '/posts/'+wow_culture_name+'/'+ str(wow_culture_row[1]) +'" \
                            target="_blank" class ="anchor-block">View story</a> \
                            </div></li>'
            template.text = culture_text+'</ul>'+about_subtext+str(result_row[0])
            f.write(tostring(aiml, pretty_print=True,xml_declaration=True  , encoding='UTF-8'))
    return 'Successfully Created!!!!'

@application.route("/wowculture")
def wowculture():
    cursor.execute("SELECT bft_insurance,bft_flexible_hours,bft_5days_week,bft_wmnf_atmp,bft_wmnf_locn, \
                    bft_cafeteria,bft_game_zone,bft_matpat_leav,bft_cab_srvc,bft_free_food,bft_dress_code, \
                    bft_yearly_bnus,bft_shifts,bft_equity,bft_reloc_alwc,bft_join_bnus,bft_wrk4m_home, \
                    bft_mand_offs,bft_fitness_cntr,bft_train_cert,bft_accomdtn,bft_creche,bft_kid_fdly, \
                    bft_pet_fdly,bft_parkg_fcty,bft_onsite_opty,bft_paid_hldy,bft_tution_rmbs,bft_401k, \
                    bft_hide FROM employer_benefits WHERE bft_hide='N' AND employer_id='3689'")
    benefitsName = [["bft_insurance" , "Insurance"],["bft_flexible_hours" , "Flexible Work Hours"],["bft_5days_week" , "5 Days a week"],["bft_wmnf_atmp" , "Women Friendly Atmosphere"],["bft_wmnf_locn" , "Women Friendly Location"],["bft_cafeteria" , "Cafeteria"],["bft_game_zone" , "Game Zone"],["bft_matpat_leav" , "Maternity & Paternity Leaves"],["bft_cab_srvc" , "Cab Service"],["bft_free_food" , "Free Food"],["bft_dress_code" , "No Dress Code"],["bft_yearly_bnus" , "Yearly Bonus"],["bft_shifts" , "Shifts"],["bft_equity" , "Equity"],["bft_reloc_alwc" , "Relocation Allowance"],["bft_join_bnus" , "Joining Bonus"],["bft_wrk4m_home" , "Work From Home"],["bft_mand_offs" , "Mandatory Offs"],["bft_fitness_cntr" , "Fitness Centre"],["bft_train_cert" , "Training & Certifications"],["bft_accomdtn" , "Accomodation"],["bft_creche" , "Creche"],["bft_kid_fdly" , "Kid Friendly"],["bft_pet_fdly" , "Pet Friendly"],["bft_parkg_fcty" , "Parking Facility"],["bft_onsite_opty" , "Onsite Opportunity"],["bft_paid_hldy" , "Paid Holidays"],["bft_tution_rmbs" , "Tution Fee Reimbursment"],["bft_401k" , "401K"], ["bft_hide", "N"]];
    if cursor.rowcount != 0:
        wow_benefits=cursor.fetchall()[0]
        benefits=[]
        for i in range(len(cursor.description)):
            if cursor.description[i][0]==benefitsName[i][0]:
                if wow_benefits[i]=='Y':
                    benefits.append(benefitsName[i][1])
        return make_response(jsonify({'culture':benefits,'fetchall':wowbenefits}))
    else :
        return '000'

@application.route("/chatdetails")
def chatdetails():
    # cursor.execute("SELECT REPLACE( bft_dress_code,  'Y',  'bft_dress_code.png' ) as bft_dress_code,REPLACE( bft_insurance,  'Y',  'bft_insurance.png' ) as bft_insurance, \
    #                        REPLACE( bft_flexible_hours,  'Y',  'bft_flexible_hours.png' ) as bft_flexible_hours,REPLACE( bft_5days_week,  'Y',  'bft_5days_week.png' ) as bft_5days_week, \
    #                        REPLACE( bft_wmnf_atmp,  'Y',  'bft_wmnf_atmp.png' ) as bft_wmnf_atmp,REPLACE( bft_wmnf_locn,  'Y',  'bft_wmnf_locn.png' ) as bft_wmnf_locn, \
    #                        REPLACE( bft_cafeteria,  'Y',  'bft_cafeteria.png' ) as bft_cafeteria,REPLACE( bft_game_zone,  'Y',  'bft_game_zone.png' ) as bft_game_zone, \
    #                        REPLACE( bft_matpat_leav,  'Y',  'bft_matpat_leav.png' ) as bft_matpat_leav,REPLACE( bft_cab_srvc,  'Y',  'bft_cab_srvc.png' ) as bft_cab_srvc, \
    #                        REPLACE( bft_free_food,  'Y',  'bft_free_food.png' ) as bft_free_food,REPLACE( bft_yearly_bnus,  'Y',  'bft_yearly_bnus.png' ) as bft_yearly_bnus, \
    #                        REPLACE( bft_shifts,  'Y',  'bft_shifts.png' ) as bft_shifts,REPLACE( bft_equity,  'Y',  'bft_equity.png' ) as bft_equity, \
    #                        REPLACE( bft_reloc_alwc,  'Y',  'bft_reloc_alwc.png' ) as bft_reloc_alwc,REPLACE( bft_join_bnus,  'Y',  'bft_join_bnus.png' ) as bft_join_bnus, \
    #                        REPLACE( bft_wrk4m_home,  'Y',  'bft_wrk4m_home.png' ) as bft_wrk4m_home,REPLACE( bft_mand_offs,  'Y',  'bft_mand_offs.png' ) as bft_mand_offs,\
    #                        REPLACE( bft_fitness_cntr,  'Y',  'bft_fitness_cntr.png' ) as bft_fitness_cntr,REPLACE( bft_train_cert,  'Y',  'bft_train_cert.png' ) as bft_train_cert,\
    #                        REPLACE( bft_accomdtn,  'Y',  'bft_accomdtn.png' ) as bft_accomdtn,REPLACE( bft_creche,  'Y',  'bft_creche.png' ) as bft_creche,\
    #                        REPLACE( bft_kid_fdly,  'Y',  'bft_kid_fdly.png' ) as bft_kid_fdly,REPLACE( bft_pet_fdly,  'Y',  'bft_pet_fdly.png' ) as bft_pet_fdly, \
    #                        REPLACE( bft_parkg_fcty,  'Y',  'bft_parkg_fcty.png' ) as bft_parkg_fcty,REPLACE( bft_onsite_opty,  'Y',  'bft_onsite_opty.png') as bft_onsite_opty, \
    #                        REPLACE( bft_paid_hldy,  'Y',  'bft_paid_hldy.png' ) as bft_paid_hldy,REPLACE( bft_tution_rmbs,  'Y',  'bft_tution_rmbs.png' ) as bft_tution_rmbs,\
    #                        REPLACE( bft_401k,  'Y',  'bft_401k.png' ) as bft_401k FROM  `employer_benefits` WHERE employer_id ='" + str(
    #     result_row[0]) + "'")
    # benefits_results = cursor.fetchall()
    # category = lxml.etree.SubElement(topic, 'category')
    # pattern = lxml.etree.SubElement(category, 'pattern')
    # pattern.text = 'BENEFITS'
    # template = lxml.etree.SubElement(category, 'template')
    # benefits_text = '<![CDATA['
    # for i in range(29):
    #     if benefits_results[i] != 'N':
    #         benefits_text = '
    cursor.execute("SELECT employer_id,replace(employer_name, char(153), '') AS employer_name,employer_website,employer_email,employer_mobile_number,employer_yr_founded,employer_strength,employer_logo,employer_desc,employer_address,job_count,replace(employer_location, char(150), '') AS employer_location,replace(employer_branches, char(150), '') AS employer_branches,employer_experts FROM employer_details LIMIT 0,3")
    company_results = cursor.fetchall()
    for result_row in company_results:
        with open('aiml/' + str(result_row[0]) + '.aiml', 'w') as f:
            aiml = lxml.etree.Element('aiml')
            category = lxml.etree.SubElement(aiml, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = (re.sub('[!@#.$~&()*]', '', result_row[1])).upper()
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template, 'set')
            set.set('name', 'topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<ul class="owl-carousel owl-theme repli">' \
                            '<li class="item"><a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Current Openings\')">Current opening</a></li>'\
                            '<li class="item"><a href="javascript:;" class="btn btn-info" onclick="cjoption(\'About Company\')">About Company</a></li>' \
                            '<li class="item"><a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Speak to HR\')">Speak to HR</a></li></ul>'
            topic = lxml.etree.SubElement(aiml, 'topic')
            topic.set('name', str(result_row[0]))
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '*'
            template = lxml.etree.SubElement(category, 'template')
            set = lxml.etree.SubElement(template, 'set')
            set.set('name', 'topic')
            set.text = str(result_row[0])
            template.text = '<![CDATA[<p>May I help you with following?</p>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Current Openings\')">Current Openings</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'About Company\')">About Company</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Speak to HR\')">Speak to HR</a>' \
                            '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Do you want to show me the culture\')">View Company Culture</a>'
            cursor.execute("SELECT * FROM `wow_handler` WHERE e_id='" + str(result_row[0]) + "'")
            wowhandler_result = cursor.fetchall()
            for handler_row in wowhandler_result:
                if handler_row[2] == None:
                    wow_handler = handler_row[1]
                else:
                    wow_handler = handler_row[2]
            cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='" + str(result_row[0]) + "' AND job_delete ='NO' AND job_publish ='PLA' ORDER BY job_crt_date DESC LIMIT 0 , 3")
            if cursor.rowcount != 0:
                job_results = cursor.fetchall()
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# CURRENT OPENINGS ^'
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
            pattern.text = '# ABOUT COMPANY ^'
            template = lxml.etree.SubElement(category, 'template')
            cursor.execute("SELECT founderName,founderDesg,founderAbout,founderImg_1,founderId FROM company_founders WHERE employer_id='" + str(result_row[0]) + "'")
            if cursor.rowcount != 0:
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
                    founder_text += '<p></p><img src="https://employer.wow.jobs/' + founder_row[3] + '"/><p>' + \
                                    founder_row[0] + '</p><p>' + result_row[1] + '</p>'
                template.text = founder_text + str(result_row[0])
            else:
                template.text = '<![CDATA[<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Here is some details about our company\')">Company Details</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Employer Expertize in\')">Expertise</a>' \
                                '<a href="javascript:;" class="btn btn-info" onclick="cjoption(\'Our Location and Branches\')">Location</a>' + str(
                    result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ DETAILS'
            template = lxml.etree.SubElement(category, 'template')
            template.text = '<![CDATA[<p>Established: ' + str(result_row[5]) + '</p><p>Employee Strength: ' + str(
                result_row[6]) + '</p>' + str(result_row[0])
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ HR'
            template = lxml.etree.SubElement(category, 'template')
            if result_row[6] == None:
                template.text = '<![CDATA[<p>Email Id: ' + str(result_row[3]) + '</p>' + str(result_row[0])
            else:
                template.text = '<![CDATA[<p>Mobile no: ' + str(result_row[4]) + '</p><p>Email Id: ' + str(result_row[3]) + '</p>' + str(result_row[0])
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
            category = lxml.etree.SubElement(topic, 'category')
            pattern = lxml.etree.SubElement(category, 'pattern')
            pattern.text = '_ CULTURE'
            template = lxml.etree.SubElement(category, 'template')
            culture_text = '<![CDATA['
            cursor.execute(
                "SELECT * FROM wow_culture_post WHERE postHide = 'N' AND postDelete = 'NO' AND posthrId='" + str(
                    result_row[0]) + "' ORDER BY postcrtDate DESC LIMIT 0,3")
            wow_culture_results = cursor.fetchall()
            for wow_culture_row in wow_culture_results:
                wow_culture_id = wow_culture_row[2]
                wow_culture_name = ((wow_culture_row[3]).strip()).replace(' ', '-')
                if wow_culture_row[7] == 'STRY':
                    cursor.execute("SELECT * FROM wow_post_story WHERE storypostId='" + str(
                        wow_culture_row[1]) + "' AND storyDelete='NO' AND storyCover='YES'")
                    story_results = cursor.fetchall()
                    for story_row in story_results:
                        culture_text += '<p><a class="btn btn-info" target="_blank" href="https://www.wow.jobs/' + wow_handler + '/' + wow_culture_name + '/' + wow_culture_name + '">' + \
                                        wow_culture_row[3] + '</a></p>'
                if wow_culture_row[7] == 'LINK':
                    cursor.execute("SELECT * FROM wow_post_link WHERE linkpostId='" + str(
                        wow_culture_row[1]) + "' AND linkDelete='NO'")
                    story_results = cursor.fetchall()
                    for story_row in story_results:
                        culture_text += '<p><a class="btn btn-info" target="_blank" href="https://www.wow.jobs/' + wow_handler + '/' + wow_culture_name + '/' + wow_culture_name + '">' + \
                                        wow_culture_row[3] + '</a></p>'
            template.text = culture_text + str(result_row[0])
            f.write(tostring(aiml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    return 'Successfully Created!!!!'

@application.route("/wowadmin")
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


@application.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor.execute("SELECT * from admin_table where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

@application.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

application.config.update(
    PROPAGATE_EXCEPTIONS = True
)

if __name__ == '__main__':
    application.run(host='0.0.0.0',port='80')

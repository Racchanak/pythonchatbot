import MySQLdb # Mysql ---
from flask import Flask, jsonify, make_response, send_from_directory
from flask import render_template
import aiml 
from flask_cors import CORS
import lxml
from lxml import etree
from lxml.etree import *
from OpenSSL import SSL
import re, os, sys
sys.setrecursionlimit(10000)

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
    company_results = employer_details()
    for result_row in company_results:
        wowhandler = wow_handlers(str(result_row[0]))
        if len(wowhandler) > 0:
            with open('aiml/' + str(result_row[0]) + '.aiml', 'w') as f:
                wow_handler = wowhandler[0]
                wow_handler_id = wowhandler[1]
                main_menu = '<ul class="owl-carousel owl-theme repli main-menu">' \
                            '<li class="item scroll" onclick="cjoption(\'Current Openings\',this)">Current opening</li>'\
                            '<li class="item scroll" onclick="cjoption(\'About Company\',this)">About us</li>'\
                            '<li class="item scroll" onclick="cjoption(\'Speak to HR\',this)">Speak to HR</li></ul>'
                aiml = lxml.etree.Element('aiml')
                category = lxml.etree.SubElement(aiml, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = (re.sub('[!@#.$~&()*]', '', result_row[1])).upper()
                template = lxml.etree.SubElement(category, 'template')
                set = lxml.etree.SubElement(template,'set')
                set.set('name','topic')
                set.text = str(result_row[0])
                template.text = '<![CDATA[<p></p>'+main_menu
                topic = lxml.etree.SubElement(aiml,'topic')
                topic.set('name',str(result_row[0]))
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '*'
                template = lxml.etree.SubElement(category, 'template')
                set = lxml.etree.SubElement(template,'set')
                set.set('name','topic')
                set.text = str(result_row[0])
                template.text = '<![CDATA[<p></p><p>May I help you with following?</p>'+main_menu
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'MAIN MENU'
                template = lxml.etree.SubElement(category, 'template')
                set = lxml.etree.SubElement(template,'set')
                set.set('name','topic')
                set.text = str(result_row[0])
                template.text = '<![CDATA[<p></p>'+main_menu
                jobresults = job_result(str(result_row[0]))
                if len(jobresults) > 0:
                    i_val = 0
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = '_ JOBS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template,'srai')
                    srai.text = 'OPENINGS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'JOBS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template,'srai')
                    srai.text = 'OPENINGS'
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
                    for job_row in jobresults:
                        job_text = '<![CDATA[<p></p><div class="jobList"><ul class="owl-carousel owl-theme repli job-list">'
                        for jobs_li in job_row:
                            job_name = ((jobs_li[1]).strip()).replace(' ', '-')
                            job_location = ((jobs_li[8]).strip()).replace(' ', '-')
                            job_experience = 'Exp: ' + str(jobs_li[10]) + '-' + str(jobs_li[11])
                            job_link = 'https://www.wow.jobs/' + wow_handler + '/' + job_name + '-jobs-' + job_location + '/' + str(jobs_li[0])
                            job_text += '<li class="item"><a class="anchor-block" target="_blank" href="' + job_link + '"><h5>' + jobs_li[1] + '</h5> <h5>' + jobs_li[8] + '</h5> \
                                        <h5>' + job_experience + '</h5> <div class="blockDis"> \
                                        Apply</div></a></li>'
                        if i_val == 0:
                            pattern_text = 'OPENINGS'
                        else:
                            pattern_text = 'MORE JOBS' + str(i_val)
                        if (i_val) < (len(jobresults) - 1):
                            job_text += '<li class="item"><a class="anchor-block job-more" target="_blank" \
                            href="https://www.wow.jobs/' + wow_handler + '" >View more</a></li>'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = pattern_text
                        template = lxml.etree.SubElement(category, 'template')
                        template.text = job_text + '</ul></div><div class="submenu">' + main_menu + '</div>' + str(result_row[0])
                        i_val = i_val + 1
                job_patterns = job_pattern(str(result_row[0]))
                if len(job_patterns) > 0:
                    for job_row in job_patterns:
                        if len(job_row[1]) > 1:
                            job_text = '<![CDATA[<p></p><div class="jobList"><ul class="owl-carousel owl-theme repli main-menu">'
                            for job_details in job_row[1]:
                                job_name = ((job_details[1]).strip()).replace(' ', '-')
                                job_location = ((job_details[2]).strip()).replace(' ', '-')
                                job_experience = 'Exp: ' + str(job_details[3]) + '-' + str(job_details[4])
                                job_link = 'https://www.wow.jobs/' + wow_handler + '/' + job_name + '-jobs-' + job_location + '/' + str(job_details[0])
                                job_text += '<li class="item"><a target="_blank" href="' + job_link + '">\
                                            <h5>' + job_details[1] + '</h5> <h5>' + job_details[2] + '</h5> \
                                            <h5>' + job_experience + '</h5> <div class="blockDis"> \
                                            <span class="anchor-block">Apply</span></div></a></li>'
                                job_li = '<a target="_blank" href="' + job_link + '"><div class="benefitsHold"> <h4 class="headIn">' + job_details[1] + '</h4> \
                                     <h5 class="blackColorText">' + job_details[2] + '</h5> <h5 class="blackColorText">' + job_experience + '</h5>'
                                if len(job_details[5]) > 0:
                                    job_li += '<h4 class="headIn">Skills for ' + job_details[1] + '</h4> <ul>'
                                    for jobskills in job_details[5]:
                                        job_li += '<li>' + jobskills[0] + ' -' + jobskills[1] + '</li>'
                                    job_li += '</ul><div class="blockDis">\
                                    <span class="anchor-block">Apply</span></div></div></a>'
                                job_li += '<div class="submenu">' + main_menu + '</div>'
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_row[0][0].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_row[0][0].upper()+' _'
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = '_ '+job_row[0][0].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_details[1].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                template.text = '<![CDATA[<p></p>' + job_li + str(result_row[0])
                            category = lxml.etree.SubElement(topic, 'category')
                            pattern = lxml.etree.SubElement(category, 'pattern')
                            pattern.text = job_row[0][0].upper()
                            template = lxml.etree.SubElement(category, 'template')
                            template.text = job_text + '</ul></div><div class="submenu">' + main_menu + '</div>' + str(result_row[0])
                        else:
                            for job_details in job_row[1]:
                                job_name = ((job_details[1]).strip()).replace(' ', '-')
                                job_location = ((job_details[2]).strip()).replace(' ', '-')
                                job_experience = 'Exp: ' + str(job_details[3]) + '-' + str(job_details[4])
                                job_link = 'https://www.wow.jobs/' + wow_handler + '/' + job_name + '-jobs-' + job_location + '/' + str(job_details[0])
                                job_li = '<a target="_blank" href="' + job_link + '"><div class="benefitsHold"> <h4 class="headIn">' + job_details[1] + '</h4> \
                                <h5 class="blackColorText">' + job_details[2] + '</h5> <h5 class="blackColorText">' + job_experience + '</h5>'
                                if len(job_details[5]) > 0:
                                    job_li += '<h4 class="headIn">Skills for ' + job_details[1] + '</h4> <ul>'
                                    for jobsskills in job_details[5]:
                                        job_li += '<li>' + jobsskills[0] + ' -' + jobsskills[1] + '</li>'
                                    job_li += '</ul><div class="blockDis">\
                                    <span class="anchor-block">Apply</span></div></div></a>'
                                job_li += '<div class="submenu">' + main_menu + '</div>'
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_row[0][0].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_row[0][0].upper()+' _'
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = '_ '+job_row[0][0].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                srai = lxml.etree.SubElement(template,'srai')
                                srai.text = job_details[1].upper()
                                category = lxml.etree.SubElement(topic, 'category')
                                pattern = lxml.etree.SubElement(category, 'pattern')
                                pattern.text = job_details[1].upper()
                                template = lxml.etree.SubElement(category, 'template')
                                template.text = '<![CDATA[<p></p>'+ job_li + str(result_row[0])
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
                pattern.text = 'WHO WE ARE'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'COMPANY'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'OUR STORY'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'COMPANY'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HELP'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'COMPANY'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'ABOUT'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'COMPANY'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'ABOUT _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'COMPANY'
                about_text = '<ul class="owl-carousel owl-theme repli main-menu"> \
                    <li class="item " onclick="cjoption(\'Work Culture\',this)">Work culture</li> \
                    <li class="item" onclick="cjoption(\'Expertise\',this)">Expertise</li>'
                wow_benefits = job_benefit(str(result_row[0]))
                if len(wow_benefits) > 0:
                    about_text += '<li class="item" onclick="cjoption(\'Benefits\',this)">Benefits</li>'
                wow_location = wow_locations(str(result_row[0]))
                if len(wow_location) > 0:
                    about_text += '<li class="item" onclick="cjoption(\'Location\',this)">Location</li>'
                founder_results = job_founder(str(result_row[0]))
                if len(founder_results) > 0:
                    about_text += '<li class="item" onclick="cjoption(\'Founder\',this)">Founders</li>'
                about_text +='<li class="item" onclick="cjoption(\'Main Menu\',this)">Main Menu</li></ul>'
                about_subtext ='<div class="submenu">'+about_text+'</div>'
                if len(wow_benefits) > 0:
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'BENEFITS'
                    template = lxml.etree.SubElement(category, 'template')
                    benefit_text = '<![CDATA[<p></p><div class="benefitsHold">\
                                    <h4 class="headIn">Benefits at ' + result_row[1] + '</h4>\
                                    <ul>'
                    for benefits in wow_benefits:
                        benefit_text += '<li>' + benefits + '</li>'
                    template.text = benefit_text + '</ul></div>' + about_subtext+ str(result_row[0])
                if len(wow_location) > 0:
                    for location in wow_location:
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = 'OFFICE'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = 'WHERE ?'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = 'OFFICE _'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = '_ WHERE'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = 'WHERE _'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = '_ OFFICE'
                        template = lxml.etree.SubElement(category, 'template')
                        srai = lxml.etree.SubElement(template,'srai')
                        srai.text = 'LOCATION'
                        category = lxml.etree.SubElement(topic, 'category')
                        pattern = lxml.etree.SubElement(category, 'pattern')
                        pattern.text = 'LOCATION'
                        template = lxml.etree.SubElement(category, 'template')
                        template.text = '<![CDATA[<p></p> \
                                <div class="hidden"><span class="lat">' + str(location[7]) + '</span> \
                                <span class="long">' + str(location[8]) + '</span><span class="name">' + location[2] + '</span></div> \
                                <div class="map_disp"></div> \
                                <p class="mapPt"><a target="_blank" href="https://www.google.co.in/maps/place/' + re.sub('[ ]', '+', location[2]) + '/@' + str(location[7]) + ',' + str(location[8]) + '"> \
                                Get Direction</a></p>' + about_subtext + str(result_row[0])
                if len(founder_results) > 0:
                    founder_text = '<![CDATA[<p></p><div class="wow-cult"><ul class="owl-carousel owl-theme repli">'
                    for founder_row in founder_results:
                        founder_text += '<li class="item"><div class="overflow-max-168"><img src="https://employer.wow.jobs/' + founder_row[3] + '"/></div><h5>'+founder_row[0]+'</h5><h5>' + founder_row[1] + '</h5></li>'
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
                    pattern.text = 'CEO'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template,'srai')
                    srai.text = 'FOUNDER'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'CTO'
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
                    template.text = founder_text + '</ul></div>'+about_subtext+str(result_row[0])
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'COMPANY'
                template = lxml.etree.SubElement(category, 'template')
                template.text = '<![CDATA[<p></p><div class="aboutCompany"><p></p> \
                    <p class="text-left"><span class="headIn">About company</span>'+result_row[8]+'<span class="blockDis">\
                    <a target="_blank" href="https://www.wow.jobs/' + wow_handler+'" class="anchor-block">Read more</a></span></p> \
                    </div><p>Do you want to know more about us?</p>'+about_text + '</ul>' + str(result_row[0])
                wow_tip = wow_tips(str(result_row[0]))
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ HR DETAILS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'SPEAK TO HR'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'PROFILE'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'RESUME'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'CV'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# HR DETAILS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template,'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR DETAILS #'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR DETAILS _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR CONTACT'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR CONTACT'
                template = lxml.etree.SubElement(category, 'template')
                hr_menu = '<ul class="owl-carousel owl-theme repli main-menu">' \
                            '<li class="item " onclick="cjoption(\'Hr Email\',this)">Email HR</li>'
                if len(wow_tip) > 0:
                    hr_menu += '<li class="item" onclick="cjoption(\'Interview Tips\',this)">Interview Tips</li>'
                hr_menu += '<li class="item" onclick="cjoption(\'Main Menu\',this)">Main Menu</li></ul>'
                template.text = '<![CDATA[<p></p>'+hr_menu+str(result_row[0])
                tips_menu = '<![CDATA[<p></p><div class="email"><p></p><p>Email Id: '+result_row[3]+'</p></div> \
                            <div class="submenu"><ul class="owl-carousel owl-theme repli main-menu">'
                if len(wow_tip) > 0:
                    tips_menu += '<li class="item" onclick="cjoption(\'Interview Tips\',this)">Interview Tips</li>'
                    tips_text = '<![CDATA[<p></p><div class="tips"><p></p>'
                    for tips in wow_tip:
                        tips_text += '<p>' + tips[0] + '</p>'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = '_ INTERVIEW TIPS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = '# INTERVIEW TIPS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'INTERVIEW TIPS #'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'INTERVIEW TIPS _'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'INTERVIEW TIPS _'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = '_ INTERVIEW TIPS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = '# INTERVIEW TIPS'
                    template = lxml.etree.SubElement(category, 'template')
                    srai = lxml.etree.SubElement(template, 'srai')
                    srai.text = 'INTERVIEW TIPS'
                    category = lxml.etree.SubElement(topic, 'category')
                    pattern = lxml.etree.SubElement(category, 'pattern')
                    pattern.text = 'INTERVIEW TIPS'
                    template = lxml.etree.SubElement(category, 'template')
                    template.text = tips_text + '</div><div class="submenu">\
                                <ul class="owl-carousel owl-theme repli main-menu"> \
                                <li class="item" onclick="cjoption(\'Hr Email\',this)">Email HR</li>\
                                <li class="item" onclick="cjoption(\'Main Menu\',this)">Main Menu</li></ul></div>' +str(result_row[0])
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ HR EMAIL'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# HR EMAIL'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR EMAIL #'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR EMAIL _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'EMAIL HR _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ EMAIL HR'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# EMAIL HR'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'HR EMAIL'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'HR EMAIL'
                template = lxml.etree.SubElement(category, 'template')
                template.text = tips_menu+'<li class="item" onclick="cjoption(\'Main Menu\',this)">\
                                Main Menu</li></ul></div>'+str(result_row[0])
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ EXPERTISE'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '# EXPERTISE'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'EXPERTISE #'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'EXPERTISE _'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'SKILLS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'OUR SKILLS'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'EXPERTISE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'EXPERTISE'
                template = lxml.etree.SubElement(category, 'template')
                expertise = result_row[13].split(',')
                expert_text = '<![CDATA[<p></p><div class="benefitsHold"><h4 class="headIn">Expertise at '+result_row[1]+'</h4><ul>'
                for expert in expertise:
                    expert_text +='<li>'+expert+'</li>'
                template.text = expert_text + '</ul></div>'+about_subtext+str(result_row[0])
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'WHAT WE DO'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'CULTURE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = '_ CULTURE'
                template = lxml.etree.SubElement(category, 'template')
                srai = lxml.etree.SubElement(template, 'srai')
                srai.text = 'CULTURE'
                category = lxml.etree.SubElement(topic, 'category')
                pattern = lxml.etree.SubElement(category, 'pattern')
                pattern.text = 'CULTURE'
                template = lxml.etree.SubElement(category, 'template')
                culture_text = '<![CDATA[<p></p><div class="wow-cult"> \
                        <ul class="owl-carousel owl-theme repli">'
                wow_culture_results = wow_culture(str(result_row[0]))
                for wow_culture_row in wow_culture_results:
                    wow_culture_name = ((wow_culture_row[3]).strip()).replace(' ', '-')
                    if wow_culture_row[7] == 'STRY':
                        story_results = wow_story(str(wow_culture_row[1]))
                        for story_row in story_results:
                            dater = wow_culture_row[11].strftime('%B %d, %Y')
                            culture_text += '<li class="item"> \
                                <div class="overflow-max"> \
                                <img class="img-responsive" src="https://employer.wow.jobs/cache/'+wow_handler_id+'/'+story_row[2]+'" alt="image"> \
                                </div><h5>'+wow_culture_row[3]+'</h5> \
                                <h5 class="last-one">'+dater+'</h5> \
                                <div class="blockDis"> \
                                <a href="https://www.wow.jobs/' + wow_handler + '/posts/'+wow_culture_name+'/'+ str(wow_culture_row[1]) +'" \
                                target="_blank" class ="anchor-block">View story</a> \
                                </div></li>'
                culture_text += '<li class="cul-more"><a class="anchor-block" target="_blank" \
                    href="https://www.wow.jobs/' + wow_handler + '" >View more</a></li>'
                template.text = culture_text+'</ul></div>'+about_subtext+str(result_row[0])
                f.write(tostring(aiml, pretty_print=True,xml_declaration=True  , encoding='UTF-8'))
    return 'Successfully Created!!!!'

def employer_details():
    cursor.execute("SELECT employer_id,replace(employer_name, char(153), '') AS employer_name,employer_website,\
      employer_email,employer_mobile_number,employer_yr_founded,employer_strength,employer_logo,replace(replace\
      (replace(replace(replace(replace(replace(replace(employer_desc,char(149), ''),char(147), ''), char(148), ''),\
       char(153), ''), char(150),''), char(146), ''),char(145), ''),char(39), '') AS employer_desc,employer_address,\
       job_count,replace(employer_location,char(150), '') AS employer_location,replace(employer_branches, char(150), '')\
      AS employer_branches,employer_experts FROM employer_details")
    return cursor.fetchall()

def wow_handlers(employer_id):
    cursor.execute("SELECT * FROM `wow_handler` WHERE e_id='" +employer_id + "'")
    wowhandler_result = cursor.fetchall()
    data = []
    for handler_row in wowhandler_result:
        wow_handler_id = handler_row[1]
        if handler_row[2] == None:
            wowhandler = wow_handler_id
        else:
            wowhandler = handler_row[2]
        data.extend((wowhandler,wow_handler_id))
    return data

def job_result(employer_id):
    job_count = job_counts(employer_id)
    if job_count%5 == 0:
        job_loop = job_count/5
    else:
        job_loop = (job_count/5)+1
    data = []
    start = 0
    for jobee in range(job_loop):
        job_jobee = job_results(str(employer_id), str(start))
        job_data = []
        for job_row in job_jobee:
            job_data.append(job_row)
        data.append(job_data)
        start = start + 5
    return data

def job_counts(employer_id):
    cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='" +employer_id+ "' AND job_delete ='NO' AND \
            job_publish ='PLA' ORDER BY job_mod_date")
    return cursor.rowcount

def job_results(employer_id,start):
    cursor.execute("SELECT * FROM job_details WHERE job_hr_id ='" +employer_id+ "' AND job_delete ='NO' AND \
            job_publish ='PLA' ORDER BY job_mod_date DESC LIMIT " +start+ " , 5")
    return cursor.fetchall()

def wow_story(story_id):
    cursor.execute("SELECT * FROM wow_post_story WHERE storypostId='" +story_id+ "' AND storyDelete='NO' AND storyCover='YES'")
    return cursor.fetchall()

def job_pattern(employer_id):
    cursor.execute("SELECT DISTINCT replace(replace(replace(job_title,'Junior', ''),'Senior', ''),'Developer', '') as job_title \
        FROM job_details WHERE job_hr_id ='"+employer_id+"' AND job_delete ='NO' AND job_publish ='PLA' ORDER BY job_mod_date DESC")
    job_results = cursor.fetchall()
    data = []
    for job_row in job_results:
        cursor.execute("SELECT * FROM job_details WHERE job_title LIKE '%"+job_row[0].replace(' ', "%")+"%' AND \
        job_hr_id ='"+employer_id+"' AND job_delete ='NO' AND job_publish ='PLA' GROUP BY job_title ORDER BY job_mod_date DESC")
        wow_job_results = cursor.fetchall()
        job_data = []
        for wow_job_row in wow_job_results:
            job_skills = job_skill(str(wow_job_row[0]))
            skills = []
            if len(job_skills) > 0:
                for skill in job_skills:
                    skills.append((skill[2],skill[3]))
            job_data.append((wow_job_row[0],wow_job_row[1],wow_job_row[8],wow_job_row[10],wow_job_row[11],skills))
        data.append((job_row,job_data))
    return data

def job_benefit(employer_id):
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
                    ["bft_paid_hldy", "Paid Holidays"], ["bft_tution_rmbs", "Tuition Fee Reimbursment"],
                    ["bft_401k", "401K"], ["bft_hide", "N"]]
    cursor.execute("SELECT bft_insurance,bft_flexible_hours,bft_5days_week,bft_wmnf_atmp,bft_wmnf_locn, \
            bft_cafeteria,bft_game_zone,bft_matpat_leav,bft_cab_srvc,bft_free_food,bft_dress_code, \
            bft_yearly_bnus,bft_shifts,bft_equity,bft_reloc_alwc,bft_join_bnus,bft_wrk4m_home, \
            bft_mand_offs,bft_fitness_cntr,bft_train_cert,bft_accomdtn,bft_creche,bft_kid_fdly, \
            bft_pet_fdly,bft_parkg_fcty,bft_onsite_opty,bft_paid_hldy,bft_tution_rmbs,bft_401k, \
            bft_hide FROM employer_benefits WHERE bft_hide='N' AND employer_id='"+employer_id+"'")
    wow_benefits = cursor.fetchall()
    benefits_result = []
    if len(wow_benefits) > 0:
        for i in range(len(cursor.description)):
            if cursor.description[i][0] == benefitsName[i][0]:
                if wow_benefits[0][i] == 'Y':
                    benefits_result.append(benefitsName[i][1])
    return benefits_result

def wow_locations(employer_id):
    cursor.execute("SELECT * FROM employer_places_around WHERE plc_delete = 'N' AND employer_id ='"+employer_id+"'")
    return cursor.fetchall()

def job_founder(employer_id):
    cursor.execute("SELECT founderName,founderDesg,founderAbout,founderImg_1,founderId FROM \
          company_founders WHERE employer_id='" +employer_id+ "' ORDER BY founderId ASC")
    return cursor.fetchall()

def job_skill(job_id):
    cursor.execute("SELECT skill_id,skill_job_id,replace(replace(replace(replace(replace(replace(skill_name, char(145), ''),\
        char(146), ''), char(39), ''),char(34), ''),char(148), ''), char(147), '')AS skill_name,\
        skill_level,skill_delete FROM job_skills WHERE skill_job_id='" +job_id+ "' AND skill_delete='NO'")
    return cursor.fetchall()

def wow_culture(employer_id):
    cursor.execute("SELECT * FROM wow_culture_post WHERE postHide = 'N' AND postType = 'STRY' AND postDelete = 'NO' \
      AND posthrId='" +employer_id+ "' ORDER BY postcrtDate DESC LIMIT 0,5")
    return cursor.fetchall()

def wow_tips(employer_id):
    cursor.execute("SELECT replace(replace(replace(replace(replace(replace(replace(replace(replace(note_desc,char(176),'')\
       ,char(149), ''),char(147), ''), char(148), ''),char(153), ''), char(150),''), char(146), ''),\
       char(145), ''),char(39), '') AS note_desc FROM employer_notes WHERE \
       employer_id = '" +employer_id+ "' AND note_delete = 'N' ORDER BY note_crtdt DESC")
    return cursor.fetchall()

@application.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

application.config.update(
    PROPAGATE_EXCEPTIONS = True
)

if __name__ == '__main__':
    # application.run(host='0.0.0.0',port='80')
    context = ('/home/srinathp_appiness/cert/wow.jobs.chained.crt', '/home/srinathp_appiness/chatbot.wow.jobs.key')
    application.run(host='0.0.0.0',port='443', debug = False/True, ssl_context=context)

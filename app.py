"""
Flask web site with a calculator for 
control times for ACP Brevets 
"""

import flask
import math
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
global BREV_DISTANCE 
global START_DATE_TIME 
global INPUT_UNIT  

import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
    """
    Calculates open/close times from miles, using rules 
    described at http://www.rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the controle distance 
    in either km or miles. 
    """
    global INPUT_UNIT
    global BREV_DISTANCE
    global START_DATE_TIME
    distance = request.args.get('controle_dist', 0, type=int)
    if (INPUT_UNIT == "miles"):
        distance = distance * 1.60934 #convert to km
        distance = round(distance) #round to nearest km before using in calcs
    open_duration = OpenDuration(distance, BREV_DISTANCE) #array with 2 ints in it
    open_hours = open_duration[0]
    open_minutes = open_duration[1]
    
    close_duration = CloseDuration(distance, BREV_DISTANCE)
    close_hours = close_duration[0]
    close_minutes= close_duration[1]
    
    open_time = START_DATE_TIME.replace(hours=+open_hours)
    open_time = open_time.replace(minutes=+open_minutes)
    str_open = open_time.format("YYYY/MM/DD HH:mm")
    close_time = START_DATE_TIME.replace(hours=+close_hours)
    close_time = close_time.replace(minutes=+close_minutes)
    str_close = close_time.format("YYYY/MM/DD HH:mm")
    
    
    rslt = {"open_time": str_open, "close_time": str_close} 
    return jsonify(result=rslt)


def OpenDuration(controle_dist, brev_dist):
    """
    This function returns the open duration; i.e. the start time plus this open duration 
    is the earliest time in which you can arrive to the controle at controle_dist in a brevet 
    of brev_dist. 
    Arguments:
        controle_dist: the distance in km from the starting point to this controle 
        brev_dist: the distance in km of the whole brevet 
    Returns: the open duration 
    """
    t = 0
    if (controle_dist == 0):
        return [0,0]
        
    if (controle_dist > brev_dist):
        controle_dist = brev_dist #if hit the brev_dist then opening is calculated using brev_dist
        
    if (0<controle_dist<=200):
        t = (controle_dist/34)
    elif (200<controle_dist<=400):
        remaining = controle_dist - 200
        t = (200/34) + (remaining/32)
    elif (400<controle_dist<=600):
        remaining = controle_dist - 400
        t = (200/34) + (200/32) + (remaining/30)
    elif (600<controle_dist<=1000):
        remaining = controle_dist - 600
        t = (200/34) + (200/32) + (200/30) + (remaining/28)
        
    hours = math.floor(t)
    dec = t - hours
    min_unrounded = dec * 60
    min = round(min_unrounded)
    hours_min = [hours, min]
    return hours_min

def CloseDuration(controle_dist, brev_dist):
    """
    This function returns the close duration; i.e. the start time plus this close duration
    is the latest time in which you can arrive to the controle at controle_dist in a brevet 
    of brevet_dist. 
    Arguments:
        controle_dist: the distance in km from the starting point to this controle 
        brev_dist: the distance in km of the whole brevet 
    Returns: the close duration 
    """
    t = 0
    time_limits = {200:[13,30], 300:[20,0], 400:[27,0], 600:[40,0], 1000:[75,0]}
    if (controle_dist == 0):
        return [1,0]
    elif (controle_dist >= brev_dist):
        return time_limits[brev_dist]
    else:
        if (0<controle_dist<=600):
            t = (controle_dist/15)
        elif (600<controle_dist<=1000):
            remaining = controle_dist - 600
            t = (600/15) + (remaining/11.428)   
      
    hours = math.floor(t)
    dec = t - hours
    min_unrounded = dec * 60
    min = round(min_unrounded)
    hours_min = [hours, min]
    return hours_min  
        
  
@app.route("/save_brevdistance")
def save_BrevDistance():
  """
  Save the brevet distance 
  """
  global BREV_DISTANCE
  BREV_DISTANCE = request.args.get('brev_dist', 0, type=int)
  return "nothing" #must return something else get error

  
@app.route("/save_StartDateTime")
def save_StartDateTime():
  """
  Save the start date and time 
  """
  global START_DATE_TIME
  start_date_time = request.args.get('start_datetime', 0, type=str)
  arrow_start_date_time = arrow.get(start_date_time, 'YYYY/MM/DD HH:mm')
  START_DATE_TIME = arrow_start_date_time
  return "none" 
  
@app.route("/save_InputUnit")
def save_InputUnit():
  """
  Save the input unit, either km or miles.  
  """
  global INPUT_UNIT
  INPUT_UNIT = request.args.get('input_unit', 0, type=str)
  return "nothing" 
  

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    # Standalone. 
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    app.debug=False
    

    

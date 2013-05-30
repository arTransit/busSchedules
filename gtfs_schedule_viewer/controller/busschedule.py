from flask import Flask, jsonify, request,g,Response
from contextlib import closing
import sqlite3
import json

# configuration
DATABASE = 'C:/AndrewRoss/Work/busSchedules/gtfs_schedule_viewer/controller/schedule.db'
DEBUG = True
SECRET_KEY = 'a long secret key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def testRoot():
    result = query_db('select * from sqlite_master;')
    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/systems')
def systems():
    result = query_db('select * from systems;')
    return Response(json.dumps(result),  mimetype='application/json')
    
@app.route('/routes')
def routes():
    system = request.args.get('system', '')
    result = query_db('select * from routes where agency_id = ?',[system])
    #print result
    return Response(json.dumps(result),  mimetype='application/json')
    
@app.route('/stops')
def stops():
    system = request.args.get('system', '')
    route = request.args.get('route', '')
    direction = request.args.get('direction', '')
    date=request.args.get('date', '')
    #print [system,route,direction,date]
    #[{"direction": 0, "run_number": 1, "stop_order": 0, "agency_id": 1, "stop_short_name": "first stop", "date_code": 1, "stop_id": 100100, "date": 20130502, "route_short_name": "route_4", "departure_time": "08:22"}, {"direction": 0, "run_number": 1, "stop_order": 1, "agency_id": 1, "stop_short_name": "second stop", "date_code": 1, "stop_id": 100102, "date": 20130502, "route_short_name": "route_4", "departure_time": "08:30"}, {"direction": 0, "run_number": 1, "stop_order": 2, "agency_id": 1, "stop_short_name": "next stop", "date_code": 1, "stop_id": 100103, "date": 20130502, "route_short_name": "route_4", "departure_time": "08:35"}, {"direction": 0, "run_number": 1, "stop_order": 3, "agency_id": 1, "stop_short_name": "last stop", "date_code": 1, "stop_id": 100104, "date": 20130502, "route_short_name": "route_4", "departure_time": "08:38"}]
    
    query = "select run_number,stop_order,stop_id,stop_short_name,departure_time from route_times join date_codes on date_codes.agency_id=route_times.agency_id and date_codes.date_code=route_times.date_code where route_times.agency_id=? and route_times.route_short_name=? and route_times.direction=? and date_codes.date=? order by run_number,stop_order"
    
    q1 = "select date_code from date_codes where date =? and agency_id=?"
    q2 = "select run_number,stop_order,stop_id,stop_short_name,departure_time from route_times where agency_id=? and route_short_name=? and direction=? and date_code=? order by run_number,stop_order"

    date_code=query_db( q1,[date,system],1 )['date_code']
    # print "date_code " + str(date_code)
    result=dict(system=system, route=route, direction=direction)
    current_run_number = -1
    
    tripList=[]
    stopList=[]
    for r in query_db( q2,[system,route,direction,date_code] ):
        run_number = r['run_number']
        print "run_number " + str(run_number)
        print "current_run_number " + str(current_run_number)
        #print "stopList " + str(stopList)
        if current_run_number != run_number:
            if current_run_number > -1:
                tripList.append( dict(run_number=current_run_number, stops=stopList))
                
            stopList = [ dict(stop_order=r['stop_order'],stop_id=r['stop_id'],stop_short_name=r['stop_short_name'],departure_time=r['departure_time']) ]
            current_run_number = run_number
        else:
            stopList.append( dict(stop_order=r['stop_order'],stop_id=r['stop_id'],stop_short_name=r['stop_short_name'],departure_time=r['departure_time']) )
    if current_run_number > -1:
        tripList.append( dict(run_number=current_run_number, stops=stopList))
    result['trips']=tripList
    return Response(json.dumps(result),  mimetype='application/json')

    
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

    
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
if __name__ == '__main__':
    app.run(debug=True)


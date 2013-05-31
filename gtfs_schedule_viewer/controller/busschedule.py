from flask import Flask, jsonify, request,g,Response
from contextlib import closing
import sqlite3
import json
import os

# configuration
DATABASE = os.path.dirname(os.path.abspath(__file__)) +'\schedule.db'
DEBUG = True

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
    
    query = "select route_short_name,route_long_name from routes where agency_id=? and route_short_name=?"
    
    r = query_db( query,[system,route],1 )
    route_display_name = r['route_short_name'] + ' ' + r['route_long_name']
    
    query = "select run_number,stop_order,stop_id,stop_short_name,departure_time from route_times where agency_id=? and route_short_name=? and direction=? and date_code in (select date_code from date_codes where date=?) order by run_number,stop_order"

    result=dict(system=system, route=route, direction=direction, 
            route_display_name=route_display_name, date=date)
    #result=dict(system=system, route=route, direction=direction )
    current_run_number = -1
    tripList=[]
    stopList=[]
    
    for r in query_db( query,[system,route,direction,date] ):
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


busSchedules
============

An apache/python/jquery app to query bus route information and display list of stops and departure times, for all trips, for a given route.
Data is derived from the GTFS.

Note: schedule.db is not included in this repository.

Apache config:

  WSGIScriptAlias /busschedule "C:/AndrewRoss/Work/busSchedules/gtfs_schedule_viewer/controller/busschedule.wsgi"
  Alias /bs "C:/AndrewRoss/Work/busSchedules/gtfs_schedule_viewer/view"

  <Directory C:/AndrewRoss/Work/busSchedules/gtfs_schedule_viewer/controller>
      Order deny,allow
	    Allow from all
  </Directory>

  <Directory C:/AndrewRoss/Work/busSchedules/gtfs_schedule_viewer/view>
	    Order deny,allow
	    Allow from all
  </Directory>
  
  

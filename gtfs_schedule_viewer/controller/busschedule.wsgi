import sys

sys.path.append(r"C:\AndrewRoss\Work\busSchedules\gtfs_schedule_viewer\controller")
from busschedule import app as app
#from test import app as application

### Uncomment to enable detailed debugging info
from werkzeug.debug import DebuggedApplication 
application = DebuggedApplication(app, True)
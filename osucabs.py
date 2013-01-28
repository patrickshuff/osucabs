#!/bin/env python


# This is not good form, this should probably be done in the apache config
import site, sys
site.addsitedir('/webdata/osucabs')

from math import *
import bustime, web, json
from pymongo import Connection
MONGOSERVER='localhost'
DBNAME='osucabs'

conn = Connection(MONGOSERVER, 27017)
db = conn['bustime']
routesdb = db["%sroutes" % DBNAME]
stopsdb = db["%sstops" % DBNAME]

# This is not good form, this should probably be done in the apache config

try:
    import settings
except ImportError:
    sys.exit("You must edit settings.py and add your api key!  Please do this!")


# User defined stuff
baseurl = 'http://trip.osu.edu/bustime/api/v1/'

# You 
apikey =  settings.apikey 
TITLE = 'OSUCABS.com'

bt = bustime.bustime(apikey=apikey, baseurl=baseurl)

urls = (
    '/?', 'index',
    '/routelist/(.*)', 'routelist',
    '/gpsdata/?', 'gpsdata',
    '/busstop/(.*)', 'busstop',
)
app = web.application(urls, globals())
application = web.application(urls, globals()).wsgifunc()
render = web.template.render('/webdata/osucabs/html/')

class index:
    def GET(self):
        i = web.input()
        if routesdb.count() == 0: capturedata()
        return render.index(TITLE,routesdb.find(),getfavs())

class routelist:
    def GET(self, route):
        routes = filter(lambda x: x["rt"].lower() == route.lower(),routesdb.find())
        if any(routes):  return render.routelist(TITLE,routes[0]["stops"])
        else: return render.index(TITLE,routes,getfavs())

class gpsdata:
    def GET(self):
        i = web.input()
        stops = list(set(map(lambda x: (distance(i,x),x["stpid"],x["stpnm"]), stopsdb.find())))
        stops.sort()
        if stops: return render.gpsdata(stops[:6])
        return  ''

def distance(i, stop):
    lat1 = float(i.lat)
    lon1 = float(i.lon)
    lat2 = float(stop["lat"])
    lon2 = float(stop["lon"])
    r = 3963.0
    return 3963.0 * acos(sin(lat1/57.2958) * sin(lat2/57.2958) + cos(lat1/57.2958) * cos(lat2/57.2958) *  cos(lon2/57.2958 -lon1/57.2958))

class busstop:
    def GET(self, stop=''):
        stp = filter(lambda x: x["stpid"] == stop,stopsdb.find())
        if not any(stp): return render.index(TITLE,routesdb.find(),getfavs())
        stpnm = stp[0]["stpnm"]
        favs = getfavs()
        favs = filter(lambda x: x["stpid"] != str(stop),favs)
        favs.append({"stpid": str(stop), "stpnm": stpnm})
        setfavs(favs)
        return render.busstop(stop, stpnm, bt.getpredictions(stpid=stop))


def getfavs():
    try:
        favs = json.loads(web.cookies().get("favs"))
        favs.reverse()
    except:
        favs = []
    return favs[:6]

def setfavs(favs):
    web.setcookie("favs",json.dumps(favs),expires=12345886)

def capturedata():
    print "Grabbing all routes from their servers"
    routes = bt.getroutes()
    print "Populating routes with all of their stops in all directions"
    allstops = bustime.populatestops(bt,routes)
    print "Dropping current table"
    routesdb.drop()
    stopsdb.drop()
    print "Inserting into database"
    routesdb.insert(routes)
    stopsdb.insert(allstops)

if __name__ == "__main__":
    if routesdb.count() == 0: capturedata()
    app.run()

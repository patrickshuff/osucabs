import urllib, time, datetime
import lxml.etree as etree

class bustime (object):
    apikey = ''
    baseurl = ''
    directions = False
    def __init__(self, apikey='', baseurl='', **kwargs):
        self.apikey = kwargs.get("apikey", apikey)
        self.baseurl = kwargs.get("baseurl", baseurl)

    def getvehicles(self, rt='',vid='', **kwargs):
        """This modules will get vehicle information by route(rt) or by vehicle id (vid).  The
        routes can be either a list of comma-delimeted string.
        """
        params = {"key": self.apikey}
        request = "getvehicles"
        rt = kwargs.get("rt",rt)
        vid = kwargs.get("vid",vid)
        if rt:
            if type(rt) is list: rt = ",".join(rt)
            params["rt"] = rt
        elif vid:  params["vid"] = vid
        else:   print "Must pass a rt of vid"
        return [a for a in _pulldata(self.baseurl, request, params)]

    def getpredictions(self, stpid='', rt='',vid='', top='', **kwargs):
        """This modules will get vehicle information by route(rt) or by vehicle id (vid).  The
        routes can be either a list of comma-delimeted string.
        """
        params = {"key": self.apikey}
        request = "getpredictions"
        rt = kwargs.get("rt",rt)
        vid = kwargs.get("vid",vid)
        stpid = kwargs.get("stpid",stpid)
        params["top"] = kwargs.get("top",top)
        if stpid:
            if type(stpid) is list: stpid = ",".join(stpid)
            params["stpid"] = stpid
        elif rt:
            if type(rt) is list: rt = ",".join(rt)
            params["rt"] = rt
        elif vid:
            if type(vid) is list: vid = ",".join(vid)
            params["vid"] = vid
        else:   print "Must pass a rt or vid or stpid"
        predictions = [a for a in _pulldata(self.baseurl, request, params)]
        for pr in predictions:
            d = datetime.datetime.strptime(pr["prdtm"],"%Y%m%d %H:%M")
            mins = int(d.strftime("%M")) + int(d.strftime("%H")) * 60
            now = int(d.now().strftime("%M")) + int(d.now().strftime("%H")) * 60
            pr.diff = abs(mins - now) % 1440
        return predictions
                                                    
        
    def getservicebulletins(self, stpid='', rt='',rtdir='', top='', **kwargs):
        """This modules will get vehicle information by route(rt) or by vehicle id (rtdir).  The
        routes can be either a list of comma-delimeted string.
        """
        params = {"key": self.apikey}
        request = "getservicebulletins"
        rt = kwargs.get("rt",rt)
        rtdir = kwargs.get("rtdir",rtdir)
        stpid = kwargs.get("stpid",stpid)
        params["top"] = kwargs.get("top",top)
        if stpid:
            if type(stpid) is list: stpid = ",".join(stpid)
            params["stpid"] = stpid
        elif rt:
            if type(rt) is list: rt = ",".join(rt)
            params["rt"] = rt
        elif rtdir:
            if type(rtdir) is list: rtdir = ",".join(rtdir)
            params["rtdir"] = rtdir
        else:   print "Must pass a rt or rtdir or stpid"
        return [a for a in _pulldata(self.baseurl, request, params)]

    def getstops(self,rt='',dir='', **kwargs):
        """This modules will get vehicle information by route(rt) or by vehicle id (vid).  The
        routes can be either a list of comma-delimeted string.
        """
        params = {"key": self.apikey}
        request = "getstops"
        rt = kwargs.get("rt",rt)
        dir = kwargs.get("dir",dir)
        if rt:
            if type(rt) is list: rt = ",".join(rt)
            params["rt"] = rt
        if dir:  params["dir"] = dir
        else:   print "Must pass a rt and a dir"
        return [a for a in _pulldata(self.baseurl, request, params)]

    def getpatterns(self,rt='',pid='', **kwargs):
        """This modules will get vehicle information by route(rt) or by vehicle id (vid).  The
        routes can be either a list of comma-delimeted string.
        """
        params = {"key": self.apikey}
        request = "getpatterns"
        rt = kwargs.get("rt",rt)
        pid = kwargs.get("pid",pid)
        if rt:
            if type(rt) is list: rt = ",".join(rt)
            params["rt"] = rt
        elif pid:
            if type(pid) is list: pid = ",".join(pid)
            params["pid"] = pid
        else:   print "Must pass a rt or pid"
        return [a for a in _pulldata(self.baseurl, request, params)]

    def getroutes(self):
        """This modules will get route information.  Nothing needs to be passed in."""
        params = {"key": self.apikey}
        request = "getroutes"
        return [a for a in _pulldata(self.baseurl, request, params)]

    def gettime(self):
        """This modules will get route information.  Nothing needs to be passed in."""
        params = {"key": self.apikey}
        request = "gettime"
        timestring = [a for a in _pulldata(self.baseurl, request, params)][0].tm
        return time.strptime(timestring,"%Y%m%d %H:%M:%S")

    def getdirections(self,rt='', **kwargs):
        """Use the getdirections request to retrieve the set of directions serviced by the
        specified route.
        """
        params = {"key": self.apikey}
        request = "getdirections"
        params["rt"] = kwargs.get("rt",rt)
        return [a for a in _pulldata(self.baseurl, request, params)]

def _pulldata (baseurl, request, params):
    """This is a private class to query the server and return a response object."""
    try:
        url = "%s%s?%s" % (baseurl, request, urllib.urlencode(params))
        data = urllib.urlopen(url).read()
    except:
        pass
    try: 
        root = etree.fromstring(data)
        nodes = [node for node in root.getchildren() if node.tag != "error"]
        for child in nodes:
            tags = {}
            tags["tag"] = child.tag
            specials = ["tm","dir"]
            if child.tag in specials:   tags[child.tag] = child.text.strip()
            for child in child.getchildren():  
                tags[child.tag] = child.text.strip()
            yield response(tags)
    except:
        pass
# class response (object):
#     def __init__(self,attribs):
#         for attrib in attribs.keys():
#             self.__setattr__(attrib,attribs[attrib])
#     def __repr__(self):
#         #return "xml element: %s,  size: %d" % (self.tag, len([a for a in dir(self) if "__" not in a]))
#         return "xml element: %s,  children: %s" % (self.tag, [a for a in dir(self) if "__" not in a])

class response (dict):
    def __init__(self,attribs):
        for attrib in attribs.keys():
            self.__setitem__(attrib,attribs[attrib])

def populatedirections(bt, routes):
    """This function is used to add the directions for a list of routes.  The reason I didn't
    include this in the getroutes method is because it takes some time to poll their api for each
    route direction.
    """
    map(lambda x: x.__setitem__("directions",[y["dir"] for y in bt.getdirections(rt=x["rt"])]),routes)
    bt.directions = True
    return routes

def populatestops(bt,routes):
    """This function will populate the stops for a list of routes.  It will add a .stops attribute
    to ever route which will consist of a tuple with the first item being the Direction and the next
    will be a list of stops.  This will likely take a lot of time (Approximately one second per
    stop).
    """
    populatedirections(bt, routes)
    allstops = []
    for route in routes:
        route["stops"] = []
        for direction in route["directions"]:
            stops = bt.getstops(rt=route["rt"],dir=direction)
            route["stops"].append((direction,stops))
            allstops.extend(stops)
    return allstops

'''
Created on Dec 23, 2016

@author: Artur Korobeynyk
'''
import geo
import httplib
import time
import datetime
import json
import urllib
from geo import Geo

class vkparser(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.profiles = {}

    def set_location_by_name(self, loc):
        self.loc = geo.get_location_coordinates(loc)

    def set_location_by_coordinates(self, lat, lng):
        self.loc = (lat, lng)
    
    def set_start_time(self, stime="21/12/2016,00:00:00"):
        self.start_time = long(time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y,%H:%M:%S").timetuple()))
    
    def set_end_time(self, etime="23/12/2016,15:00:00"):
        self.end_time = long(time.mktime(datetime.datetime.strptime(etime, "%d/%m/%Y,%H:%M:%S").timetuple()))
    
    def fetch(self, radius=1500):
        request = '/method/photos.search?lat={lat}&long={lng}&count=1000&radius={rad}&start_time={st}&end_time={et}'.format(
            lat = self.loc["latitude"],
            lng = self.loc["longitude"],
            rad = radius,
            st = self.start_time,
            et = self.end_time)
        con = httplib.HTTPSConnection('api.vk.com', 443)
        con.request('GET', request)
        resp = json.loads(con.getresponse().read())
        for record in resp["response"]:
            if type(record) is int:
                continue
            profile_id = record["owner_id"]
            if "-" in str(profile_id):
                profile_id = str(profile_id).replace("-", "public")
            if profile_id not in self.profiles:
                self.profiles[profile_id] = {"images" : []}
            img = record["src"]
            try:
                geo_cordinates = Geo(record["lat"], record["long"])
            except(KeyError):
                geo_cordinates = Geo(None, None)
            insert = {"src" : img, "location" : geo_cordinates.get_location_name()}
            self.profiles[profile_id]["images"].append(insert)
        self.get_profiles()
        
    def get_profiles(self):
        usr_ids = [str(x) for x in self.profiles.keys() if type(x) is int]
        request = '/method/users.get?user_ids={ids}'.format(ids = urllib.quote(",".join(usr_ids),safe=''))
        con = httplib.HTTPSConnection('api.vk.com', 443)
        con.request('GET', request)
        resp = json.loads(con.getresponse().read())
        for i in resp["response"]:
            self.profiles[i["uid"]]["name"] = "%s %s" % (i["first_name"], i["last_name"])


if __name__ == "__main__":
    vk = vkparser()
    vk.set_start_time()
    vk.set_end_time()
    vk.set_location_by_name("Jauhajankuja 1B, Helsinki")
    vk.fetch()
    for i,j in vk.profiles.iteritems():
        print("%s\n\t%s\n\n" % (i,str(j)))
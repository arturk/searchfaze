'''
Created on Dec 23, 2016

@author: Artur Korobeynyk
'''

import time
import httplib
import json
import unittest
import urllib


def get_location_coordinates(loc):
        time.sleep(0.1)
        request = '/maps/api/geocode/json?address=%s' % urllib.quote(loc, safe='')
        con = httplib.HTTPSConnection('maps.googleapis.com', 443)
        con.request('GET', request)
        response = json.loads(con.getresponse().read())
        try:
            lat = str(response["results"][0]["geometry"]["location"]["lat"])
            lng = str(response["results"][0]["geometry"]["location"]["lng"])
        except:
            (lat, lng) = (None, None)
        finally:
            return {"latitude" : lat, "longitude" : lng}


class Geo(object):
    '''
    classdocs
    '''

    def __init__(self, latitude, longitude):
        '''
        Constructor
        '''
        self.latitude = latitude
        self.longitude = longitude

    def get_location_name(self):
        time.sleep(0.1)
        request = '/maps/api/geocode/json?latlng={lat},{lng}'.format(
            lat=str(self.latitude),
            lng=str(self.longitude))
        con = httplib.HTTPSConnection('maps.googleapis.com', 443)
        con.request('GET', request)
        response = json.loads(con.getresponse().read())
        try:
            address = unicode(''.join(response["results"][0]["formatted_address"].strip()))
        except:
            address = None
        finally:
            return address

class GeoTest(unittest.TestCase):
    def test_good_location(self):
        t = Geo("60.164624", "24.921875")
        expected = "Porkalagatan 4"
        actual = t.get_location_name()
        assert expected in actual, "Failed to determine correct location. Actual: {actual}. Expected: {expected}".format(actual=actual, expected=expected)
    
    def test_bad_location(self):
        t = Geo("111111", "111111")
        expected = None
        actual = t.get_location_name()
        assert expected == actual, "Unexistent address miscalculated. Expected: None, Actual: %s" % str(actual)
    
    def test_location_coordinates(self):
        lat, lng = get_location_coordinates("Porkalagatan 4, Helsinki")
        assert (lat, lng) == ("60.1646504", "24.9225171"), "Actual location coordinates: {alt}, {lng}".format(lat=lat, lng=lng)


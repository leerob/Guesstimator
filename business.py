import urllib2
import json


class Business:
    def __init__(self, name, address, rating, rating_count, checkin_count):
        self.name = name
        self.address = address
        self.rating = rating
        self.rating_count = rating_count
        self.checkin_count = checkin_count
        self.bayesian = 0.0
        self.source_count = 1


def make_request(url):
    """
    Makes a new HTTP request to the given URL

    :param url: The URL to request
    :returns: JSON response
    """
    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    response.close()

    return data

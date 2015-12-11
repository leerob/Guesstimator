import time

from api_keys import CLIENT_ID, CLIENT_SECRET, CATEGORY_ID
from business import Business, make_request

SEARCH_URL = 'https://api.foursquare.com/v2/venues/explore?ll={},{}&intent=browse&radius={}&limit=50&categoryId={}&client_id={}&client_secret={}&v={}'


def search(lat, lng, distance):
    """
    Searches the Foursquare API (Max Limit = 50)

    :param lat: Latitude of the request
    :param long: Longitude of the request
    :param distance: Distance to search (meters)
    :returns: List of retrieved venues
    """

    url = SEARCH_URL.format(lat, lng, distance,
                            CATEGORY_ID, CLIENT_ID, CLIENT_SECRET,
                            time.strftime("%Y%m%d"))
    venue_list = []

    try:
        data = make_request(url)

        for item in data['response']['groups'][0]['items']:
            venue = item['venue']
            venue_list.append(Business(venue['name'],
                                       venue['location']['address'],
                                       venue['rating'],
                                       venue['ratingSignals'],
                                       venue['stats']['checkinsCount']))
    except Exception, e:
        print e

    return venue_list

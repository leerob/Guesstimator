from api_keys import GOOGLE_API_KEY

from business import Business
from business import make_request


def search(lat, lng, distance):
    """
    Searches the Google Places API (Max Limit = 20)

    :param lat: Latitude of the request
    :param long: Longitude of the request
    :param distance: Distance to search (meters)
    :returns: List of retrieved places
    """

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%s&types=bar&key=%s' % (lat, lng, distance, GOOGLE_API_KEY)
    place_list = []

    try:
        data = make_request(url)

        for result in data['results']:
            place = search_place(result['place_id'])
            place_list.append(place)

    except Exception, e:
        print e

    return place_list


def search_place(place_id):

    """
    Searches Google for a specific Place

    :param id: Google Place ID
    :returns: Business object
    """

    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s' % (place_id, GOOGLE_API_KEY)

    try:
        data = make_request(url)

        place = data['result']
        return Business(place['name'],
                        place['formatted_address'].split(',')[0],
                        place['rating'],
                        place['user_ratings_total'],
                        'N/A')
    except Exception, e:
        print e

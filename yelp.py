import rauth

from api_keys import CONSUMER_KEY
from api_keys import CONSUMER_SECRET
from api_keys import TOKEN
from api_keys import TOKEN_SECRET

from business import Business


def search(lat, lng, distance):
    """
    Searches the Yelp API (Max Limit = 20)

    :param lat: Latitude of the request
    :param long: Longitude of the request
    :param distance: Distance to search (meters)
    :returns: List of retrieved businesses
    """

    params = {}
    params['term'] = 'nightlife,night_club,restaurant'
    params['ll'] = '%f,%f' % (lat, lng) 
    params['radius_filter'] = distance

    session = rauth.OAuth1Session(consumer_key = CONSUMER_KEY,
                                  consumer_secret = CONSUMER_SECRET,
                                  access_token = TOKEN,
                                  access_token_secret = TOKEN_SECRET)
        
    request = session.get('https://api.yelp.com/v2/search', params=params)
    data = request.json()
    session.close()

    business_list = []
    for business in data['businesses']:
        business_list.append(Business(business['name'],
                                      business['location']['display_address'][0],
                                      business['rating'],
                                      business['review_count'],
                                      'N/A'))
    return business_list

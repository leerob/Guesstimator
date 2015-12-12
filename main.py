import csv
import time

import foursquare
import yelp
import google


def bayesian(R, v, m, C):
    """
    Computes the Bayesian average for the given parameters

    :param R: Average rating for this business
    :param v: Number of ratings for this business
    :param m: Minimum ratings required
    :param C: Mean rating across the entire list
    :returns: Bayesian average
    """

    # Convert to floating point numbers
    R = float(R)
    v = float(v)
    m = float(m)
    C = float(C)

    return ((v / (v + m)) * R + (m / (v + m)) * C)


def get_input_locations():
    """
    Retrieves lat/long points from the user.

    :returns: Locations tuples
    """

    input_value = ''
    locations = []

    while input_value is not 'n':
        lat = float(raw_input('Lat: '))
        lng = float(raw_input('Long: '))
        locations.append((lat, lng))
        input_value = raw_input('Would you like more points? (y/n) ')

    return locations


def write_businesses(filename, businesses):
    """
    Saves list of businesses to a .csv file sorted by Bayesian rating

    :param filename: Output file name
    :param businesses: List of businesses to write
    """

    businesses.sort(key=lambda x: x.bayesian, reverse=True)

    with open(filename, 'w') as csvfile:

        categories = ['Name', 'Rating', 'Number of Ratings', 'Checkins', 'Sources']
        writer = csv.DictWriter(csvfile, fieldnames=categories)

        writer.writeheader()
        for business in businesses:
            writer.writerow({'Name': business.name.encode('utf-8'),
                             'Rating': '{0:.2f}'.format(business.bayesian),
                             'Number of Ratings': business.rating_count,
                             'Checkins': business.checkin_count,
                             'Sources': business.source_count})


def execute_search(locations, distance, search_engines):
    """
    Searches each API module at the given location(s) and distance.

    :param locations: User supplied lat/long point(s)
    :param distance: How far to search (meters)
    :param search_engines: List of search engine modules
    :returns: Full list of businesses
    """

    full_business_list = []
    for engine in search_engines:

        businesses = []
        for lat, lng in locations:
            print 'Searching {} at lat: {} long: {} ...'.format(engine.__name__, lat, lng)
            businesses.extend(engine.search(lat, lng, distance))
            time.sleep(1.0)  # Rate-limit API calls

        # Remove duplicates from API call overlap
        businesses = list(set(businesses))

        # Calculate low threshold and average ratings
        low_threshold = min(business.rating_count for business in businesses)
        average_rating = sum(business.rating for business in businesses) / len(businesses)

        # Convert to 10 point scale
        if engine.__name__ == 'foursquare':
            scale_multiplier = 1
        else:
            scale_multiplier = 2

        # Add bayesian estimates to business objects
        for business in businesses:
            business.bayesian = bayesian(business.rating * scale_multiplier,
                                         business.rating_count,
                                         low_threshold,
                                         average_rating * scale_multiplier)

        # Add this search engine's list to full business list
        full_business_list.extend(businesses)

    print 'Found {} total businesses!'.format(len(full_business_list))
    return full_business_list


def combine_duplicate_businesses(businesses):
    """
    Averages ratings of the same business from different sources

    :param businesses: Full list of businesses
    :returns: Filtered list with combined sources
    """

    seen_addresses = set()
    filtered_list = []
    for business in businesses:
        if business.address not in seen_addresses:
            filtered_list.append(business)
            seen_addresses.add(business.address)
        else:
            # Find duplicate in list
            for b in filtered_list:
                if b.address == business.address:
                    # Average bayesian ratings and update source count
                    new_rating = (b.bayesian + business.bayesian) / 2.0
                    b.bayesian = new_rating
                    b.source_count = b.source_count + 1

    return filtered_list


def main():
    """
    Searches the Foursquare, Google Places, and Yelp APIs at the given
    location and distance. Use different lat/long points to cover
    entire town since API calls have length limits.
    """

    distance = int(raw_input('Search Radius (meters): '))
    locations = get_input_locations()
    businesses = execute_search(locations, distance, [foursquare, google, yelp])
    filtered_list = combine_duplicate_businesses(businesses)
    write_businesses('data.csv', filtered_list)


if __name__ == '__main__':
    main()

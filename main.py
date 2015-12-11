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


def main():
    """
    Finds all the bars/restaurants in the given area. Use different
    lat/long points to cover entire town since API calls have length limits.
    """

    distance = int(raw_input('Search Radius (meters): '))
    locations = get_input_locations()

    venues, businesses, places = [], [], []

    for lat,lng in locations:

        # Retrieve all businesses for all sources
        print 'Searching lat: {} long: {} ...'.format(lat, lng)
        venues.extend(foursquare.search(lat, lng, distance))
        businesses.extend(yelp.search(lat, lng, distance))
        places.extend(google.search(lat, lng, distance))

        # Rate-limit API calls
        time.sleep(1.0)

    # Remove duplicates from API call overlap
    venues = list(set(venues))
    businesses = list(set(businesses))
    places = list(set(places))

    # Calculate low threshold and average ratings
    fs_low = min(venue.rating_count for venue in venues)
    fs_avg = sum(venue.rating for venue in venues) / len(venues)

    yp_low = min(business.rating_count for business in businesses)
    yp_avg = sum(business.rating for business in businesses) / len(businesses)

    gp_low = min(place.rating_count for place in places)
    gp_avg = sum(place.rating for place in places) / len(places)

    # Add bayesian estimates to business objects
    for v in venues:
        v.bayesian = bayesian(v.rating, v.rating_count, fs_low, fs_avg)
    for b in businesses:
        b.bayesian = bayesian(b.rating * 2, b.rating_count, yp_low, yp_avg * 2)
    for p in places:
        p.bayesian = bayesian(p.rating * 2, p.rating_count, gp_low, gp_avg * 2)

    # Combine all lists into one
    full_list = venues + businesses + places
    print 'Found {} total businesses!'.format(len(full_list))
    
    # Combine ratings of duplicates
    seen_addresses = set()
    filtered_list = []
    for business in full_list:
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
                 
    # Sort by Bayesian rating
    filtered_list.sort(key=lambda x: x.bayesian, reverse=True)

    # Write to .csv file
    with open('data.csv', 'w') as csvfile:

        categories = ['Name', 'Rating', 'Number of Ratings', 'Checkins', 'Sources']
        writer = csv.DictWriter(csvfile, fieldnames=categories)

        writer.writeheader()
        for venue in filtered_list:
            writer.writerow({'Name': venue.name.encode('utf-8'),
                             'Rating': '{0:.2f}'.format(venue.bayesian),
                             'Number of Ratings': venue.rating_count,
                             'Checkins': venue.checkin_count,
                             'Sources': venue.source_count})


if __name__ == '__main__':
    main()
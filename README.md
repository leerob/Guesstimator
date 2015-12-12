#Guesstimator
<img src="http://i.imgur.com/JMD7wo4.jpg" />

Guesstimator is a program that searches the Google Places, Yelp, and Foursquare APIs to create a list of bars in the given location. Then, it combines their ratings as a Bayesian estimate to rank them more accurately.

##Setup
You'll need to acquire API keys for each of the individual services and add them to api_keys.py.

- [Google Places](https://developers.google.com/places/web-service/get-api-key)
- [Yelp](https://www.yelp.com/developers/manage_api_keys)
- [Foursquare](https://developer.foursquare.com/)

You'll also need to install rauth for authentication.

`pip install rauth`
##Usage
    Search Radius (meters): 40000
    Lat: 41.5908
    Long: -93.6208
    Would you like more points? (y/n) n
    Searching foursquare at lat: 41.5908 long: -93.6208 ...
    Searching google at lat: 41.5908 long: -93.6208 ...
    Searching yelp at lat: 41.5908 long: -93.6208 ...
    Found 90 total businesses!


##Other Usages
This program could also be used to search restaurants, coffee shops, you name it. You'll need to:

- Update the Foursquare CATEGORY_ID
- Change the type parameter in the Google Search URL
- Modify the term parameter in the Yelp Search URL

Review the API documentation for each service to determine what types are allowed.


##Output

1. **El Bait Shop** - 8.93 with 3 sources
2. **Hessen Haus**  - 8.43 with 3 sources
3. **Zombie Burger + Drink Lab** - 8.73 with 2 sources
4. **The Royal Mile** - 8.28 with 3 sources
5. **Confluence Brewing Company** - 9.15 with 1 source
6. **High Life Lounge** - 8.53 with 2 sources
7. **Louie’s Wine Dive** - 8.45 with 2 sources
8. **Up-Down** - 8.42 with 2 sources
9. **Exile Brewing Company** - 8.88 with 1 source
10. **Court Avenue Restaurant & Brewing Company** - 8.26 with 2 sources

If you look at the raw data.csv, you'll notice I removed results that were primarily restaurants and adjusted the rankings based on the number of data sources. This isn't a perfect rating system, but it's an improvement from using a single source. 

##Issues
You'll have to create an edge case if two bars somehow happen to have the same address. You should never have more data sources in your .csv file than search engine modules. If you do, then two bars with the same address are getting bucketed together.
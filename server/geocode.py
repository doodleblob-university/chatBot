import requests ### imported module requests <https://pypi.python.org/pypi/requests> - 9/11/2017
### Charlie Barry
class geocode(object):
    def __init__(self):
        self.googlePlaces = 'AIzaSyDQ-mcgK1gSnI6soXWZnAA2Z9MeDnb5ZRo'
        self.googleGeocode = 'AIzaSyDiqfHUyzaaCEPr2gF04NPFyhR7Iew30vs'

    def getLocationCoords(self, location):
        '''Returns longitude and latitude in a dictionary, using Google Geocode API to fetch the co-ords'''
        placeID = self.getPlaceID(location)
        if placeID != "":
            url = 'https://maps.googleapis.com/maps/api/geocode/json?place_id={}&key={}'.format(placeID, self.googleGeocode)
            request = requests.get(url) #gets data from google geocode query, using the placeID
            placeinfo = request.json()  #turns data into json format
            if placeinfo['status'] == 'OK':
                lat = placeinfo['results'][0]['geometry']['location']['lat']
                lng = placeinfo['results'][0]['geometry']['location']['lng']
                return {'latitude': lat, 'longitude': lng}  #returns the longitude and latitude of the place ID in a dictionary
        return {}

    def getPlaceID(self, location):
        '''Uses Google Places API to predict the correct location to what the user entered, and returns the ID code for said location'''
        url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&types=geocode&key={}'.format(location, self.googlePlaces)
        request = requests.get(url) #gets data from google places query
        placeinfo = request.json()  #turns data into json format
        if placeinfo['status'] == "OK":
            return placeinfo['predictions'][0]['place_id']  #returns the place id from the json object
        return ""
